#!/usr/bin/env python3
#
#  peaks.py
"""
Peak Report Generator.
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
import os
from typing import List, NamedTuple, Optional, Tuple

# 3rd party
from domdf_python_tools.paths import PathLike
from libgunshotmatch.consolidate import ConsolidatedPeak
from libgunshotmatch.project import Project
from libgunshotmatch_mpl.peakviewer import draw_peaks
from libgunshotmatch_mpl.peakviewer import load_project as load_project  # noqa: F401
from matplotlib import pyplot as plt  # type: ignore[import]
from matplotlib.figure import Figure  # type: ignore[import]
from reportlab.lib import colors  # type: ignore[import]
from reportlab.lib.pagesizes import A4  # type: ignore[import]
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore[import]
from reportlab.lib.units import inch  # type: ignore[import]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import]
from reportlab.platypus import (  # type: ignore[import]
		BaseDocTemplate,
		Image,
		PageBreak,
		Paragraph,
		SimpleDocTemplate,
		Spacer,
		Table,
		TableStyle
		)

# this package
from gunshotmatch_reports.utils import extend_list, figure_to_drawing, scale

__all__ = ("CSVReports", "PeakMetadataTable", "PeakSummary", "build_peak_report")


def _get_peak_figure(project: Project, consolidated_peak: ConsolidatedPeak) -> Figure:

	# figsize = (6.4, 4.8)
	figsize = (10.5, 5)
	figure = plt.figure(figsize=figsize, layout="constrained")
	axes = figure.subplots(
			len(project.datafile_data),
			1,
			sharex=True,
			)

	draw_peaks(project, consolidated_peak.meta["peak_number"], figure, axes)

	return figure


def _get_peak_image(
		project: Project,
		consolidated_peak: ConsolidatedPeak,
		image_scale: float = 0.75,
		align: str = "CENTER",
		) -> Image:
	drawing = figure_to_drawing(_get_peak_figure(project, consolidated_peak))
	return Image(scale(drawing, scale=image_scale), hAlign=align)


styles = getSampleStyleSheet()
title_style = ParagraphStyle(
		"Title",
		parent=styles["Heading1"],
		alignment=1,
		)
title_spacer_style = ParagraphStyle(
		"TitleSpacer",
		parent=title_style,
		textColor=colors.HexColor("#ffffff"),
		)


class PeakSummary(NamedTuple):
	"""
	Summary data for a :class:`~libgunshotmatch.consolidate.ConsolidatedPeak`.

	Formatted for insertion into a PDF or CSV peak report.

	.. versionadded:: 0.3.0
	"""

	#: Peak number, 1-indexed
	peak_no: str

	#: The name of the top hit
	name: str

	#: Mean retention time
	rt: str

	#: Mean peak area
	area: str

	#: Mean peak area as a percentage of the largest peak
	area_percentage: str

	#: Mean match factor for the top hit
	mf: str

	#: Whether the peak has been rejected (e.g. with PeakViewer)
	rejected: str


class PeakMetadataTable:
	"""
	Helper class for peak metadata for insertion into a PDF or CSV report.

	:param project: A GunShotMatch project.

	.. versionadded:: 0.3.0
	"""

	def __init__(self, project: Project):

		#: A GunShotMatch project.
		self.project = project

		assert project.consolidated_peaks is not None

		#: The total number of peaks in the project.
		self.max_peak_number = len(project.consolidated_peaks)

		#: Maximum number of rows for the metadata table.
		self.num_rows = max(5, len(project.datafile_data))

		all_areas = [cp.area for cp in project.consolidated_peaks]
		max_area = max(all_areas)

		#: Peak areas as percentage of largest peak
		self.area_percentages = [area / max_area for area in all_areas]

	def get_summary_for_peak(self, peak: ConsolidatedPeak, peak_number: int) -> PeakSummary:
		"""
		Return a formatted summary of the peak.

		:param peak:
		:param peak_number: The peak number, 1-indexed.
		"""

		return PeakSummary(
				str(peak_number),
				peak.hits[0].name,
				f"{peak.rt / 60:0.3f}",
				f"{peak.area:0,.1f}",
				f"{self.area_percentages[peak_number-1]:0.3%}",
				f"{peak.hits[0].match_factor:.1f}",
				f"{not peak.meta.get('acceptable_shape', True)}",
				)

	def get_table_for_peak(
			self,
			peak: ConsolidatedPeak,
			peak_number: int,
			) -> List[Tuple[str, str, str, str, str, str, str, str, str]]:
		"""
		Return tabulated data on the peak, with individual peak areas, retention times, and the top 5 hits.

		:param peak:
		:param peak_number: The peak number, 1-indexed.
		"""

		summary = self.get_summary_for_peak(peak, peak_number)
		peak_metadata: List[Tuple[str, str]] = [
				("Peak", f"{peak_number} / {self.max_peak_number}"),
				("Retention Time", summary.rt),
				("Peak Area", summary.area),
				# ("Peak Area Stdev", f"{peak.area_stdev:0.1f}"),
				("Peak Area %", summary.area_percentage),
				("Rejected", summary.rejected),
				]

		peak_metadata = extend_list(peak_metadata, ('', ''), self.num_rows)

		hits_data: List[Tuple[str, str, str]] = []
		for hit in peak.hits[:5]:
			hits_data.append((hit.name, f"{hit.match_factor:.1f}", str(len(hit))))

		hits_data = extend_list(hits_data, ('', '', ''), self.num_rows)

		rt_area_data = []
		for rt, area in zip(peak.rt_list, peak.area_list):
			rt_area_data.append((f"{rt/60:0.3f}", f"{area:0,.1f}"))

		rt_area_data = extend_list(rt_area_data, ('', ''), self.num_rows)

		table_data = [('', '', '', "Hit Name", "MF", 'n', '', "RTs", "Peak Areas")]
		for peak_row, hits_row, rt_area_row in zip(peak_metadata, hits_data, rt_area_data):
			table_row = peak_row + ('', ) + hits_row + ('', ) + rt_area_row
			table_data.append(table_row)

		return table_data


def build_peak_report(
		project: Project,
		pdf_filename: Optional[PathLike] = None,
		*,
		title_every_page: bool = False,
		) -> str:
	"""
	Construct a peak report for the given project and write to the chosen file.

	:param project:
	:param pdf_filename: Optional output filename. Defaults to :file:`{project_name}_peak_report.pdf`.
	:no-default pdf_filename:

	:returns: The output filename.
	"""

	if pdf_filename is None:
		pdf_filename = project.name + "_peak_report.pdf"
	else:
		pdf_filename = os.fspath(pdf_filename)

	pageinfo = f"GunShotMatch Peak Report – {project.name}"

	def draw_footer(canvas: Canvas, doc: BaseDocTemplate) -> None:
		canvas.saveState()
		canvas.setFont("Times-Roman", 9)
		canvas.drawString(inch, 0.75 * inch, "Page %d – %s" % (doc.page, pageinfo))
		canvas.restoreState()

	doc = SimpleDocTemplate(
			pdf_filename,
			pagesize=A4[::-1],
			leftMargin=0.5 * inch,
			righMargin=0.5 * inch,
			topMargin=0.75 * inch,
			bottomMargin=0.5 * inch,
			title=pageinfo,
			)

	page_title_para = Paragraph(pageinfo, style=title_style)
	doc_elements = [page_title_para]

	assert project.consolidated_peaks is not None
	metadata_table_writer = PeakMetadataTable(project)

	for peak_idx, consolidated_peak in enumerate(project.consolidated_peaks):
		image = _get_peak_image(project, consolidated_peak)

		table_data = metadata_table_writer.get_table_for_peak(consolidated_peak, peak_idx + 1)

		t = Table(
				table_data,
				colWidths=(None, None, 0.04 * inch, None, None, None, 0.04 * inch, None, None),
				)
		tablestyle = TableStyle([
				# 	('SPAN', (5, 0), (6, 0)),
				("LINEBELOW", (0, 0), (-1, 0), 0.25, colors.black),
				("LINEAFTER", (1, 0), (2, -1), 0.25, colors.black),
				("LINEAFTER", (5, 0), (6, -1), 0.25, colors.black),
				])
		t.setStyle(tablestyle)
		doc_elements.append(t)

		doc_elements.append(image)
		doc_elements.append(Spacer(1, 0.25 * inch))
		doc_elements.append(PageBreak())
		if title_every_page:
			doc_elements.append(page_title_para)
		else:
			doc_elements.append(Paragraph('a', style=title_spacer_style))
		# doc_elements.append(Spacer(1,1*inch))

	# Remove last page break to prevent blank page
	doc_elements.pop()
	doc_elements.pop()

	doc.build(doc_elements, onFirstPage=draw_footer, onLaterPages=draw_footer)

	return pdf_filename


class CSVReports:
	"""
	Class for producing CSV peak reports.

	:param project: A GunShotMatch project.

	.. versionadded:: 0.4.0
	"""

	def __init__(self, project: Project):

		self._metadata_table_writer = PeakMetadataTable(project)

		assert project.consolidated_peaks is not None
		self._peaks_and_indices = list(enumerate(project.consolidated_peaks))
		self._peaks_and_indices.sort(key=lambda x: x[1].area, reverse=True)

	def overview_csv(self) -> str:
		"""
		Produce an overview report of the peaks, giving the name, retention time and peak area of the peaks.

		The output columns are as follows:

		* Peak No.
		* Name – The name of the top hit
		* Rt – Mean retention time
		* Area – Mean peak area
		* Area % – Mean peak area as a percentage of the largest peak
		* MF – Mean match factor for the top hit
		* Rejected – Whether the peak has been rejected (e.g. with PeakViewer)

		The peaks are sorted from largest to smallest.
		"""

		fp = io.StringIO()

		csvwriter = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

		csvwriter.writerow(["Peak No.", "Name", "Rt", "Area", "Area %", "MF", "Rejected"])
		for peak_idx, consolidated_peak in self._peaks_and_indices:
			summary = self._metadata_table_writer.get_summary_for_peak(consolidated_peak, peak_idx + 1)
			csvwriter.writerow(summary)
		csvwriter.writerow('')

		return fp.getvalue()

	def summary_csv(self) -> str:
		"""
		Produce a summary report of the peaks, giving the individual retention times and hits.

		The table for each peak mirrors the table in the PDF peak report (:func:`~.build_peak_report`).
		The peaks are sorted from largest to smallest.
		"""

		fp = io.StringIO()

		csvwriter = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

		for peak_idx, consolidated_peak in self._peaks_and_indices:
			table_data = self._metadata_table_writer.get_table_for_peak(consolidated_peak, peak_idx + 1)
			csvwriter.writerows(table_data)
			csvwriter.writerow('')

		return fp.getvalue()
