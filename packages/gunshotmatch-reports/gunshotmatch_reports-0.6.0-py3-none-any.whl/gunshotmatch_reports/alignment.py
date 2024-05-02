#!/usr/bin/env python3
#
#  alignment.py
"""
CSV reports of alignment between reference projects and unknown samples.

.. versionadded:: 0.5.0
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
import csv
import io
from typing import MutableSequence, NamedTuple, Optional, Tuple

# 3rd party
from libgunshotmatch.consolidate import ConsolidatedPeak
from libgunshotmatch.project import Project

__all__ = ["CSVRow", "csv_two_projects", "csv_two_projects_and_unknown", "get_csv_data"]


def _max_peak_area(project: Project) -> float:
	"""
	Returns the maximum peak area for the given project.

	:param project:
	"""

	assert project.consolidated_peaks is not None
	return max(cp.area for cp in project.consolidated_peaks)


class CSVRow(NamedTuple):
	"""
	Represents data for a peak in a CSV report.
	"""

	peak_no: str = ''
	name: str = ''
	rt: str = ''
	area: str = ''
	area_percentage: str = ''
	match_factor: str = ''

	def __bool__(self) -> bool:
		return all(self)

	@classmethod
	def header(cls) -> Tuple[str, str, str, str, str, str]:
		"""
		Returns the CSV column headers.

		:rtype:

		.. latex:clearpage::
		"""

		return "Peak No.", "Name", "Rt", "Area", "Area %", "MF"

	# @classmethod
	# def padding(cls) -> Tuple[str, str, str, str, str, str]:
	# 	return "", "", "", "", "" ""


def get_csv_data(project: Project, cp: Optional[ConsolidatedPeak], max_area: float) -> CSVRow:
	"""
	Return data for the CSV report for given peak in the given project.

	:param project:
	:param cp:
	:param max_area: The maximum peak area in the project.
	"""

	assert project.consolidated_peaks is not None

	if cp is None:
		return CSVRow()
	else:
		first_hit = cp.hits[0]
		area = cp.area
		area_percentage = area / max_area
		return CSVRow(
				str(project.consolidated_peaks.index(cp) + 1),
				first_hit.name,
				f"{cp.rt / 60:.3f}",
				f"{area:.1f}",
				f"{area_percentage:.3%}",
				f"{first_hit.match_factor:.1f}"
				)


_PaddedPeakList = MutableSequence[Optional[ConsolidatedPeak]]


def csv_two_projects_and_unknown(
		p1: Project,
		padded_p1_cp: _PaddedPeakList,
		p2: Project,
		padded_p2_cp: _PaddedPeakList,
		u: Project,
		padded_u_cp: _PaddedPeakList,
		*,
		pair_only: bool = False,
		) -> str:
	"""
	Returns CSV report for the alignment between the given projects and unknown.

	:param p1: The first project.
	:param padded_p1_cp: Padded consolidated peak list for the first project.
	:param p2: The second project.
	:param padded_p2_cp: Padded consolidated peak list for the second project.
	:param u: The unknown sample.
	:param padded_u_cp: Padded consolidated peak list for the unknown sample.
	:param pair_only: Only show peaks in common between two or more of the projects/unknown.
	"""

	fp = io.StringIO()

	p1_max_pa = _max_peak_area(p1)
	p2_max_pa = _max_peak_area(p2)
	unkn_max_pa = _max_peak_area(u)

	csvwriter = csv.writer(fp, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	top_row_pad = ('', ) * (5)
	csvwriter.writerow((p1.name, *top_row_pad, u.name, *top_row_pad, p2.name, *top_row_pad))
	csvwriter.writerow(CSVRow.header() * 3)

	for cp1, cp2, cpu in zip(padded_p1_cp, padded_p2_cp, padded_u_cp):
		cp1_data = get_csv_data(p1, cp1, p1_max_pa)
		cp2_data = get_csv_data(p2, cp2, p2_max_pa)
		unknown_data = get_csv_data(u, cpu, unkn_max_pa)

		if pair_only:
			if sum(tuple(map(all, [cp1_data, cp2_data, unknown_data]))) >= 2:
				csvwriter.writerow(cp1_data + unknown_data + cp2_data)
		else:
			csvwriter.writerow(cp1_data + unknown_data + cp2_data)

	return fp.getvalue()


def csv_two_projects(
		p1: Project,
		padded_p1_cp: _PaddedPeakList,
		p2: Project,
		padded_p2_cp: _PaddedPeakList,
		) -> str:
	"""
	Returns CSV report for the alignment between the given projects.

	:param p1: The first project.
	:param padded_p1_cp: Padded consolidated peak list for the first project.
	:param p2: The second project.
	:param padded_p2_cp: Padded consolidated peak list for the second project.
	"""

	fp = io.StringIO()

	p1_max_pa = _max_peak_area(p1)
	p2_max_pa = _max_peak_area(p2)

	csvwriter = csv.writer(fp, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	top_row_pad = ('', ) * (5)
	csvwriter.writerow((p1.name, *top_row_pad, p2.name, *top_row_pad))
	csvwriter.writerow(CSVRow.header() * 2)

	for cp1, cp2 in zip(padded_p1_cp, padded_p2_cp):
		cp1_data = get_csv_data(p1, cp1, p1_max_pa)
		cp2_data = get_csv_data(p2, cp2, p2_max_pa)
		csvwriter.writerow(cp1_data + cp2_data)

	return fp.getvalue()
