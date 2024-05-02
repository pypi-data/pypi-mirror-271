#!/usr/bin/env python3
#
#  chromatogram.py
"""
PDF Chromatogram Generator.
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
import os
from typing import Optional

# 3rd party
from domdf_python_tools.paths import PathLike
from libgunshotmatch.project import Project
from libgunshotmatch_mpl.chromatogram import draw_chromatograms
from matplotlib import pyplot as plt  # type: ignore[import]

# this package
from gunshotmatch_reports.utils import save_pdf

__all__ = ["build_chromatogram_report"]


def build_chromatogram_report(project: Project, pdf_filename: Optional[PathLike] = None) -> str:
	"""
	Construct a chromatogram report for the given project and write to the chosen file.

	:param project:
	:param pdf_filename: Optional output filename. Defaults to :file:`{project_name}_chromatogram.pdf`.
	:no-default pdf_filename:
	"""

	if pdf_filename is None:
		pdf_filename = project.name + "_chromatogram.pdf"
	else:
		pdf_filename = os.fspath(pdf_filename)

	fig = plt.figure(layout="constrained", figsize=(11.7, 8.3))
	axes = fig.subplots(len(project.datafile_data), 1, sharex=True)
	draw_chromatograms(project, fig, axes)
	save_pdf(fig, pdf_filename)

	return pdf_filename
