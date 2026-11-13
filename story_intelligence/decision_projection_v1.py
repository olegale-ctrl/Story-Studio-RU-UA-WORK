"""Pure private RU/UK explanation of pinned bounded EVALUATE results.

PD-01: every admitted invocation is recomputed by the unchanged evaluator and
compared in canonical bytes. No cache, authority, provider, I/O or clock. Strings
are frozen from the owner-approved SI-PRODUCT-01.0 contract at f56f4ea2.
"""
from copy import deepcopy
import re

from .codec_v1 import canonical_si_json, canonical_si_sha256
from .model_v1 import validate_si_ref
from .evaluate_v1 import evaluate_si as _evaluate

__all__ = ['project_evaluation']

_CONDITIONS = {'RC01': ('Не определено, нужны ли данные за конкретный период.',
          'Не визначено, чи потрібні дані за конкретний період.',
          'A1'),
 'RC02': ('Не решено, нужны ли данные за конкретный период.',
          'Не вирішено, чи потрібні дані за конкретний період.',
          'A1'),
 'RC03': ('Не задан состав необходимых данных.', 'Не задано склад необхідних даних.', 'A2'),
 'RC04': ('Не уточнено, какие данные нужны от источника.',
          'Не уточнено, які дані потрібні від джерела.',
          'A2'),
 'RC05': ('Не задан необходимый период данных.', 'Не задано необхідний період даних.', 'A3'),
 'RC06': ('Не представлено рассмотрение свежести источника.',
          'Не надано розгляд свіжості джерела.',
          'A4'),
 'RC07': ('Не решено, нужна ли проверка свежести источника.',
          'Не вирішено, чи потрібна перевірка свіжості джерела.',
          'A4'),
 'RC08': ('Достаточность подтверждения свежести источника не установлена.',
          'Достатність підтвердження свіжості джерела не встановлено.',
          'A4'),
 'RC09': ('Не задан рассмотренный период для источника.',
          'Не задано розглянутий період для джерела.',
          'A4'),
 'C01': ('Для центрального фактического утверждения не представлена применимая проверка.',
         'Для центрального фактичного твердження не надано застосовної перевірки.',
         'A5'),
 'C02': ('Проверка центрального фактического утверждения остаётся нерешённой или недостаточной.',
         'Перевірка центрального фактичного твердження залишається невирішеною або недостатньою.',
         'A5'),
 'C03': ('Проверка утверждения требует дополнительного исследования.',
         'Перевірка твердження потребує додаткового дослідження.',
         'A5'),
 'C04': ('Не представлена применимая проверка утверждения.',
         'Не надано застосовної перевірки твердження.',
         'A5'),
 'C05': ('В зафиксированных данных остаётся противоречие.',
         'У зафіксованих даних залишається суперечність.',
         'A5'),
 'K01': ('В данных зафиксирован блокирующий научный риск.',
         'У даних зафіксовано блокувальний науковий ризик.',
         'A6'),
 'K02': ('В данных зафиксирован блокирующий правовой риск.',
         'У даних зафіксовано блокувальний правовий ризик.',
         'A6'),
 'K03': ('В данных зафиксирован блокирующий этический риск.',
         'У даних зафіксовано блокувальний етичний ризик.',
         'A6'),
 'K04': ('В данных зафиксирован блокирующий репутационный риск.',
         'У даних зафіксовано блокувальний репутаційний ризик.',
         'A6'),
 'K05': ('В данных зафиксирован блокирующий производственный риск.',
         'У даних зафіксовано блокувальний виробничий ризик.',
         'A6'),
 'K06': ('В данных зафиксирован блокирующий рыночный риск.',
         'У даних зафіксовано блокувальний ринковий ризик.',
         'A6'),
 'V01': ('Для необходимого материала не установлена достаточная основа использования.',
         'Для необхідного матеріалу не встановлено достатньої підстави використання.',
         'A7'),
 'Q01': ('Не задан уровень подготовки аудитории.', 'Не задано рівень підготовки аудиторії.', 'A8'),
 'Q02': ('Не задана мотивация аудитории.', 'Не задано мотивацію аудиторії.', 'A8'),
 'Q03': ('Не заданы исходные производственные ограничения.',
         'Не задано вихідні виробничі обмеження.',
         'A9'),
 'Q04': ('Исследование источников не завершено для заявленных утверждений.',
         'Дослідження джерел не завершено для заявлених тверджень.',
         'A5'),
 'F01': ('Не задана одна из обязательных оценок по рубрике.',
         "Не задано одну з обов'язкових оцінок за рубрикою.",
         'A10'),
 'F02': ('Рассмотрение неопределённости одной из оценок отсутствует или недостаточно.',
         'Розгляд невизначеності однієї з оцінок відсутній або недостатній.',
         'A10'),
 'F03': ('Исследование локального портфеля не завершено.',
         'Дослідження локального портфеля не завершено.',
         'A11'),
 'F04': ('Не представлено обязательное сравнение с записью локального портфеля.',
         "Не надано обов'язкового порівняння із записом локального портфеля.",
         'A11'),
 'F05': ('Редакционное решение о пересечении с локальным портфелем остаётся открытым.',
         'Редакційне рішення про перетин із локальним портфелем залишається відкритим.',
         'A11')}

