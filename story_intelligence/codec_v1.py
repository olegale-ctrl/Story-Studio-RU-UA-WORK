"""SI/1 canonical JSON byte/hash primitives, not typed-record certification."""
import hashlib
import json

from .model_v1 import SIValidationError

__all__ = ['canonical_si_json', 'decode_canonical_si_json', 'canonical_si_sha256']
_MAX_BYTES = 1_000_000
_MAX_TEXT = 100_000
_MAX_DEPTH = 32


def _fail(code, path, message):
    raise SIValidationError(code, path, message)


def _string(value, path):
    if type(value) is not str:
        _fail('TYPE', path, 'Expected plain string')
    if len(value) > _MAX_TEXT:
        _fail('LIMIT', path, 'String exceeds 100000 codepoints')
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        _fail('TYPE', path, 'Surrogate forbidden')


def _decimal(number):
    # No str(huge_int) or global sys.set_int_max_str_digits mutation.
    negative = number < 0
    number = abs(number)
    chunks = []
    while number >= 1_000_000_000:
        number, remainder = divmod(number, 1_000_000_000)
        chunks.append(f'{remainder:09d}')
    return ('-' if negative else '') + str(number) + ''.join(reversed(chunks))


def canonical_si_json(value):
    """Return exact bounded UTF-8 C(value); reject coercion and all floats."""
    parts, size = [], 0

    def emit(text, path):
        nonlocal size
        data = text.encode('utf-8')
        size += len(data)
        if size > _MAX_BYTES:
            _fail('LIMIT', path, 'Canonical JSON exceeds 1000000 bytes')
        parts.append(data)

    def walk(v, path, depth):
        kind = type(v)
        if kind in (dict, list):
            if depth >= _MAX_DEPTH:
                _fail('LIMIT', path, 'Nesting exceeds 32 containers (including root)')
            if kind is dict:
                for key in v:
                    _string(key, path)
                emit('{', path)
                for i, key in enumerate(sorted(v)):
                    if i:
                        emit(',', path)
                    emit(json.dumps(key, ensure_ascii=False), path)
                    emit(':', path)
                    walk(v[key], f'{path}.{key}', depth + 1)
                emit('}', path)
            else:
                emit('[', path)
                for i, child in enumerate(v):
                    if i:
                        emit(',', path)
                    walk(child, f'{path}[{i}]', depth + 1)
                emit(']', path)
        elif kind is str:
            _string(v, path)
            emit(json.dumps(v, ensure_ascii=False), path)
        elif kind is int:
            # Cheap upper rejection before decimal expansion for impossible values.
            if v.bit_length() > _MAX_BYTES * 4:
                _fail('LIMIT', path, 'Integer exceeds byte budget')
            emit(_decimal(v), path)
        elif kind is bool:
            emit('true' if v else 'false', path)
        elif v is None:
            emit('null', path)
        else:
            _fail('TYPE', path, 'Only exact JSON types; floats/subclasses forbidden')
    walk(value, '$', 0)
    return b''.join(parts)


def _check_depth(text):
    quoted = escaped = False
    depth = 0
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            if depth > _MAX_DEPTH:
                _fail('LIMIT', '$', 'Nesting exceeds 32 containers')
        elif char in ']}':
            depth -= 1


class _Pairs(list):
    """Internal marker to preserve duplicate object keys until validation."""


def decode_canonical_si_json(data):
    """Decode canonical bytes only; never normalize noncanonical input."""
    if type(data) is not bytes:
        _fail('TYPE', '$', 'Expected plain bytes')
    if len(data) > _MAX_BYTES:
        _fail('LIMIT', '$', 'Input exceeds 1000000 bytes')
    try:
        text = data.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        _fail('TYPE', '$', 'Invalid UTF-8')
    _check_depth(text)

    def forbidden(_):
        _fail('TYPE', '$', 'Float/NaN/Infinity forbidden')

    def integer(s):
        negative = s.startswith('-')
        digits = s[1:] if negative else s
        number = 0
        for i in range(0, len(digits), 9):
            chunk = digits[i:i + 9]
            number = number * 10 ** len(chunk) + int(chunk)
        return -number if negative else number

    try:
        raw = json.loads(text, object_pairs_hook=_Pairs, parse_int=integer,
                         parse_float=forbidden, parse_constant=forbidden)
    except SIValidationError:
        raise
    except (ValueError, RecursionError):
        _fail('TYPE', '$', 'Malformed JSON')

    def unpack(v, path):
        if type(v) is _Pairs:
            result = {}
            for key, child in v:
                if key in result:
                    _fail('TYPE', f'{path}.{key}', 'Duplicate JSON key')
                result[key] = unpack(child, f'{path}.{key}')
            return result
        if type(v) is list:
            return [unpack(child, f'{path}[{i}]') for i, child in enumerate(v)]
        return v
    value = unpack(raw, '$')
    if canonical_si_json(value) != data:
        _fail('TYPE', '$', 'Noncanonical JSON bytes')
    return value


def canonical_si_sha256(value):
    """Lowercase SHA-256 of C(value); no truth/provenance/authority assertion."""
    return hashlib.sha256(canonical_si_json(value)).hexdigest()
