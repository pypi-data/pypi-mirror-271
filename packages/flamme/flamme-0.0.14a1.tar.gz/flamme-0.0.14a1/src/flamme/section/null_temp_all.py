r"""Contain the implementation of sections to analyze the number null
values for all columns."""

from __future__ import annotations

__all__ = ["AllColumnsTemporalNullValueSection"]

import logging
from typing import TYPE_CHECKING

from coola.utils import str_indent
from jinja2 import Template
from matplotlib import pyplot as plt
from tqdm import tqdm

from flamme.section.base import BaseSection
from flamme.section.null_temp import plot_temporal_null_total
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)
from flamme.utils.figure import figure2html, readable_xticklabels

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np
    from pandas import DataFrame

logger = logging.getLogger(__name__)


class AllColumnsTemporalNullValueSection(BaseSection):
    r"""Implement a section to analyze the temporal distribution of null
    values for all columns.

    Args:
        frame: The DataFrame to analyze.
        dt_column: The datetime column used to analyze
            the temporal distribution.
        period: The temporal period e.g. monthly or daily.
        ncols: The number of columns.
        figsize: The figure size in inches. The first dimension
            is the width and the second is the height.
    """

    def __init__(
        self,
        frame: DataFrame,
        dt_column: str,
        period: str,
        ncols: int = 2,
        figsize: tuple[float, float] = (7, 5),
    ) -> None:
        self._frame = frame
        self._dt_column = dt_column
        self._period = period
        self._ncols = ncols
        self._figsize = figsize

    @property
    def frame(self) -> DataFrame:
        r"""``pandas.DataFrame``: The DataFrame to analyze."""
        return self._frame

    @property
    def dt_column(self) -> str:
        r"""The datetime column."""
        return self._dt_column

    @property
    def period(self) -> str:
        r"""The temporal period used to analyze the data."""
        return self._period

    @property
    def ncols(self) -> int:
        r"""int: The number of columns to show the figures."""
        return self._ncols

    @property
    def figsize(self) -> tuple[float, float] | None:
        r"""Tuple or ``None``: The individual figure size in pixels.

        The first dimension is the width and the second is the height.
        """
        return self._figsize

    def get_statistics(self) -> dict:
        return {}

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        logger.info(
            "Rendering the temporal null value distribution of all columns | "
            f"datetime column: {self._dt_column} | period: {self._period}"
        )
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "column": self._dt_column,
                "figure": create_temporal_null_figure(
                    frame=self._frame,
                    dt_column=self._dt_column,
                    period=self._period,
                    ncols=self._ncols,
                    figsize=self._figsize,
                ),
            }
        )

    def render_html_toc(
        self, number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
    ) -> str:
        return render_html_toc(number=number, tags=tags, depth=depth, max_depth=max_depth)

    def _create_template(self) -> str:
        return """
<h{{depth}} id="{{id}}">{{section}} {{title}} </h{{depth}}>

{{go_to_top}}

<p style="margin-top: 1rem;">
This section analyzes the monthly distribution of null values.
The column <em>{{column}}</em> is used as the temporal column.

{{figure}}

<p style="margin-top: 1rem;">
"""


def create_temporal_null_figure(
    frame: DataFrame,
    dt_column: str,
    period: str,
    ncols: int = 2,
    figsize: tuple[float, float] = (7, 5),
) -> str:
    r"""Create a HTML representation of a figure with the temporal null
    value distribution.

    Args:
        frame: The DataFrame to analyze.
        dt_column: The datetime column used to analyze
            the temporal distribution.
        period: The temporal period e.g. monthly or daily.
        ncols: The number of columns.
        figsize: The figure size in inches. The first dimension
            is the width and the second is the height.

    Returns:
        The HTML representation of the figure.
    """
    if frame.shape[0] == 0:
        return ""
    figures = create_temporal_null_figures(
        frame=frame, dt_column=dt_column, period=period, figsize=figsize
    )
    # figures = list(map(str, range(len(figures))))

    columns = []
    for i in range(ncols):
        figs = str_indent("\n".join(figures[i::ncols]))
        columns.append(f'<div class="col">\n  {figs}\n</div>')

    return Template(
        """
    <div class="container-fluid text-center">
      <div class="row align-items-start">
        {{columns}}
      </div>
    </div>
    """
    ).render({"columns": "\n".join(columns)})


def create_temporal_null_figures(
    frame: DataFrame,
    dt_column: str,
    period: str,
    figsize: tuple[float, float] = (7, 5),
) -> list[str]:
    r"""Create a HTML representation of each figure with the temporal
    null value distribution.

    Args:
        frame: The DataFrame to analyze.
        dt_column: The datetime column used to analyze
            the temporal distribution.
        period: The temporal period e.g. monthly or daily.
        figsize: The figure size in inches. The first dimension
            is the width and the second is the height.

    Returns:
        The HTML representations of the figures.
    """
    if frame.shape[0] == 0:
        return []
    columns = sorted([col for col in frame.columns if col != dt_column])
    figures = []
    for column in tqdm(columns, desc="generating figures"):
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(f"column: {column}")

        num_nulls, total, labels = prepare_data(
            frame=frame, column=column, dt_column=dt_column, period=period
        )
        plot_temporal_null_total(ax=ax, labels=labels, num_nulls=num_nulls, total=total)
        readable_xticklabels(ax, max_num_xticks=50)
        figures.append(figure2html(fig, close_fig=True))

    return figures


def prepare_data(
    frame: DataFrame,
    column: str,
    dt_column: str,
    period: str,
) -> tuple[np.ndarray, np.ndarray, list]:
    r"""Prepare the data to create the figure and table.

    Args:
        frame: The DataFrame to analyze.
        column: The column to analyze.
        dt_column: The datetime column used to analyze
            the temporal distribution.
        period: The temporal period e.g. monthly or
            daily.

    Returns:
        A tuple with 3 values. The first value is a numpy NDArray
            that contains the number of null values per period. The
            second value is a numpy NDArray that contains the total
            number of values. The third value is a list that contains
            the label of each period.

    Example usage:

    ```pycon
    >>> import numpy as np
    >>> import pandas as pd
    >>> from flamme.section.null_temp_all import prepare_data
    >>> num_nulls, total, labels = prepare_data(
    ...     frame=pd.DataFrame(
    ...         {
    ...             "col": np.array([np.nan, 1, 0, 1]),
    ...             "datetime": pd.to_datetime(
    ...                 ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
    ...             ),
    ...         }
    ...     ),
    ...     column="col",
    ...     dt_column="datetime",
    ...     period="M",
    ... )
    >>> num_nulls
    array([1, 0, 0, 0])
    >>> total
    array([1, 1, 1, 1])
    >>> labels
    ['2020-01', '2020-02', '2020-03', '2020-04']

    ```
    """
    dataframe = frame[[column, dt_column]].copy()
    dt_col = "__datetime__"
    dataframe[dt_col] = dataframe[dt_column].dt.to_period(period)

    null_col = f"__{column}_isna__"
    dataframe.loc[:, null_col] = dataframe.loc[:, column].isna()

    num_nulls = dataframe.groupby(dt_col)[null_col].sum().sort_index()
    total = dataframe.groupby(dt_col)[null_col].count().sort_index()
    labels = [str(dt) for dt in num_nulls.index]
    return num_nulls.to_numpy().astype(int), total.to_numpy().astype(int), labels