_ACTIONS = {'A0': ('Проверьте полноту и совместимость данных для пояснения.',
        'Перевірте повноту й сумісність даних для пояснення.'),
 'A1': ('Решите, нужны ли данные за конкретный период, и явно задайте это условие.',
        'Вирішіть, чи потрібні дані за конкретний період, і явно задайте цю умову.'),
 'A2': ('Уточните состав и содержание необходимых данных.',
        'Уточніть склад і зміст необхідних даних.'),
 'A3': ('Задайте необходимый период данных.', 'Задайте необхідний період даних.'),
 'A4': ('Рассмотрите свежесть источника за нужный период и достаточность зафиксированных '
        'подтверждений.',
        'Розгляньте свіжість джерела за потрібний період і достатність зафіксованих підтверджень.'),
 'A5': ('Исследуйте утверждение и противоречащие данные; передайте существенные разногласия на '
        'рассмотрение человеку.',
        'Дослідіть твердження й суперечливі дані; передайте суттєві розбіжності на розгляд '
        'людині.'),
 'A6': ('Передайте отмеченный риск на рассмотрение ответственному человеку; текст плана сам по '
        'себе риск не снимает.',
        'Передайте зазначений ризик на розгляд відповідальній людині; текст плану сам собою ризик '
        'не усуває.'),
 'A7': ('Рассмотрите точный материал, предполагаемое использование и права; описание замены не '
        'подтверждает её допустимость.',
        'Розгляньте точний матеріал, передбачене використання й права; опис заміни не підтверджує '
        'її допустимості.'),
 'A8': ('Уточните редакционную гипотезу об аудитории, не выдавая её за измеренный спрос.',
        'Уточніть редакційну гіпотезу про аудиторію, не видаючи її за виміряний попит.'),
 'A9': ('Уточните ограничения производства; фактическую выполнимость проверьте отдельно.',
        'Уточніть обмеження виробництва; фактичну здійсненність перевірте окремо.'),
 'A10': ('Представьте недостающую оценку или рассмотрите её неопределённость, сохраняя неизвестные '
         'значения явно.',
         'Надайте відсутню оцінку або розгляньте її невизначеність, зберігаючи невідомі значення '
         'явно.'),
 'A11': ('Сравните тему с указанными записями локального портфеля и примите редакционное решение.',
         'Порівняйте тему із зазначеними записами локального портфеля й ухваліть редакційне '
         'рішення.')}

