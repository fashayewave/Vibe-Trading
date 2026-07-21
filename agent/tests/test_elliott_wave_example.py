from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

from backtest.runner import _load_module_from_file, _validate_signal_engine_class


_AGENT_ROOT = Path(__file__).resolve().parents[1]
_EXAMPLE_PATH = _AGENT_ROOT / "src" / "skills" / "elliott-wave" / "example_signal_engine.py"


def _load_example_module():
    spec = importlib.util.spec_from_file_location("elliott_wave_example", _EXAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_example_passes_protected_backtest_runner_validation() -> None:
    module = _load_module_from_file(_EXAMPLE_PATH, "elliott_wave_runner_example")

    _validate_signal_engine_class(module.SignalEngine)


def test_swings_are_emitted_only_at_confirmation_and_do_not_repaint() -> None:
    module = _load_example_module()
    engine = module.SignalEngine(swing_window=2, min_wave_bars=1)
    index = pd.RangeIndex(13)
    high = pd.Series([1, 2, 5, 2, 1, 2, 4, 2, 1, 2, 6, 2, 1], index=index, dtype=float)
    low = high - 0.5

    full = engine._find_swings(high, low)

    assert full[0]["index"] == 2
    assert full[0]["confirmed_index"] == 4
    assert engine._find_swings(high.iloc[:3], low.iloc[:3]) == []

    for stop in range(5, len(high) + 1):
        expected = [point for point in full if point["confirmed_bar_pos"] < stop]
        actual = engine._find_swings(high.iloc[:stop], low.iloc[:stop])
        assert actual == expected


def test_min_wave_bars_uses_bar_positions_for_intraday_data() -> None:
    module = _load_example_module()
    engine = module.SignalEngine(min_wave_bars=5)
    timestamps = pd.date_range("2026-01-01", periods=4, freq="10h")
    swings = [
        {
            "index": timestamp,
            "confirmed_index": timestamp,
            "bar_pos": position * 5,
            "confirmed_bar_pos": position * 5,
            "price": float(position),
            "type": "H" if position % 2 == 0 else "L",
        }
        for position, timestamp in enumerate(timestamps)
    ]

    assert engine._check_min_bars(swings, 0, 4)


def test_impulse_signal_uses_last_pivot_confirmation_time() -> None:
    module = _load_example_module()
    engine = module.SignalEngine(swing_window=2, min_wave_bars=5)
    dates = pd.date_range("2026-01-01", periods=40, freq="h")
    prices = [100.0, 110.0, 105.0, 121.0, 115.0, 125.0]
    types = ["L", "H", "L", "H", "L", "H"]
    positions = [0, 5, 10, 15, 20, 25]
    swings = [
        {
            "index": dates[position],
            "confirmed_index": dates[position + 2],
            "bar_pos": position,
            "confirmed_bar_pos": position + 2,
            "price": price,
            "type": swing_type,
        }
        for position, price, swing_type in zip(positions, prices, types)
    ]

    assert engine._find_impulse(swings) == [(dates[27], -1)]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"swing_window": 0}, "swing_window"),
        ({"min_wave_bars": 0}, "min_wave_bars"),
        ({"fib_tolerance": 1.0}, "fib_tolerance"),
    ],
)
def test_invalid_parameters_are_rejected(kwargs: dict, message: str) -> None:
    module = _load_example_module()

    with pytest.raises(ValueError, match=message):
        module.SignalEngine(**kwargs)
