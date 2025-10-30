from datetime import datetime

def time_ago(dt):
    delta = datetime.now() - dt
    if delta.days > 0: return f"{delta.days}일 전"
    sec = delta.seconds
    if sec < 60: return f"{sec}초 전"
    if sec < 3600: return f"{sec//60}분 전"
    return f"{sec//3600}시간 전"