_LIMITS = (('Карточка поясняет только оценку переданного контекста; полнота внешних данных не установлена.',
  'Картка пояснює лише оцінку переданого контексту; повноту зовнішніх даних не встановлено.'),
 ('Баллы и уверенность не доказывают научную истинность, достоверность источников или спрос '
  'аудитории.',
  'Бали й упевненість не доводять наукової істинності, достовірності джерел або попиту аудиторії.'),
 ('Рассмотрение научных выводов человеком и всех семи областей научной проверки этой карточкой не '
  'удостоверяется.',
  'Розгляд наукових висновків людиною й усіх семи сфер наукової перевірки цією карткою не '
  'засвідчується.'),
 ('Права на материалы, фактическая доступность и выполнимость производства требуют отдельной '
  'проверки.',
  'Права на матеріали, фактична доступність і здійсненність виробництва потребують окремої '
  'перевірки.'),
 ('Карточка не удостоверяет личность, компетентность или полномочия проверяющего и не '
  'предоставляет редакционного утверждения.',
  'Картка не засвідчує особу, компетентність або повноваження перевіряльника й не надає '
  'редакційного затвердження.'),
 ('Допуск к творческой разработке не является разрешением на производство или публикацию.',
  'Допуск до творчої розробки не є дозволом на виробництво або публікацію.'))

_SUBJECTS = {'SourceItem': ('Источник', 'Джерело'),
 'StoryIdea': ('Тема', 'Тема'),
 'Rubric': ('Рубрика', 'Рубрика'),
 'ChannelContext': ('Контекст канала', 'Контекст каналу'),
 'AudienceHypothesis': ('Гипотеза об аудитории', 'Гіпотеза про аудиторію'),
 'ClaimItem': ('Утверждение', 'Твердження'),
 'ClaimCheck': ('Проверка утверждения', 'Перевірка твердження'),
 'EvidenceItem': ('Свидетельство', 'Свідчення'),
 'Risk': ('Риск', 'Ризик'),
 'VisualRequirement': ('Материал', 'Матеріал')}

_LABELS = {'audience_interest': ('Интерес аудитории', 'Інтерес аудиторії'),
 'channel_fit': ('Соответствие каналу', 'Відповідність каналу'),
 'angle_novelty': ('Новизна ракурса', 'Новизна ракурсу'),
 'evidence_quality': ('Качество подтверждений', 'Якість підтверджень'),
 'narrative_potential': ('Потенциал повествования', 'Потенціал оповіді'),
 'visual_feasibility': ('Возможность визуального воплощения', 'Можливість візуального втілення'),
 'resource_fit': ('Соответствие ресурсам', 'Відповідність ресурсам'),
 'risk_manageability': ('Управляемость рисков', 'Керованість ризиків'),
 'portfolio_distinctness': ('Отличие от локального портфеля',
                            'Відмінність від локального портфеля')}

_SUMMARIES = {'ELIGIBLE_FOR_CREATIVE': ('Можно продолжить творческую разработку в пределах этой оценки. Эта '
                           'оценка не предоставляет допуска к производству.',
                           'Можна продовжити творчу розробку в межах цієї оцінки. Ця оцінка не '
                           'надає допуску до виробництва.'),
 'NEEDS_INPUT': ('Сначала уточните необходимые исходные данные.',
                 'Спочатку уточніть необхідні вихідні дані.'),
 'NEEDS_RESEARCH': ('Сначала закройте отмеченные исследовательские пробелы.',
                    'Спочатку усуньте зазначені дослідницькі прогалини.'),
 'REVIEW_DUPLICATE': ('Нужна редакционная проверка пересечения с портфелем.',
                      'Потрібна редакційна перевірка перетину з портфелем.'),
 'BLOCKED': ('Продолжение творческой разработки заблокировано отмеченными условиями.',
             'Продовження творчої розробки заблоковане зазначеними умовами.'),
 'STALE': ('Оценка устарела относительно переданного контекста. Использовать прежнее решение '
           'нельзя.',
           'Оцінка застаріла щодо переданого контексту. Використовувати попереднє рішення не '
           'можна.'),
 'INVALID': ('На основании переданных данных нельзя принять результат оценки.',
             'На підставі переданих даних не можна прийняти результат оцінки.')}

