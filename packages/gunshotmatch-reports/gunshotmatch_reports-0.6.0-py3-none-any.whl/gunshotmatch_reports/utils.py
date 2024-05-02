#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from io import BytesIO, StringIO
from typing import List, Tuple, TypeVar

# 3rd party
import matplotlib  # type: ignore[import]
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from matplotlib import pyplot as plt
from matplotlib.figure import Figure  # type: ignore[import]
from reportlab.graphics.shapes import Drawing  # type: ignore[import]
from svglib.svglib import svg2rlg  # type: ignore[import]

__all__ = ["extend_list", "figure_to_drawing", "scale", "save_pdf", "save_svg"]


def scale(drawing: Drawing, scale: float) -> Drawing:
	"""
	Scale reportlab.graphics.shapes.Drawing() object while maintaining aspect ratio.

	:param drawing:
	:param scale:
	"""

	scaling_x = scaling_y = scale

	drawing.width = drawing.minWidth() * scaling_x
	drawing.height = drawing.height * scaling_y
	drawing.scale(scaling_x, scaling_y)

	return drawing


def figure_to_drawing(figure: Figure) -> Drawing:
	"""
	Convert a matplotlib figure to a reportlab drawing.

	:param figure:
	"""

	imgdata = BytesIO()
	figure.savefig(imgdata, format="svg")
	plt.close(fig=figure)
	imgdata.seek(0)  # go to start of BytesIO
	return svg2rlg(imgdata)


_T = TypeVar("_T", bound=Tuple[str, ...])


def extend_list(l: List[_T], fillvalue: _T, length: int) -> List[_T]:
	"""
	Extend list to the given length with fillvalue.

	:param l:
	:param fillvalue:
	:param length:
	"""

	fillsize = length - len(l)
	for _ in range(fillsize):
		l.append(fillvalue)

	assert len(l) == length

	return l


def save_pdf(fig: Figure, filename: PathLike) -> None:
	"""
	Save a PDF without a creation date.

	:param fig:
	:param filename:

	.. versionadded:: 0.6.0
	"""

	fig.savefig(filename, format="pdf", metadata={"CreationDate": None})


def save_svg(fig: Figure, filename: PathLike) -> None:
	"""
	Save an SVG with fixed hashsalt and without a creation date.

	:param fig:
	:param filename:

	.. versionadded:: 0.6.0
	"""

	filename_p = PathPlus(filename)

	current_hashsalt = matplotlib.rcParams.get("svg.hashsalt")

	try:
		matplotlib.rcParams["svg.hashsalt"] = filename_p.name
		s = StringIO()
		fig.savefig(s, format="svg", metadata={"Date": None})
		filename_p.write_clean(s.getvalue())
	finally:
		matplotlib.rcParams["svg.hashsalt"] = current_hashsalt
