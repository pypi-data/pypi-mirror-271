r"""Implement an analyzer that generates a section to analyze the number
of null values."""

from __future__ import annotations

__all__ = ["NullValueAnalyzer"]

import logging
from typing import TYPE_CHECKING

import numpy as np

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import NullValueSection

if TYPE_CHECKING:
    from pandas import DataFrame

logger = logging.getLogger(__name__)


class NullValueAnalyzer(BaseAnalyzer):
    r"""Implement a null value analyzer.

    Args:
        figsize: The figure size in inches. The first
            dimension is the width and the second is the height.

    Example usage:

    ```pycon
    >>> import numpy as np
    >>> import pandas as pd
    >>> from flamme.analyzer import NullValueAnalyzer
    >>> analyzer = NullValueAnalyzer()
    >>> analyzer
    NullValueAnalyzer(figsize=None)
    >>> frame = pd.DataFrame(
    ...     {
    ...         "int": np.array([np.nan, 1, 0, 1]),
    ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
    ...         "str": np.array(["A", "B", None, np.nan]),
    ...     }
    ... )
    >>> section = analyzer.analyze(frame)

    ```
    """

    def __init__(self, figsize: tuple[float, float] | None = None) -> None:
        self._figsize = figsize

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(figsize={self._figsize})"

    def analyze(self, frame: DataFrame) -> NullValueSection:
        logger.info("Analyzing the null value distribution of all columns...")
        return NullValueSection(
            columns=list(frame.columns),
            null_count=frame.isna().sum().to_frame("count")["count"].to_numpy(),
            total_count=np.full((frame.shape[1],), frame.shape[0]),
            figsize=self._figsize,
        )