_INVALID = {'TYPE': ('Структура переданных данных не позволяет принять результат оценки.',
          'Структура переданих даних не дає змоги прийняти результат оцінки.'),
 'UNKNOWN_FIELD': ('Структура переданных данных не позволяет принять результат оценки.',
                   'Структура переданих даних не дає змоги прийняти результат оцінки.'),
 'MISSING_FIELD': ('Структура переданных данных не позволяет принять результат оценки.',
                   'Структура переданих даних не дає змоги прийняти результат оцінки.'),
 'LIMIT': ('Переданные данные выходят за поддерживаемые ограничения.',
           'Передані дані виходять за підтримувані обмеження.'),
 'VERSION_UNSUPPORTED': ('Версия переданных данных не поддерживается.',
                         'Версія переданих даних не підтримується.'),
 'REF_MISSING': ('Не удалось проверить необходимые точные связи данных.',
                 "Не вдалося перевірити необхідні точні зв'язки даних."),
 'REF_TYPE_MISMATCH': ('Точные связи или содержимое данных не согласованы.',
                       "Точні зв'язки або вміст даних не узгоджені."),
 'REF_HASH_MISMATCH': ('Точные связи или содержимое данных не согласованы.',
                       "Точні зв'язки або вміст даних не узгоджені."),
 'DEPENDENCY_CYCLE': ('В зависимостях переданных данных обнаружен недопустимый цикл.',
                      'У залежностях переданих даних виявлено неприпустимий цикл.'),
 'PROVENANCE_MISMATCH': ('Заявленное происхождение данных не согласовано.',
                         'Заявлене походження даних не узгоджене.'),
 'LOCALE_MISMATCH': ('Языковые параметры оценки не согласованы.',
                     'Мовні параметри оцінки не узгоджені.'),
 'SELECTION_CONFLICT': ('Переданные сведения о выборе не согласованы.',
                        'Передані відомості про вибір не узгоджені.'),
 'EVIDENCE_NEEDED': ('Данные проверки утверждения некорректны для принятия результата.',
                     'Дані перевірки твердження некоректні для прийняття результату.'),
 'RIGHTS_BLOCKED': ('Данные об использовании материала некорректны для принятия результата.',
                    'Дані про використання матеріалу некоректні для прийняття результату.'),
 'PRIVACY_REVIEW_REQUIRED': ('Переданные данные не прошли проверку ограничений приватности.',
                             'Передані дані не пройшли перевірку обмежень приватності.'),
 'PRIVACY_BLOCKED': ('Переданные данные не прошли проверку ограничений приватности.',
                     'Передані дані не пройшли перевірку обмежень приватності.')}

_UNAVAILABLE = ('Пояснение оценки недоступно. Не используйте эту карточку для решения о продолжении работы.',
 'Пояснення оцінки недоступне. Не використовуйте цю картку для рішення про продовження роботи.')

_REQUIRED = frozenset(('records', 'semantic_input_refs', 'observed_context',
                       'ratings', 'expected_context', 'human_findings'))
_OPTIONAL = frozenset(('required_current_premise', 'ui_locale'))
_VERSION = 'editorial-decision-projection/1'
_N = r'(0|[1-9][0-9]*)'
_P, _F = '$.required_current_premise', '$.human_findings'
_E, _CC, _DR, _RB = ('EVIDENCE_NEEDED', 'CENTRAL_CLAIM_UNSUPPORTED',
                     'DUPLICATE_REVIEW_NEEDED', 'RIGHTS_BLOCKED')
_RISKS = dict(zip(('SCIENTIFIC', 'LEGAL', 'ETHICAL', 'REPUTATIONAL', 'PRODUCTION', 'MARKET'),
                 ('K01', 'K02', 'K03', 'K04', 'K05', 'K06')))
_BASE = ('Основание — условия, зафиксированные оценкой переданных данных.',
         'Підстава — умови, зафіксовані оцінкою переданих даних.')
_ABSENCE = ('В этой оценке не осталось отмеченных условий, препятствующих творческой разработке.',
            'У цій оцінці не залишилося зазначених умов, що перешкоджають творчій розробці.')
_CONTINUE = ('Редактору следует решить, продолжать ли творческую разработку.',
             'Редактору слід вирішити, чи продовжувати творчу розробку.')
_UNKNOWN_SCORE = ('Итоговый балл не определён.', 'Підсумковий бал не визначений.')
_STALE = ('Версии или контекст оценки изменились.', 'Версії або контекст оцінки змінилися.')
_STALE_ACTION = ('После проверки точных версий и контекста заново выполните оценку.',
                 'Після перевірки точних версій і контексту виконайте оцінку заново.')
