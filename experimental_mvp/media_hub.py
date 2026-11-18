"""Manual-first media accounts and quota planning. This module never sends generation requests."""
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from experimental_mvp.storyboard import fingerprint

CATALOG = Path(__file__).with_name('providers.json')


def catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))['providers']


def utc(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Требуется timezone в дате.')
    return parsed.astimezone(timezone.utc)


def account_state(account):
    # A self-reported login is not a verified session / usable API connection.
    return 'MANUAL_ACCOUNT_REPORTED' if account.get('login_reported') else 'REQUIRES_LOGIN'


def quota(account, now):
    try:
        confirmed = utc(account['confirmed_at'])
        expires = utc(account['valid_until'])
        balance = account['balance']
        cost = account['cost_per_clip']
        if type(balance) not in (int, float) or type(cost) not in (int, float):
            return None
        if not math.isfinite(balance) or not math.isfinite(cost) or balance < 0 or cost <= 0:
            return None
        if not account.get('source') or not account.get('unit') or not confirmed <= now < expires:
            return None
        # Reset never automatically refills a balance, even if the day changed.
        if account.get('reset_at') and now >= utc(account['reset_at']):
            return None
        return balance, cost
    except (KeyError, TypeError, ValueError, OverflowError):
        return None


def plan(project, providers=None, now=None):
    providers = providers if providers is not None else catalog()
    by_id = {p['id']: p for p in providers}
    accounts = project.get('media_accounts', {})
    now = now or datetime.now(timezone.utc)
    budgets, queue = {}, []
    anchors = [a for scene in project.get('scenes', []) for a in scene.get('anchors', [])]
    for a in sorted(anchors, key=lambda a: -a.get('priority', 0)):
        key = fingerprint(a)
        item = dict(anchor_id=a['anchor_id'], fingerprint=key, provider=a.get('preferred_provider', ''),
                    fallback=a.get('fallback_mode', 'NONE'), status='PLANNED', reason='',
                    estimated_cost=None, reuse=False)
        need = 'video' if a.get('generation_mode') == 'AI_VIDEO' else 'image'
        item['candidates'] = [dict(provider=p['id'], duration_match=(
            'NOT_APPLICABLE' if need == 'image' else
            'CONFIRMED' if isinstance(p.get('video_durations_seconds'), list) and a['duration_ms']/1000 in p['video_durations_seconds'] else 'UNKNOWN'))
            for p in providers if need in p.get('kinds', [])]
        if a.get('local_asset_path'):
            from hashlib import sha256
            path = Path(a['local_asset_path'])
            if not path.is_file() or (a.get('asset_sha256') and sha256(path.read_bytes()).hexdigest() != a['asset_sha256']):
                item.update(status='FAILED', reason='Материал отсутствует / изменён; восстановите импорт')
            else:
                same = a.get('provenance', {}).get('prompt_fingerprint') == key
                item.update(status='IMPORTED', reuse=True,
                            reason='Материал сохранён' + ('' if same else '; промпт изменён — решите, нужен ли новый'))
        elif a.get('generation_mode') not in ('AI_VIDEO', 'AI_IMAGE'):
            item.update(status='SKIPPED', reason='Локальный материал / ручная графика / fallback')
        else:
            p = by_id.get(item['provider'])
            account = accounts.get(item['provider'], {})
            mode = a['generation_mode']
            need = 'video' if mode == 'AI_VIDEO' else 'image'
            if p is None or need not in p.get('kinds', []):
                item.update(status='WAITING_FOR_USER', reason='Выберите подходящий официальный сервис')
            elif not account.get('login_reported'):
                item.update(status='WAITING_FOR_USER', reason='Нет подтверждённого пользователем аккаунта; вход необязателен')
            else:
                durations = account.get('durations_seconds', p.get('video_durations_seconds'))
                if need == 'video' and (not isinstance(durations, list) or a['duration_ms']/1000 not in durations):
                    item.update(status='WAITING_FOR_USER', reason='Длительность не подтверждена; укоротите якорь или используйте fallback')
                else:
                    q = quota(account, now)
                    if q is None:
                        item.update(status='WAITING_FOR_QUOTA', reason='UNKNOWN / устаревшая квота; проверьте аккаунт')
                    else:
                        balance, cost = q
                        budget = budgets.setdefault(p['id'], balance)
                        item['estimated_cost'] = cost
                        if budget < cost:
                            item.update(status='WAITING_FOR_QUOTA', reason='Недостаточно квоты с учётом очереди')
                        else:
                            budgets[p['id']] -= cost
                            item.update(status='READY', reason='Только ручная генерация на официальном сайте; запрос не отправлен')
        queue.append(item)
    return {'jobs': queue, 'ready_clips': sum(j['status'] == 'READY' for j in queue),
            'reused_assets': sum(j['reuse'] for j in queue), 'remaining_planned_balance': budgets,
            'execution': 'MANUAL_ONLY_NO_CREDITS_SPENT'}
