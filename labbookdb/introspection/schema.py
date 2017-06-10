import codecs
import pydotplus
import sadisplay
from os import path
from labbookdb.db.query import ALLOWED_CLASSES
from labbookdb.db.common_classes import *

def generate(
	extent="all",
	save_dotfile="",
	save_plot="",
	label="",
	linker_tables=False
	):
	"""Retreive the LabbookDB schema and save either a DOT file, or a PNG or PDF plot.
	"""

	if extent == "all":
		nodes = ALLOWED_CLASSES.values()
	elif type(extent) is list:
		nodes = [ALLOWED_CLASSES[key] for key in extent]

	if linker_tables:
		nodes.extend(linker_tables)

	desc = sadisplay.describe(nodes)

	if save_dotfile:
		save_dotfile = path.abspath(path.expanduser(save_dotfile))
		with codecs.open(save_dotfile, 'w', encoding='utf-8') as f:
			f.write(sadisplay.dot(desc))

	if save_plot:
		save_plot = path.abspath(path.expanduser(save_plot))
		dot = sadisplay.dot(desc)
		dot = dot.replace('label = "generated by sadisplay v0.4.8"', 'label = "{}"'.format(label))
		graph = pydotplus.graph_from_dot_data(dot)
		filename, extension = path.splitext(save_plot)
		if extension in [".png",".PNG"]:
			graph.write_png(save_plot)
		elif extension in [".pdf",".PDF"]:
			graph.write_pdf(save_plot)

if __name__ == '__main__':
	# generate(extent="all", save_plot="~/full_schema.png")
	# generate(extent=["Animal","CageStay","Cage","OpticFiberImplantProtocol","Operation","OrthogonalStereotacticTarget","Protocol"], save_plot="~/cagestay_schema.pdf", linker_tables=[operation_association])
	# generate(extent=["Animal","CageStay","Cage",], save_plot="~/cagestay_schema.pdf", linker_tables=[cage_stay_association])
	# generate(
	# 	extent=[
	# 		"Animal",
	# 		"ForcedSwimTestMeasurement",
	# 		"Evaluation",
	# 		"CageStay",
	# 		"Cage",
	# 		"Measurement",
	# 		"Treatment",
	# 		"Protocol",
	# 		],
	# 	save_plot="~/fst_schema.pdf",
	# 	linker_tables=[
	# 		cage_stay_association,
	# 		treatment_cage_association,
	# 		],
	# 	)
	# generate(extent=["Animal","CageStay","Cage","SucrosePreferenceMeasurement"], save_plot="~/measurements_schema.pdf")
	generate(extent=["Animal","Operation","Protocol","Operator"], save_plot="~/basic_schema.pdf", linker_tables=[authors_association,operation_association])
	# generate(extent=["Animal","FMRIMeasurement","OpenFieldTestMeasurement","WeightMeasurement"], save_plot="~/measurements_schema.pdf")