_INVALID_ACTION = ('Проверьте состав данных и точность их связей; затем повторите оценку.',
                   "Перевірте склад даних і точність їхніх зв'язків; потім повторіть оцінку.")


class _Unsupported(Exception):
    pass


def _need(condition):
    if not condition:
        raise _Unsupported()


def _plain(value):
    """Only builtin trees; do not invoke untrusted deepcopy/equality hooks.

    Floats are allowed only in invocation data so genuine evaluator INVALID
    witnesses (including P34) can be explained. They cannot pass canonical result
    comparison or become displayed values. No arbitrary bundle-size quota added.
    """
    active, pending = set(), [(value, False)]
    while pending:
        child, leaving = pending.pop()
        if leaving:
            active.remove(id(child))
            continue
        kind = type(child)
        if kind in (type(None), bool, int, float, str):
            continue
        if kind not in (dict, list) or id(child) in active:
            return False
        if kind is dict and any(type(k) is not str for k in child):
            return False
        active.add(id(child))
        pending.append((child, True))
        values = child.values() if kind is dict else child
        pending.extend((item, False) for item in values)
    return True


def _card(locale, summary, reasons, gaps, actions, available=True):
    return {'projection_version': _VERSION, 'display_locale': ('ru', 'uk')[locale],
            'availability': 'DISPLAYABLE' if available else 'UNAVAILABLE',
            'sections': {'decision_summary': summary, 'reasons': list(reasons),
                         'blocking_risks_and_gaps': list(gaps), 'next_actions': list(actions),
                         'limitations': [value[locale] for value in _LIMITS]}}


def _unavailable(locale):
    return _card(locale, _UNAVAILABLE[locale], [], [], [_ACTIONS['A0'][locale]], False)


def _key(ref):
    return (ref['type'], ref['id'], ref['revision'], ref['sha256'])


def _record_ref(record):
    h = record['H']
    return dict(type=h['type'], id=h['id'], revision=h['revision'],
                sha256=canonical_si_sha256(record))


def _same_ref(actual, expected, kind):
    _need(actual == expected and type(actual) is dict and actual['type'] == kind)


def _shape(result):
    """Check the actual two result shapes, never treat eligibility as status."""
    _need(type(result) is dict)
    status = result['status']
    _need(type(status) is str and status in ('OK', 'STALE', 'INVALID'))
    fields = {'status', 'currentness', 'locale', 'eligibility', 'aggregate_tenths',
              'ratings', 'diagnostics'}
    _need(set(result) == (fields if status == 'OK' else fields | {'reason_codes'}))
    _need(type(result['diagnostics']) is list)
    for d in result['diagnostics']:
        _need(type(d) is dict and set(d) == {'code', 'field_path', 'input_ref', 'message'})
        _need(all(type(d[k]) is str and d[k] for k in ('code', 'field_path', 'message')))
        if d['input_ref'] is not None:
            validate_si_ref(d['input_ref'])  # Syntax only; never resolve rejected refs.
    if status == 'OK':
        _need(result['currentness'] == 'CURRENT' and result['locale'] in ('ru', 'uk'))
        e = result['eligibility']
        _need(type(e) is dict and set(e) == {'state', 'reason_codes'})
        _need(e['state'] in _SUMMARIES and e['state'] not in ('STALE', 'INVALID'))
        codes = e['reason_codes']
        _need(type(result['ratings']) is list and len(result['ratings']) == 9)
        aggregate = result['aggregate_tenths']
        _need(type(aggregate) is dict)
        if aggregate.get('state') == 'KNOWN':
            _need(set(aggregate) == {'state', 'value'} and type(aggregate['value']) is int
                  and 0 <= aggregate['value'] <= 1000)
        else:
            _need(set(aggregate) == {'state', 'reason'} and aggregate['state'] == 'UNKNOWN'
                  and type(aggregate['reason']) is str and bool(aggregate['reason']))
        _need(all(d['code'] in (_E, _CC, _DR, _RB) for d in result['diagnostics']))
    else:
        _need(result['currentness'] == status and result['locale'] is None
              and result['eligibility'] is None and result['aggregate_tenths'] is None
              and result['ratings'] == [] and bool(result['diagnostics']))
        codes = result['reason_codes']
        allowed = ('INPUT_STALE',) if status == 'STALE' else _INVALID
        _need(all(d['code'] in allowed for d in result['diagnostics']))
    _need(type(codes) is list and codes == sorted({d['code'] for d in result['diagnostics']}))
    identities = [canonical_si_json(d) for d in result['diagnostics']]
    _need(len(set(identities)) == len(identities))
    return status


