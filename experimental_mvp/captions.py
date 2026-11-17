"""Scene-relative captions shared by preview and final export."""


class CueError(ValueError):
    def __init__(self, scene, index, reason):
        self.index = index
        super().__init__(f"Сцена {scene}, реплика {index + 1}: {reason}")


def calculated(text, length):
    chunks = []
    line = ""
    for word in text.split():
        if line and len(line) + len(word) + 1 > 64:
            chunks.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        chunks.append(line)
    return [
        {"start_ms": length * i // len(chunks),
         "end_ms": length * (i + 1) // len(chunks), "text": chunk}
        for i, chunk in enumerate(chunks)
        if length * (i + 1) // len(chunks) > length * i // len(chunks)
    ]


def validate(rows, length, scene):
    if not isinstance(rows, list) or not rows:
        raise CueError(scene, 0, "нужна хотя бы одна реплика.")
    previous = 0
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise CueError(scene, i, "неверный формат реплики.")
        a, b, text = row.get("start_ms"), row.get("end_ms"), row.get("text")
        if type(a) is not int or type(b) is not int or not 0 <= a < b <= length:
            raise CueError(scene, i, f"нужно 0 ≤ начало < конец ≤ {length} мс.")
        if a < previous:
            raise CueError(scene, i, "интервал пересекает предыдущую реплику.")
        if not isinstance(text, str) or not text.strip() or len(text.splitlines()) != 1:
            raise CueError(scene, i, "введите непустую строку текста.")
        previous = b
    return rows


def timestamp(ms):
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, ms = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def render_srt(scenes, spans, overrides):
    cues = []
    for number, (scene, (start, end)) in enumerate(zip(scenes, spans), 1):
        length = end - start
        rows = overrides.get(scene.get("id"), calculated(scene["text"], length))
        for row in validate(rows, length, number):
            a, b = (timestamp(start + row[key]) for key in ("start_ms", "end_ms"))
            text = row["text"].strip().translate(str.maketrans("<>{}", "‹›｛｝"))
            cues.append(f"{len(cues)+1}\n{a} --> {b}\n{text}\n")
    return "\n".join(cues)
