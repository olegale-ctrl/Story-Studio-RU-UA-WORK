"""Local PREVIEW_ONLY editor adapter. No rendering, translation or authority."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.first_video import read_plan
from story_intelligence.evaluate_v1 import evaluate_si
from story_intelligence.decision_projection_v1 import project_evaluation

VERSION = "EditorPreviewInputV1"
LOCALES = ("ru", "uk")
FIELDS = {"schema_version", "purpose", "topic", "audience", "evaluation_inputs", "scene_drafts", "materials"}
REQUIRED_EVALUATION = {"records": list, "semantic_input_refs": list, "observed_context": dict,
                       "ratings": list, "expected_context": dict, "human_findings": dict}
OPTIONAL_EVALUATION = {"ui_locale", "required_current_premise"}
RIGHTS = {"UNKNOWN", "PENDING_REVIEW", "REPORTED_BY_EDITOR", "VERIFIED_EXTERNALLY"}
# Closed text catalog: no interpolation of user values, identifiers or exceptions.
TEXT = {
    "INPUT_MISSING": ("Не предоставлены сведения редактора.", "Не надано відомості редактора.", "Заполните указанный раздел.", "Заповніть зазначений розділ."),
    "INPUT_INVALID": ("Раздел имеет неподдерживаемую структуру.", "Розділ має непідтримувану структуру.", "Исправьте структуру по формату V1.", "Виправте структуру за форматом V1."),
    "JSON_INVALID": ("Входной JSON не принят.", "Вхідний JSON не прийнято.", "Проверьте UTF-8, уникальность ключей и допустимые значения.", "Перевірте UTF-8, унікальність ключів і допустимі значення."),
    "SCHEMA_UNSUPPORTED": ("Версия входного формата не поддерживается.", "Версія вхідного формату не підтримується.", "Используйте EditorPreviewInputV1.", "Використовуйте EditorPreviewInputV1."),
    "PURPOSE_UNSUPPORTED": ("Допустим только предварительный просмотр.", "Дозволено лише попередній перегляд.", "Укажите PREVIEW_ONLY.", "Зазначте PREVIEW_ONLY."),
    "EVALUATION_MISSING": ("Для оценки не хватает входных аргументов.", "Для оцінки бракує вхідних аргументів.", "Предоставьте полный набор SI-данных, ratings и findings; не заменяйте их заглушками.", "Надайте повний набір SI-даних, ratings і findings; не замінюйте їх заглушками."),
    "EVALUATION_INVALID": ("Evaluator отклонил некорректные данные; карточка не создана.", "Evaluator відхилив некоректні дані; картку не створено.", "Проверьте точные SI-ссылки, контекст и структуру данных.", "Перевірте точні SI-посилання, контекст і структуру даних."),
    "EVALUATION_STALE": ("Evaluator обнаружил устаревшие зависимости.", "Evaluator виявив застарілі залежності.", "Подготовьте актуальные данные и явно согласованный контекст; повторите оценку.", "Підготуйте актуальні дані та явно узгоджений контекст; повторіть оцінювання."),
    "EVALUATION_FAILED": ("Оценка не завершена.", "Оцінювання не завершено.", "Проверьте допустимость аргументов и повторите локальную проверку.", "Перевірте допустимість аргументів і повторіть локальну перевірку."),
    "PROJECTION_UNAVAILABLE": ("Приватная карточка недоступна.", "Приватна картка недоступна.", "Проверьте согласованность входов и результата оценки.", "Перевірте узгодженість входів і результату оцінювання."),
    "PLAN_INCOMPLETE": ("Черновик сцен неполон.", "Чернетка сцен неповна.", "Предоставьте точные тексты сцен для указанного языка; перевод не создаётся автоматически.", "Надайте точні тексти сцен зазначеною мовою; переклад не створюється автоматично."),
    "PLAN_INVALID": ("Черновик не соответствует формату плана.", "Чернетка не відповідає формату плану.", "Проверьте 1–20 сцен, непустые тексты до 2000 символов и имена изображений.", "Перевірте 1–20 сцен, непорожні тексти до 2000 символів і назви зображень."),
    "RIGHTS_UNKNOWN": ("Статус проверки прав неизвестен.", "Статус перевірки прав невідомий.", "Передайте материалы на отдельную проверку прав и способа использования.", "Передайте матеріали на окрему перевірку прав і способу використання."),
    "RIGHTS_UNREVIEWED": ("Проверка прав ожидается.", "Очікується перевірка прав.", "Завершите отдельную проверку перед будущей сборкой.", "Завершіть окрему перевірку перед майбутньою збіркою."),
    "RIGHTS_REPORTED": ("Сведения о правах сообщены редактором.", "Відомості про права повідомлено редактором.", "Отдельно проверьте подтверждения и допустимый способ использования.", "Окремо перевірте підтвердження та допустимий спосіб використання."),
    "RIGHTS_EXTERNAL_REPORT": ("Заявлена внешняя проверка прав; разрешение не предоставлено.", "Заявлено зовнішню перевірку прав; дозволу не надано.", "Проверьте внешние подтверждения и привязку к точным материалам.", "Перевірте зовнішні підтвердження та прив'язку до точних матеріалів."),
}
CHECKS = [
    ("Фактическая обоснованность утверждений и источников.", "Фактична обґрунтованість тверджень і джерел."),
    ("Редакционное утверждение точных RU/UK текстов.", "Редакційне затвердження точних RU/UK текстів."),
    ("Права на изображения, музыку, голос, аудио и другие материалы.", "Права на зображення, музику, голос, аудіо та інші матеріали."),
    ("Соответствие прав предполагаемому способу использования.", "Відповідність прав передбачуваному способу використання."),
    ("Разрешение на рендер через будущий Production Readiness.", "Дозвіл на рендер через майбутній Production Readiness."),
    ("Финальная привязка разрешений к неизменённым материалам.", "Остаточна прив'язка дозволів до незмінених матеріалів."),
]


def wire(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def bounded(value, depth=0):
    if depth > 64:
        raise ValueError("JSON_INVALID")
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError("JSON_INVALID")
            key.encode("utf-8")
            bounded(item, depth + 1)
    elif type(value) is list:
        for item in value:
            bounded(item, depth + 1)
    elif type(value) is str:
        value.encode("utf-8")
    elif value is not None and type(value) is not bool and not (type(value) is int and value.bit_length() <= 64):
        raise ValueError("JSON_INVALID")


def present_text(value, limit=4000):
    return type(value) is str and bool(value.strip()) and len(value) <= limit


def preview(data):
    """Return detached status/artifacts; never creates or repairs evaluator inputs."""
    diagnostics = []
    files = {}
    sections = {}
    status = dict(schema_version="EditorPreviewStatusV1", purpose="PREVIEW_ONLY",
                  adapter_state="NEEDS_INPUT", input_completeness="INCOMPLETE",
                  input_sha256=None, sections=sections, diagnostics=diagnostics,
                  evaluation={"state": "NOT_RUN", "reason": "EVALUATION_MISSING"},
                  cards={l: {"state": "NOT_CREATED", "reason": "EVALUATION_MISSING"} for l in LOCALES},
                  plans={l: {"state": "MISSING", "reason": "PLAN_INCOMPLETE"} for l in LOCALES},
                  materials_summary=[],
                  production_readiness=dict(state="NOT_ASSESSED", permissions_granted=False,
                      future_checks=[dict(ru=a, uk=b) for a, b in CHECKS]))

    def note(code, section, locale=None, index=None):
        a, b, c, d = TEXT[code]
        item = dict(code=code, section=section, message=dict(ru=a, uk=b), next_action=dict(ru=c, uk=d))
        if locale is not None:
            item["locale"] = locale
        if index is not None:
            item["index"] = index
        diagnostics.append(item)

    try:
        bounded(data)
        if len(wire(data)) > 2_000_000:
            raise ValueError("JSON_INVALID")
        status["input_sha256"] = sha256(wire(data)).hexdigest()
    except (ValueError, UnicodeError, RecursionError):
        note("JSON_INVALID", "input")
        status["input_completeness"] = "INVALID"
        return status, files
    if type(data) is not dict or set(data) - FIELDS:
        note("INPUT_INVALID", "input")
        status["input_completeness"] = "INVALID"
        return status, files
    if data.get("schema_version") != VERSION or data.get("purpose") != "PREVIEW_ONLY":
        code = "SCHEMA_UNSUPPORTED" if data.get("schema_version") != VERSION else "PURPOSE_UNSUPPORTED"
        note(code, "input")
        status["input_completeness"] = "INVALID"
        return status, files

    for name, fields, checks in [
        ("topic", {"id", "text", "source_locale"}, lambda v: present_text(v.get("id"), 200) and present_text(v.get("text"), 2000) and v.get("source_locale") in LOCALES),
        ("audience", {"description"}, lambda v: present_text(v.get("description"))),
    ]:
        value = data.get(name)
        good = type(value) is dict and not set(value) - fields and checks(value)
        sections[name] = "COMPLETE" if good else "INCOMPLETE" if value is None else "INVALID"
        if not good:
            note("INPUT_MISSING" if value is None else "INPUT_INVALID", name)

    inputs = data.get("evaluation_inputs")
    sections["evaluation_inputs"] = "COMPLETE"
    if inputs is None:
        sections["evaluation_inputs"] = "INCOMPLETE"
        note("EVALUATION_MISSING", "evaluation_inputs")
    elif type(inputs) is not dict or set(inputs) - REQUIRED_EVALUATION.keys() - OPTIONAL_EVALUATION:
        sections["evaluation_inputs"] = "INVALID"
        note("INPUT_INVALID", "evaluation_inputs")
    else:
        for key, kind in REQUIRED_EVALUATION.items():
            if inputs.get(key) is None:
                sections["evaluation_inputs"] = "INCOMPLETE"
                note("EVALUATION_MISSING", key)
            elif type(inputs[key]) is not kind:
                sections["evaluation_inputs"] = "INVALID"
                note("INPUT_INVALID", key)
        if sections["evaluation_inputs"] == "COMPLETE":
            try:
                result = evaluate_si(**deepcopy(inputs))
                state = result["status"]
                if state not in ("OK", "INVALID", "STALE"):
                    raise ValueError("EVALUATION_FAILED")
                # SI diagnostic paths can contain keys supplied by the editor.
                # Only the in-memory result is passed to Projection for verification.
                files["evaluation.json"] = {
                    **result,
                    "diagnostics": [{"code": item["code"]} for item in result["diagnostics"]],
                }
                status["evaluation"] = dict(state=state, file="evaluation.json")
                if state == "OK":
                    status["evaluation"]["eligibility"] = result["eligibility"]["state"]
                else:
                    note("EVALUATION_" + state, "evaluation_inputs")
                for locale in LOCALES:
                    if state == "INVALID":
                        status["cards"][locale] = dict(state="NOT_CREATED", reason="EVALUATION_INVALID")
                        continue
                    try:
                        card = project_evaluation(inputs, result, locale)
                    except Exception:
                        card = {"availability": "UNAVAILABLE"}
                    if type(card) is dict and card.get("availability") == "DISPLAYABLE":
                        filename = f"private-card-{locale}.json"
                        files[filename] = card
                        status["cards"][locale] = dict(state="DISPLAYABLE", file=filename)
                    else:
                        status["cards"][locale] = dict(state="UNAVAILABLE", reason="PROJECTION_UNAVAILABLE")
                        note("PROJECTION_UNAVAILABLE", "cards", locale)
            except Exception:
                files.pop("evaluation.json", None)
                status["evaluation"] = dict(state="FAILED", reason="EVALUATION_FAILED")
                note("EVALUATION_FAILED", "evaluation_inputs")

    drafts = data.get("scene_drafts")
    sections["scene_drafts"] = "COMPLETE"
    if drafts is not None and (type(drafts) is not dict or set(drafts) - set(LOCALES)):
        sections["scene_drafts"] = "INVALID"
        note("INPUT_INVALID", "scene_drafts")
        drafts = {}
    for locale in LOCALES:
        draft = drafts.get(locale) if type(drafts) is dict else None
        if draft is None:
            sections["scene_drafts"] = "INCOMPLETE"
            note("PLAN_INCOMPLETE", "scene_drafts", locale)
            continue
        shape = type(draft) is dict and not set(draft) - {"title", "scenes"}
        shape = shape and (draft.get("title") is None or type(draft["title"]) is str)
        scenes = draft.get("scenes") if shape else None
        shape = shape and (scenes is None or (type(scenes) is list and len(scenes) <= 20 and all(
            type(s) is dict and not set(s) - {"text", "image"} and
            all(s.get(k) is None or type(s[k]) is str for k in s) for s in scenes)))
        if not shape:
            sections["scene_drafts"] = "INVALID"
            status["plans"][locale] = dict(state="INVALID", reason="PLAN_INVALID")
            note("PLAN_INVALID", "scene_drafts", locale)
            continue
        complete = bool(scenes) and all(present_text(s.get("text"), 2000) and
            ("image" not in s or (present_text(s["image"], 255) and not any(c in s["image"] for c in ("/", "\\", ":")) and s["image"] not in (".", ".."))) for s in scenes)
        if complete:
            filename = f"plan-{locale}.json"
            plan = dict(locale=locale, scenes=deepcopy(scenes))
            if draft.get("title") is not None:
                plan["title"] = draft["title"]
            files[filename] = plan
            status["plans"][locale] = dict(state="DRAFT_PLAN_VALID", file=filename)
        else:
            filename = f"draft-{locale}.json"
            files[filename] = deepcopy(draft)
            status["plans"][locale] = dict(state="PARTIAL", file=filename, reason="PLAN_INCOMPLETE")
            sections["scene_drafts"] = "INCOMPLETE"
            note("PLAN_INCOMPLETE", "scene_drafts", locale)

    materials = data.get("materials")
    sections["materials"] = "COMPLETE"
    if type(materials) is not list:
        sections["materials"] = "INCOMPLETE" if materials is None else "INVALID"
        note("INPUT_MISSING" if materials is None else "INPUT_INVALID", "materials")
    else:
        for index, material in enumerate(materials, 1):
            valid = type(material) is dict and not set(material) - {"id", "description", "kind", "rights_status"}
            valid = valid and all(present_text(material.get(k)) for k in ("id", "description", "kind"))
            right = material.get("rights_status") if type(material) is dict else None
            status["materials_summary"].append(dict(index=index,
                reported_status=right if type(right) is str and right in RIGHTS else "UNKNOWN",
                grants_permission=False))
            if not valid:
                sections["materials"] = "INVALID"
                note("INPUT_INVALID", "materials", index=index)
            if type(right) is not str or right not in RIGHTS:
                sections["materials"] = "INCOMPLETE"
                note("RIGHTS_UNKNOWN", "materials", index=index)
            else:
                note({"UNKNOWN": "RIGHTS_UNKNOWN", "PENDING_REVIEW": "RIGHTS_UNREVIEWED",
                      "REPORTED_BY_EDITOR": "RIGHTS_REPORTED", "VERIFIED_EXTERNALLY": "RIGHTS_EXTERNAL_REPORT"}[right], "materials", index=index)
    # Preserve invalidity when another missing field in the same section was seen later.
    for diagnostic in diagnostics:
        if diagnostic["code"] in ("INPUT_INVALID", "PLAN_INVALID"):
            section = diagnostic["section"]
            sections["evaluation_inputs" if section in REQUIRED_EVALUATION else section] = "INVALID"
    status["input_completeness"] = "INVALID" if "INVALID" in sections.values() else "INCOMPLETE" if "INCOMPLETE" in sections.values() else "COMPLETE"
    if status["input_completeness"] == "COMPLETE":
        status["adapter_state"] = "INPUT_COMPLETE"
    return status, files


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("JSON_INVALID")
        result[key] = value
    return result


def reject_number(value):
    raise ValueError("JSON_INVALID")


def write_json(path, value):
    data = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
        stream.write(data)


def run(source, output):
    """Write a fresh private preview directory; never reuse earlier artifacts."""
    if output.exists() or output.is_symlink():
        raise FileExistsError("OUTPUT_EXISTS")
    raw = None
    invalid_json = False
    try:
        with source.open("rb") as stream:
            raw = stream.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("JSON_INVALID")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=reject_number, parse_constant=reject_number)
        bounded(data)
    except (ValueError, UnicodeError, RecursionError):
        data = None
        invalid_json = True
    status, files = preview(data)
    if invalid_json:
        status["input_sha256"] = None
        a, b, c, d = TEXT["JSON_INVALID"]
        status["diagnostics"] = [dict(code="JSON_INVALID", section="input",
            message=dict(ru=a, uk=b), next_action=dict(ru=c, uk=d))]
    if raw is not None and len(raw) <= 2_000_000:
        status["source_sha256"] = sha256(raw).hexdigest()
    output = output.absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".editor-preview-", dir=output.parent) as temp:
        stage = Path(temp) / "preview"
        stage.mkdir(mode=0o700)
        for filename, value in files.items():
            path = stage / filename
            write_json(path, value)
            if filename.startswith("plan-"):
                read_plan(path)
        write_json(stage / "preview-status.json", status)
        if output.exists() or output.is_symlink():
            raise FileExistsError("OUTPUT_EXISTS")
        stage.rename(output)
    return status


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("editor_input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        status = run(args.editor_input, args.output_dir)
    except (OSError, ValueError, TypeError):
        print("EDITOR_PREVIEW_IO_FAILED", file=sys.stderr)
        return 2
    print(status["adapter_state"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