class _Context:
    """Private exact lookups only after real evaluator verification succeeded."""
    def __init__(self, inputs):
        self.inputs = inputs
        self.refs = [_record_ref(r) for r in inputs['records']]
        self.records = inputs['records']
        self.index = {_key(ref): r for ref, r in zip(self.refs, self.records)}
        self.binding = inputs['human_findings']['binding']
        self.premise = inputs.get('required_current_premise')

    def payload(self, ref):
        return self.index[_key(ref)]['payload']

    def core(self, name):
        return self.binding[name + '_ref']

    def match(self, d):
        code, path, ref, message = (d[k] for k in ('code', 'field_path', 'input_ref', 'message'))
        matches = []

        def emit(family, expected_code, expected_ref, kind, fixed, rank, slot=None):
            if code == expected_code and message == fixed:
                if kind is None:
                    _need(ref is None and expected_ref is None)
                else:
                    _same_ref(ref, expected_ref, kind)
                    _need(_key(ref) in self.index)
                matches.append((family, rank, slot))

        if path == _P and self.premise is None:
            emit('RC01', _E, None, None, 'Required-current determination is missing.', 1)
        if self.premise is not None:
            p = self.premise
            if path == _P + '.determination' and p['determination'] == 'UNDETERMINED':
                emit('RC02', _E, self.core('idea'), 'StoryIdea', 'Required-current determination is unresolved.', 1)
            if path == _P + '.required_data' and p['determination'] == 'REQUIRED':
                emit('RC03', _E, self.core('idea'), 'StoryIdea', 'Required data specification is missing.', 1)
            found = re.fullmatch(re.escape(_P) + r'\.required_data\.value\[' + _N + r'\]\.(specification|period)', path)
            if found:
                item = p['required_data']['value'][int(found[1])]
                field = found[2]
                _need(item[field]['state'] == 'UNKNOWN')
                emit('RC04' if field == 'specification' else 'RC05', _E, item['source_ref'],
                     'SourceItem', 'Required source data are unspecified.' if field == 'specification'
                     else 'Required period is unspecified.', 1)
            if path == _P + '.source_freshness':
                _need(type(ref) is dict and ref['type'] == 'SourceItem')
                _need(ref not in [a['source_ref'] for a in p['source_freshness']])
                emit('RC06', _E, ref, 'SourceItem', 'Source freshness review is missing.', 2)
            found = re.fullmatch(re.escape(_P) + r'\.source_freshness\[' + _N + r'\]\.(applicability|outcome|review_period)', path)
            if found:
                item = p['source_freshness'][int(found[1])]
                family, fixed = {'applicability': ('RC07', 'Source freshness applicability is unresolved.'),
                                 'outcome': ('RC08', 'Source freshness evidence is insufficient.'),
                                 'review_period': ('RC09', 'Source review period is unspecified.')}[found[2]]
                _need(item['applicability'] != 'NOT_APPLICABLE')
                emit(family, _E, item['source_ref'], 'SourceItem', fixed, 2)

        found = re.fullmatch(r'\$\.records\[' + _N + r'\]\.payload\.([a-z_]+)', path)
        if found:
            i, field = int(found[1]), found[2]
            record, expected_ref = self.records[i], self.refs[i]
            kind, p = record['H']['type'], record['payload']
            if kind == 'ClaimItem':
                if field == 'materiality':
                    _need(p['claim_kind'] == 'factual' and p['materiality'] == 'CENTRAL')
                    emit('C01', _CC, expected_ref, kind, 'A central factual claim lacks applicable support.', 0)
                if field == 'evidence_expectation':
                    emit('C04', _E, expected_ref, kind, 'Claim support requires research.', 2)
            if kind in ('ClaimCheck', 'EvidenceItem') and field in ('state', 'relation'):
                claim = self.payload(p['claim_ref'])
                _need(claim['claim_kind'] != 'fictional')
                central = claim['claim_kind'] == 'factual' and claim['materiality'] == 'CENTRAL'
                expected_code, rank = (_CC, 0) if central else (_E, 2)
                if kind == 'ClaimCheck' and field == 'state':
                    emit('C02' if central else 'C03', expected_code, expected_ref, kind,
                         'A central factual claim has unresolved review.' if central
                         else 'Claim review requires further research.', rank)
                if kind == 'EvidenceItem' and field == 'relation' and p['relation'] == 'contradicts':
                    emit('C05', expected_code, expected_ref, kind, 'Recorded evidence remains in conflict.', rank)
            if kind == 'Risk' and field in ('blocking', 'resolution_basis_refs'):
                _need(p['blocking'] is True)
                _need(field == ('resolution_basis_refs' if p['resolution'] == 'MITIGATED' else 'blocking'))
                emit(_RISKS[p['category']], _E, expected_ref, kind,
                     'An explicit ' + p['category'].lower() + ' risk remains blocking.', 0)
            if kind == 'VisualRequirement' and field == 'rights_state' and p['role'] == 'REQUIRED':
                emit('V01', _RB, expected_ref, kind, 'Essential material rights are unresolved.', 0)
            mapping = {('AudienceHypothesis', 'knowledge_level'): ('Q01', 'Audience knowledge level is unspecified.', 1),
                       ('AudienceHypothesis', 'motivation'): ('Q02', 'Audience motivation is unspecified.', 1),
                       ('ChannelContext', 'capability_notes'): ('Q03', 'Production constraints are unspecified.', 1),
                       ('StoryIdea', 'source_refs'): ('Q04', 'Source research is incomplete.', 2),
                       ('ChannelContext', 'portfolio'): ('F03', 'Portfolio research is incomplete.', 2)}
            if (kind, field) in mapping:
                family, fixed, rank = mapping[(kind, field)]
                _need(p[field]['state'] == 'UNKNOWN')
                emit(family, _E, expected_ref, kind, fixed, rank)

        found = re.fullmatch(r'\$\.ratings\[' + _N + r'\]\.value', path)
        if found:
            i = int(found[1]); _need(self.inputs['ratings'][i]['value']['state'] == 'UNKNOWN')
            emit('F01', _E, self.core('rubric'), 'Rubric', 'A required rating is unknown.', 2, i)
        if path == _F + '.confidence_findings':
            values = self.inputs['human_findings']['confidence_findings']
            for i, (key, rating) in enumerate(zip(_LABELS, self.inputs['ratings'])):
                value = next((v for v in values if v['criterion_key'] == key), None)
                if rating['confidence']['level'] == 'UNKNOWN' and (value is None or value['outcome'] == 'INSUFFICIENT'):
                    emit('F02', _E, self.core('rubric'), 'Rubric',
                         'Confidence consideration is missing or insufficient for ' + key + '.', 2, i)
        if path == _F + '.duplicate_findings':
            values = self.inputs['human_findings']['duplicate_findings']
            portfolio = self.payload(self.core('channel'))['portfolio']['value']
            missing = set(range(len(portfolio))) - {v['portfolio_entry_index'] for v in values}
            for i in sorted(missing):
                emit('F04', _DR, self.core('channel'), 'ChannelContext',
                     f'Portfolio comparison is missing for index {i}.', 3, i)
        found = re.fullmatch(re.escape(_F) + r'\.duplicate_findings\[' + _N + r'\]\.outcome', path)
        if found:
            item = self.inputs['human_findings']['duplicate_findings'][int(found[1])]
            _need(item['outcome'] in ('DUPLICATE', 'UNRESOLVED'))
            emit('F05', _DR, self.core('channel'), 'ChannelContext',
                 'A portfolio comparison is unresolved.', 3, item['portfolio_entry_index'])
        _need(len(matches) == 1)
        return matches[0]


