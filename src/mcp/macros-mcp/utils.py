from __future__ import annotations

def round2(value: float) -> float:
    try:
        return round(float(value), 2)
    except Exception:  # noqa: BLE001
        return 0.0


def clamp_non_negative(value: float) -> float:
    try:
        v = float(value)
        return v if v >= 0 else 0.0
    except Exception:  # noqa: BLE001
        return 0.0


