from datetime import datetime, timedelta


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def hm(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def exit_card_text(type_title: str, start_dt: datetime, planned_minutes, delayed: bool, remaining_seconds=None) -> str:
    lines = [f"{type_title}", f"Початок: {hm(start_dt)}"]
    if planned_minutes:
        lines.append(f"Ліміт: {planned_minutes} хв" + (" (з урахуванням затримки)" if delayed else ""))
    if remaining_seconds is not None:
        if remaining_seconds > 0:
            m, s = divmod(int(remaining_seconds), 60)
            lines.append(f"⏱ Залишилось: {m:02d}:{s:02d}")
        else:
            over = abs(int(remaining_seconds))
            m, s = divmod(over, 60)
            lines.append(f"⏱ Прострочено: {m:02d}:{s:02d}")
    if delayed:
        lines.append("⚠️ Позначено як «затримка»")
    return "\n".join(lines)