def _sort_key(d, rank=-1):
    return (rank, d['code'], d['field_path'], canonical_si_json(d['input_ref']), d['message'])


def _render(result, inputs, locale):
    status = _shape(result)
    diagnostics = result['diagnostics']
    if status != 'OK':
        order = [_sort_key(d) for d in diagnostics]
        _need(order == sorted(order))
        reasons = [(_STALE if status == 'STALE' else _INVALID[d['code']])[locale] for d in diagnostics]
        action = (_STALE_ACTION if status == 'STALE' else _INVALID_ACTION)[locale]
        return _card(locale, _SUMMARIES[status][locale], reasons, reasons, [action for _ in diagnostics])
    context = _Context(inputs)
    matched = [context.match(d) for d in diagnostics]  # Complete coverage before Card.
    order = [_sort_key(d, m[1]) for d, m in zip(diagnostics, matched)]
    _need(order == sorted(order))
    aliases, counters, gaps, actions = {}, {}, [], []
    for d, (family, _, slot) in zip(diagnostics, matched):
        ref = d['input_ref']; prefix = ''
        if ref is not None:
            key = _key(ref); kind = ref['type']
            if key not in aliases:
                counters[kind] = counters.get(kind, 0) + 1
                aliases[key] = _SUBJECTS[kind][locale] + ' ' + str(counters[kind])
            prefix = aliases[key]
        if family in ('F01', 'F02'):
            label = list(_LABELS.values())[slot][locale]
            prefix += (' / Оценка «' if locale == 0 else ' / Оцінка «') + label + '»'
        elif family in ('F04', 'F05'):
            prefix += (' / Сравнение ' if locale == 0 else ' / Порівняння ') + str(slot + 1)
        prefix += ': ' if prefix else ''
        text = _CONDITIONS[family]
        gaps.append(prefix + text[locale])
        actions.append(prefix + _ACTIONS[text[2]][locale])
    score = result['aggregate_tenths']
    score_line = (_UNKNOWN_SCORE[locale] if score['state'] == 'UNKNOWN' else
                  (f'Баллы по заданной рубрике: {score["value"]} из 1000.' if locale == 0 else
                   f'Бали за заданою рубрикою: {score["value"]} із 1000.'))
    reasons = [_BASE[locale], score_line] + gaps
    if not diagnostics:
        _need(result['eligibility']['state'] == 'ELIGIBLE_FOR_CREATIVE')
        reasons.append(_ABSENCE[locale]); actions = [_CONTINUE[locale]]
    return _card(locale, _SUMMARIES[result['eligibility']['state']][locale], reasons, gaps, actions)


