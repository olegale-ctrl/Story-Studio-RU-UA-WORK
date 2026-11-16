"""PREVIEW_ONLY regression with genuine SI results; all side effects denied."""
from contextlib import ExitStack, redirect_stdout, redirect_stderr
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import editor_preview as cli
from scripts.first_video import read_plan
from tests.test_story_intelligence_decision_projection_v1 import stale_args

ROOT = Path(__file__).resolve().parents[1]


def full():
    return json.loads((ROOT / 'examples/editor_input_example.json').read_text(encoding='utf-8'))


class EditorPreview(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.blocked = [self.stack.enter_context(patch(name, side_effect=AssertionError('forbidden effect')))
            for name in ('scripts.first_video.build', 'scripts.first_video.render_mp4',
                         'core.mp4_render.render_mp4', 'integrations.silero_local.SileroLocalProvider.synthesize',
                         'subprocess.run', 'subprocess.Popen', 'socket.socket', 'socket.create_connection',
                         'urllib.request.urlopen', 'wave.open')]
        self.addCleanup(self.stack.close)

    def tearDown(self):
        for mock in self.blocked:
            mock.assert_not_called()

    def render(self, data):
        before = deepcopy(data)
        status, files = cli.preview(data)
        self.assertEqual(data, before)
        self.assertEqual(status['production_readiness']['state'], 'NOT_ASSESSED')
        self.assertFalse(status['production_readiness']['permissions_granted'])
        self.assertEqual(len(status['production_readiness']['future_checks']), 6)
        self.assertTrue(all(x['code'] in cli.TEXT for x in status['diagnostics']))
        return status, files

    def test_full_real_cards_and_plans(self):
        data = full()
        real_eval, real_project = cli.evaluate_si, cli.project_evaluation
        with patch.object(cli, 'evaluate_si', wraps=real_eval) as evaluate, \
                patch.object(cli, 'project_evaluation', wraps=real_project) as project:
            status, files = self.render(data)
        evaluate.assert_called_once_with(**data['evaluation_inputs'])
        self.assertEqual(project.call_count, 2)
        self.assertEqual(status['adapter_state'], 'INPUT_COMPLETE')
        self.assertEqual(files['evaluation.json']['status'], 'OK')
        self.assertEqual(set(files), {'evaluation.json', 'private-card-ru.json', 'private-card-uk.json', 'plan-ru.json', 'plan-uk.json'})
        for locale in cli.LOCALES:
            self.assertEqual(files[f'private-card-{locale}.json'], real_project(data['evaluation_inputs'], files['evaluation.json'], locale))
            self.assertEqual(files[f'plan-{locale}.json']['scenes'], data['scene_drafts'][locale]['scenes'])
            self.assertEqual(status['plans'][locale]['state'], 'DRAFT_PLAN_VALID')

    def test_missing_audience_independent_from_actual_si_evaluation(self):
        data = full(); del data['audience']
        status, files = self.render(data)
        self.assertEqual(status['adapter_state'], 'NEEDS_INPUT')
        self.assertIn(('INPUT_MISSING', 'audience'), [(d['code'], d['section']) for d in status['diagnostics']])
        self.assertEqual(files['evaluation.json']['status'], 'OK')

    def test_missing_ratings_findings_no_evaluator_or_projection(self):
        for fields in [('ratings',), ('human_findings',), ('ratings', 'human_findings')]:
            for value in ('missing', None):
                with self.subTest(fields=fields, value=value):
                    data = full()
                    for field in fields:
                        if value == 'missing': del data['evaluation_inputs'][field]
                        else: data['evaluation_inputs'][field] = None
                    with patch.object(cli, 'evaluate_si') as evaluate, patch.object(cli, 'project_evaluation') as project:
                        status, files = self.render(data)
                    evaluate.assert_not_called(); project.assert_not_called()
                    self.assertEqual(status['evaluation']['state'], 'NOT_RUN')
                    self.assertNotIn('evaluation.json', files)
                    self.assertFalse(any(n.startswith('private-card') for n in files))
                    self.assertIn('plan-ru.json', files)

    def test_real_invalid_no_card_no_projection(self):
        data = full(); data['evaluation_inputs']['records'] = []
        with patch.object(cli, 'project_evaluation') as project:
            status, files = self.render(data)
        project.assert_not_called()
        self.assertEqual(status['evaluation']['state'], 'INVALID')
        self.assertEqual(files['evaluation.json']['status'], 'INVALID')
        self.assertIsNone(files['evaluation.json']['eligibility'])
        self.assertFalse(any(n.startswith('private-card') for n in files))
        self.assertIn('EVALUATION_INVALID', [d['code'] for d in status['diagnostics']])

    def test_real_stale_card_retains_stale_semantics(self):
        data = full(); data['evaluation_inputs'] = stale_args()
        status, files = self.render(data)
        self.assertEqual(status['evaluation']['state'], 'STALE')
        self.assertEqual(files['evaluation.json']['status'], 'STALE')
        self.assertIsNone(files['evaluation.json']['eligibility'])
        for locale in cli.LOCALES:
            card = files[f'private-card-{locale}.json']
            self.assertEqual(card, cli.project_evaluation(data['evaluation_inputs'], files['evaluation.json'], locale))
        self.assertIn('EVALUATION_STALE', [d['code'] for d in status['diagnostics']])

    def test_projection_unavailable_never_fabricated(self):
        for unavailable in ({'availability': 'UNAVAILABLE'}, None):
            with self.subTest(unavailable=unavailable):
                with patch.object(cli, 'project_evaluation', return_value=unavailable):
                    status, files = self.render(full())
                self.assertIn('evaluation.json', files)
                self.assertFalse(any(n.startswith('private-card') for n in files))
                self.assertTrue(all(x['state'] == 'UNAVAILABLE' for x in status['cards'].values()))

    def test_missing_uk_preserves_exact_ru_and_partial_drafts(self):
        data = full(); del data['scene_drafts']['uk']
        data['scene_drafts']['ru']['scenes'][0]['text'] = '  Точный текст\nе\u0301  '
        status, files = self.render(data)
        self.assertEqual(files['plan-ru.json']['scenes'][0]['text'], '  Точный текст\nе\u0301  ')
        self.assertEqual(status['plans']['uk']['state'], 'MISSING')
        self.assertNotIn('plan-uk.json', files)
        data['scene_drafts']['uk'] = {'scenes': [{'text': 'Готовий фрагмент'}, {'text': None}]}
        status, files = self.render(data)
        self.assertEqual(files['draft-uk.json'], data['scene_drafts']['uk'])
        self.assertNotIn('plan-uk.json', files)
        self.assertEqual(status['plans']['uk']['state'], 'PARTIAL')

    def test_all_rights_states_and_unknown_value_no_authority(self):
        for right in sorted(cli.RIGHTS) + ['SECRET_RIGHTS_TOKEN', None, {}, True]:
            with self.subTest(right=right):
                data = full(); data['materials'] = [dict(id='private-id', description='private material', kind='voice', rights_status=right)]
                status, files = self.render(data)
                self.assertEqual(files['evaluation.json']['status'], 'OK')
                self.assertNotIn('SECRET_RIGHTS_TOKEN', json.dumps(status))
                self.assertNotIn('private-id', json.dumps(status))
                self.assertNotIn('private material', json.dumps(status))

    def test_input_binding_change_determinism_detachment(self):
        data = full(); s1, f1 = self.render(data); s2, f2 = self.render(deepcopy(data))
        self.assertEqual((s1, f1), (s2, f2))
        data['scene_drafts']['ru']['scenes'][0]['text'] += '!'
        s3, f3 = self.render(data)
        self.assertNotEqual(s1['input_sha256'], s3['input_sha256'])
        self.assertNotEqual(f1['plan-ru.json'], f3['plan-ru.json'])
        f3['plan-ru.json']['scenes'].clear()
        self.assertTrue(data['scene_drafts']['ru']['scenes'])

    def test_closed_version_purpose_and_evaluator_shapes(self):
        cases = [dict(schema_version='UNKNOWN'), dict(purpose='PRODUCTION'), dict(secret_path='/PRIVATE'),
                 dict(evaluation_inputs={'ratings': 0}), dict(evaluation_inputs={'records': []})]
        for edit in cases:
            with self.subTest(edit=edit), patch.object(cli, 'evaluate_si') as evaluate:
                data = full(); data.update(edit); status, files = self.render(data)
                evaluate.assert_not_called()
                self.assertNotIn('evaluation.json', files)
                self.assertNotIn('/PRIVATE', json.dumps(status))

    def test_optional_unknown_sections_no_placeholder_creation(self):
        data = dict(schema_version=cli.VERSION, purpose='PREVIEW_ONLY')
        with patch.object(cli, 'evaluate_si') as evaluate:
            status, files = self.render(data)
        evaluate.assert_not_called(); self.assertEqual(files, {})
        self.assertEqual(status['adapter_state'], 'NEEDS_INPUT')
        self.assertEqual(set(status['sections']), {'topic', 'audience', 'evaluation_inputs', 'scene_drafts', 'materials'})

    def test_malformed_plans_no_complete_output(self):
        for draft in ({'scenes': [{'text': 'x', 'image': '../PRIVATE.png'}]},
                      {'scenes': [{'text': 'x', 'unexpected': 'PRIVATE'}]},
                      {'scenes': [{'text': 'x' * 2001}]}, {'scenes': []}, {'scenes': [False]}):
            with self.subTest(draft=draft):
                data = full(); data['scene_drafts']['ru'] = draft
                status, files = self.render(data)
                self.assertNotIn('plan-ru.json', files)
                self.assertNotIn('PRIVATE', json.dumps(status))

    def test_write_read_plan_private_files_and_no_reuse(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'input.json'; source.write_text(json.dumps(full(), ensure_ascii=False), encoding='utf-8')
            out = root / 'preview'; status = cli.run(source, out)
            self.assertEqual(status, json.loads((out / 'preview-status.json').read_text(encoding='utf-8')))
            for locale in cli.LOCALES:
                self.assertEqual(read_plan(out / f'plan-{locale}.json')['scenes'], full()['scene_drafts'][locale]['scenes'])
            self.assertTrue(all(p.suffix == '.json' for p in out.iterdir()))
            self.assertFalse((out / 'project.json').exists())
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            with self.assertRaises(FileExistsError): cli.run(source, out)
            self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})
            if __import__('os').name == 'posix':
                self.assertEqual(out.stat().st_mode & 0o777, 0o700)
                self.assertTrue(all(p.stat().st_mode & 0o777 == 0o600 for p in out.iterdir()))

    def test_bad_json_is_safe_status_only(self):
        cases = [b'{"schema_version":1,"schema_version":2}', b'\xff', b'{"x":NaN}', b'{"x":1.2}',
                 b'{"x":"\\ud800"}', b'[' * 70 + b'0' + b']' * 70, b' ' * 2_000_001]
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i, raw in enumerate(cases):
                with self.subTest(i=i):
                    source = root / 'input'; source.write_bytes(raw); out = root / str(i)
                    with patch.object(cli, 'evaluate_si') as evaluate:
                        status = cli.run(source, out)
                    evaluate.assert_not_called()
                    self.assertEqual([p.name for p in out.iterdir()], ['preview-status.json'])
                    self.assertEqual(status['diagnostics'][0]['code'], 'JSON_INVALID')
                    self.assertIsNone(status['input_sha256'])
                    if len(raw) <= 2_000_000:
                        self.assertEqual(status['source_sha256'], __import__('hashlib').sha256(raw).hexdigest())

    def test_failures_no_private_exception_echo_and_atomic_plan_check(self):
        with patch.object(cli, 'evaluate_si', side_effect=RuntimeError('/PRIVATE/secret')):
            status, files = self.render(full())
            self.assertEqual(status['evaluation']['state'], 'FAILED')
            self.assertNotIn('/PRIVATE', json.dumps(status))
            self.assertNotIn('evaluation.json', files)
        with TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'input'; source.write_text(json.dumps(full()), encoding='utf-8')
            with patch.object(cli, 'read_plan', side_effect=ValueError('PRIVATE')):
                with self.assertRaises(ValueError): cli.run(source, root / 'out')
            self.assertFalse((root / 'out').exists())
            self.assertEqual([p.name for p in root.iterdir()], ['input'])

    def test_cli_no_paths_or_source_fragments_in_console(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp); output = StringIO(); errors = StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                result = cli.main([str(root / 'PRIVATE_MISSING'), '--output-dir', str(root / 'out')])
            self.assertEqual(result, 2)
            self.assertEqual(errors.getvalue(), 'EDITOR_PREVIEW_IO_FAILED\n')
            self.assertNotIn('PRIVATE', output.getvalue() + errors.getvalue())


if __name__ == '__main__':
    unittest.main()
