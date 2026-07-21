"""艾略特波浪理论信号引擎。

通过 Zigzag 检测 Swing 点，匹配 5 浪推动和 3 浪调整结构，
结合 Fibonacci 浪间关系验证，生成趋势见顶/调整结束信号。
纯 pandas/numpy 实现，无外部波浪库依赖。
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


class SignalEngine:
    """艾略特波浪理论信号引擎。

    检测流程：
    1. Zigzag Swing 点检测（滚动窗口局部极值）
    2. 5 浪推动结构匹配 + 三大铁律验证
    3. ABC 调整结构匹配
    4. Fibonacci 浪间关系过滤

    策略：宁可漏信号也不误判。

    Attributes:
        swing_window: Swing 点检测滚动窗口半径。
        fib_tolerance: Fibonacci 比率容差。
        min_wave_bars: 每浪最少 K 线数。

    Example:
        >>> engine = SignalEngine()
        >>> signals = engine.generate({"BTC-USDT": df})
        >>> signals["BTC-USDT"].value_counts()
    """

    def __init__(
        self,
        swing_window: int = 10,
        fib_tolerance: float = 0.15,
        min_wave_bars: int = 5,
    ):
        """初始化艾略特波浪信号引擎。

        Args:
            swing_window: Swing 点检测滚动窗口半径，默认 10。
            fib_tolerance: Fibonacci 比率容差，默认 0.15。
            min_wave_bars: 每浪最少 K 线数，默认 5。
        """
        if (
            not isinstance(swing_window, int)
            or isinstance(swing_window, bool)
            or swing_window < 1
        ):
            raise ValueError("swing_window must be a positive integer")
        if (
            not isinstance(min_wave_bars, int)
            or isinstance(min_wave_bars, bool)
            or min_wave_bars < 1
        ):
            raise ValueError("min_wave_bars must be a positive integer")
        if not 0 <= fib_tolerance < 1:
            raise ValueError("fib_tolerance must be in the range [0, 1)")

        self.swing_window = swing_window
        self.fib_tolerance = fib_tolerance
        self.min_wave_bars = min_wave_bars

    def _find_swings(
        self, high: pd.Series, low: pd.Series
    ) -> List[Dict]:
        """用滚动窗口找局部高低点，生成交替的 Zigzag 序列。

        Args:
            high: 最高价序列。
            low: 最低价序列。

        Returns:
            交替排列的 Swing 点列表，每个元素为
            {"index": datetime, "price": float, "type": "H"|"L"}。
        """
        w = self.swing_window
        full_w = w * 2 + 1

        if len(high) < full_w:
            return []

        # Confirm a pivot only after ``w`` completed bars have closed to its right.
        # ``index`` remains the actual pivot time for measurement and charting;
        # ``confirmed_index`` is the first time the pivot is knowable and therefore
        # the earliest timestamp at which a signal may be emitted.
        raw_points = []
        for pivot_pos in range(w, len(high) - w):
            left = pivot_pos - w
            right = pivot_pos + w + 1
            pivot_index = high.index[pivot_pos]
            confirmed_pos = pivot_pos + w
            confirmed_index = high.index[confirmed_pos]
            pivot_high = high.iloc[pivot_pos]
            pivot_low = low.iloc[pivot_pos]
            is_h = bool(pd.notna(pivot_high) and pivot_high == high.iloc[left:right].max())
            is_l = bool(pd.notna(pivot_low) and pivot_low == low.iloc[left:right].min())
            if is_h and is_l:
                # An outside/constant bar is ambiguous without a tie-break rule.
                # Exclude it rather than silently assigning an arbitrary direction.
                continue
            elif is_h:
                raw_points.append(
                    {
                        "index": pivot_index,
                        "confirmed_index": confirmed_index,
                        "bar_pos": pivot_pos,
                        "confirmed_bar_pos": confirmed_pos,
                        "price": float(pivot_high),
                        "type": "H",
                    }
                )
            elif is_l:
                raw_points.append(
                    {
                        "index": pivot_index,
                        "confirmed_index": confirmed_index,
                        "bar_pos": pivot_pos,
                        "confirmed_bar_pos": confirmed_pos,
                        "price": float(pivot_low),
                        "type": "L",
                    }
                )

        if len(raw_points) < 2:
            return raw_points

        # 过滤为严格交替的 H/L 序列
        zigzag = [raw_points[0]]
        for pt in raw_points[1:]:
            if pt["type"] == zigzag[-1]["type"]:
                # Keep the first confirmed point. Replacing it with a later,
                # more-extreme point would rewrite historical counts when the
                # engine is recomputed with additional future data.
                continue
            else:
                zigzag.append(pt)

        return zigzag

    def _check_fib_ratios(
        self, w1: float, w2: float, w3: float, w4: float, w5: float
    ) -> bool:
        """验证 5 浪推动结构的 Fibonacci 浪间关系。

        检查项：
        - 浪2 回撤浪1 的 0.5-0.618
        - 浪3/浪1 在 1.0-2.618 范围
        - 浪4 回撤浪3 的 0.236-0.5

        Args:
            w1: 浪1 幅度（绝对值）。
            w2: 浪2 回撤幅度（绝对值）。
            w3: 浪3 幅度（绝对值）。
            w4: 浪4 回撤幅度（绝对值）。
            w5: 浪5 幅度（绝对值）。

        Returns:
            是否满足 Fibonacci 比率要求。
        """
        tol = self.fib_tolerance

        if w1 == 0 or w3 == 0:
            return False

        # 浪2 回撤浪1：目标 0.5-0.618
        r2 = w2 / w1
        if not (0.5 - tol <= r2 <= 0.618 + tol):
            return False

        # 浪3 / 浪1：目标 ~1.618，放宽到 1.0-2.618
        r3 = w3 / w1
        if not (1.0 - tol <= r3 <= 2.618 + tol):
            return False

        # 浪4 回撤浪3：目标 ~0.382，放宽到 0.236-0.5
        r4 = w4 / w3
        if not (0.236 - tol <= r4 <= 0.5 + tol):
            return False

        return True

    def _check_min_bars(self, swings: List[Dict], start: int, count: int) -> bool:
        """检查连续 Swing 点之间是否满足最少 K 线数。

        Args:
            swings: Swing 点列表。
            start: 起始索引。
            count: 检查的点数。

        Returns:
            是否每段都满足最少 K 线数。
        """
        for i in range(start, start + count - 1):
            pos_a = swings[i].get("bar_pos")
            pos_b = swings[i + 1].get("bar_pos")
            if pos_a is None or pos_b is None:
                raise ValueError("swing points must include bar_pos")
            diff = abs(int(pos_b) - int(pos_a))
            if diff < self.min_wave_bars:
                return False
        return True

    def _find_impulse(self, swings: List[Dict]) -> List[Tuple]:
        """在 Swing 序列中寻找 5 浪推动结构。

        看涨推动浪：L-H-L-H-L-H（6个点，5段浪）
        看跌推动浪：H-L-H-L-H-L（6个点，5段浪）

        三大铁律验证：
        1. 浪2 不破浪1 起点
        2. 浪3 不是最短推动浪
        3. 浪4 不进入浪1 区域

        Args:
            swings: 交替排列的 Swing 点列表。

        Returns:
            (结束时间戳, 信号方向) 元组列表。
            5 浪上升完成返回 -1（卖），5 浪下跌完成返回 1（买）。
        """
        results = []

        for i in range(len(swings) - 5):
            types = [s["type"] for s in swings[i : i + 6]]

            # --- 看涨推动浪: L, H, L, H, L, H ---
            if types == ["L", "H", "L", "H", "L", "H"]:
                x, p1, p2, p3, p4, p5 = swings[i : i + 6]

                wave1 = p1["price"] - x["price"]     # 上升
                wave2 = p1["price"] - p2["price"]     # 回撤（正值）
                wave3 = p3["price"] - p2["price"]     # 上升
                wave4 = p3["price"] - p4["price"]     # 回撤（正值）
                wave5 = p5["price"] - p4["price"]     # 上升

                if wave1 <= 0 or wave3 <= 0 or wave5 <= 0:
                    continue

                # 铁律1：浪2不破浪1起点
                if p2["price"] <= x["price"]:
                    continue

                # 铁律2：浪3不是最短推动浪
                if wave3 < wave1 and wave3 < wave5:
                    continue

                # 铁律3：浪4不进入浪1区域
                if p4["price"] <= p1["price"]:
                    continue

                # 最少K线数检查
                if not self._check_min_bars(swings, i, 6):
                    continue

                # Fibonacci 验证
                if not self._check_fib_ratios(wave1, wave2, wave3, wave4, wave5):
                    continue

                # 5浪上升完成 → 卖出信号
                results.append((p5["confirmed_index"], -1))

            # --- 看跌推动浪: H, L, H, L, H, L ---
            elif types == ["H", "L", "H", "L", "H", "L"]:
                x, p1, p2, p3, p4, p5 = swings[i : i + 6]

                wave1 = x["price"] - p1["price"]     # 下跌
                wave2 = p2["price"] - p1["price"]     # 反弹（正值）
                wave3 = p2["price"] - p3["price"]     # 下跌
                wave4 = p4["price"] - p3["price"]     # 反弹（正值）
                wave5 = p4["price"] - p5["price"]     # 下跌

                if wave1 <= 0 or wave3 <= 0 or wave5 <= 0:
                    continue

                # 铁律1：浪2不超过浪1起点
                if p2["price"] >= x["price"]:
                    continue

                # 铁律2：浪3不是最短推动浪
                if wave3 < wave1 and wave3 < wave5:
                    continue

                # 铁律3：浪4不进入浪1区域
                if p4["price"] >= p1["price"]:
                    continue

                # 最少K线数检查
                if not self._check_min_bars(swings, i, 6):
                    continue

                # Fibonacci 验证
                if not self._check_fib_ratios(wave1, wave2, wave3, wave4, wave5):
                    continue

                # 5浪下跌完成 → 买入信号
                results.append((p5["confirmed_index"], 1))

        return results

    def _find_abc(self, swings: List[Dict]) -> List[Tuple]:
        """在 Swing 序列中寻找 ABC 调整结构。

        看跌调整（上升趋势后）：H-L-H-L（A 下 B 反弹 C 下）
        看涨调整（下降趋势后）：L-H-L-H（A 上 B 回落 C 上）

        Args:
            swings: 交替排列的 Swing 点列表。

        Returns:
            (结束时间戳, 信号方向) 元组列表。
            ABC 下调完成返回 1（买），ABC 上调完成返回 -1（卖）。
        """
        tol = self.fib_tolerance
        results = []

        for i in range(len(swings) - 3):
            types = [s["type"] for s in swings[i : i + 4]]

            # --- 看跌 ABC: H, L, H, L（下-上-下）→ 调整结束后买入 ---
            if types == ["H", "L", "H", "L"]:
                start, pa, pb, pc = swings[i : i + 4]

                wave_a = start["price"] - pa["price"]   # A 下跌幅度
                wave_b = pb["price"] - pa["price"]       # B 反弹幅度
                wave_c = pb["price"] - pc["price"]       # C 下跌幅度

                if wave_a <= 0 or wave_b <= 0 or wave_c <= 0:
                    continue

                # B 不超过起点
                if pb["price"] >= start["price"]:
                    continue

                # B 回撤 A 的 0.382-0.618
                r_b = wave_b / wave_a
                if not (0.382 - tol <= r_b <= 0.618 + tol):
                    continue

                # C ≈ A（0.618-1.618 倍 A 浪）
                r_c = wave_c / wave_a
                if not (0.618 - tol <= r_c <= 1.618 + tol):
                    continue

                # 最少K线数检查
                if not self._check_min_bars(swings, i, 4):
                    continue

                # ABC 下调完成 → 买入信号
                results.append((pc["confirmed_index"], 1))

            # --- 看涨 ABC: L, H, L, H（上-下-上）→ 调整结束后卖出 ---
            elif types == ["L", "H", "L", "H"]:
                start, pa, pb, pc = swings[i : i + 4]

                wave_a = pa["price"] - start["price"]   # A 上涨幅度
                wave_b = pa["price"] - pb["price"]       # B 回落幅度
                wave_c = pc["price"] - pb["price"]       # C 上涨幅度

                if wave_a <= 0 or wave_b <= 0 or wave_c <= 0:
                    continue

                # B 不低于起点
                if pb["price"] <= start["price"]:
                    continue

                # B 回撤 A 的 0.382-0.618
                r_b = wave_b / wave_a
                if not (0.382 - tol <= r_b <= 0.618 + tol):
                    continue

                # C ≈ A
                r_c = wave_c / wave_a
                if not (0.618 - tol <= r_c <= 1.618 + tol):
                    continue

                # 最少K线数检查
                if not self._check_min_bars(swings, i, 4):
                    continue

                # ABC 上调完成 → 卖出信号
                results.append((pc["confirmed_index"], -1))

        return results

    def generate(
        self, data_map: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.Series]:
        """根据艾略特波浪理论生成交易信号。

        Args:
            data_map: 标的代码到 OHLCV DataFrame 的映射。
                DataFrame 需包含 high/low/close 列，index 为 datetime。

        Returns:
            标的代码到信号 Series 的映射（1=做多, -1=做空, 0=观望）。
        """
        result = {}

        for code, df in data_map.items():
            signal = pd.Series(0, index=df.index, dtype=int)

            swings = self._find_swings(df["high"], df["low"])
            if len(swings) < 4:
                result[code] = signal
                continue

            # 5 浪推动结构
            if len(swings) >= 6:
                for idx, direction in self._find_impulse(swings):
                    if idx in signal.index:
                        signal[idx] = direction

            # ABC 调整结构
            for idx, direction in self._find_abc(swings):
                if idx in signal.index:
                    signal[idx] = direction

            result[code] = signal

        return result


def _fetch_okx(
    inst_id: str, bar: str = "1D", limit: int = 300
) -> pd.DataFrame:
    """从 OKX API 获取 K 线数据。

    Args:
        inst_id: 交易对标识，如 "BTC-USDT"。
        bar: K 线周期，默认 "1D"。
        limit: 获取数量，默认 300。

    Returns:
        OHLCV DataFrame，index 为 datetime。

    Raises:
        KeyError: API 返回格式异常时。
    """
    import requests

    resp = requests.get(
        "https://www.okx.com/api/v5/market/candles",
        params={"instId": inst_id, "bar": bar, "limit": str(limit)},
    )
    candles = resp.json()["data"]
    columns = [
        "ts", "open", "high", "low", "close",
        "vol", "volCcy", "volCcyQuote", "confirm",
    ]
    df = pd.DataFrame(reversed(candles), columns=columns)
    df["ts"] = pd.to_datetime(df["ts"].astype("int64"), unit="ms")
    df = df.set_index("ts")
    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)
    df["volume"] = df["vol"].astype(float)
    return df