def project_evaluation(evaluation_inputs=None, evaluation_result=None, display_locale=None):
    """Return the approved private Card or locale-less AdmissionFailure.

    Only existing evaluator defaults may be omitted from the invocation frame.
    Malformed inputs, mismatched results and runtime exceptions fail closed without
    echoing private values. Every otherwise admissible call recomputes the real
    evaluator; no result cache or caller-controlled verified flag exists.
    """
    if type(display_locale) is not str or display_locale not in ('ru', 'uk'):
        return {'availability': 'UNAVAILABLE'}
    locale = 0 if display_locale == 'ru' else 1
    try:
        _need(type(evaluation_inputs) is dict and type(evaluation_result) is dict)
        _need(_plain(evaluation_inputs) and _plain(evaluation_result))
        _need(_REQUIRED <= set(evaluation_inputs)
              and set(evaluation_inputs) <= _REQUIRED | _OPTIONAL)
        inputs, supplied = deepcopy(evaluation_inputs), deepcopy(evaluation_result)
        # PD-01: no digest-only or trusted-handoff alternative. Inputs remain exact;
        # evaluate_si itself applies its two existing optional None defaults.
        actual = _evaluate(**inputs)
        _need(_plain(actual))
        _need(canonical_si_json(supplied) == canonical_si_json(actual))
        return _render(supplied, inputs, locale)
    except Exception:
        # No private exception text, refs, paths or logs on the rejection path.
        return _unavailable(locale)
