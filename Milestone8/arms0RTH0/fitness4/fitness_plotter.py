import pickle
import sys
import pandas as pd
import os
import glob
import itertools
import bokeh
import itertools
import constants as c
import math
from datetime import datetime
from bokeh.io import output_file, show, save, export_png
from bokeh.palettes import Spectral, Dark2, Category10, Category20, Category20b, Category20c, inferno 
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components, file_html
from bokeh.models import ColumnDataSource, Range1d, DateFormatter, CustomJS, Legend, NumeralTickFormatter, HoverTool, PrintfTickFormatter, LabelSet, FuncTickFormatter, DatetimeTickFormatter
from bokeh.resources import CDN
from bokeh.colors import RGB
from selenium import webdriver


class FitnessPlotter:

	def __init__(self):

		# Read in the pickle file 
		file = f'arms_{c.ARMS}_RT_{c.ROTATING_HIP}.pkl'
		info = pickle.load(open(file, "rb"))

		### Create a pandas dataframe with 3 columns: Generation, Fitness Score, PHC Run
		generation_count 	= 0
		generations 		= []
		fitness_scores 		= []
		phc_runs 			= []
		for phc_run in info["phc_run__2__fitness_scores_per_generation_of_best_parent"].keys():
			for fitness_score in info['phc_run__2__fitness_scores_per_generation_of_best_parent'][phc_run]:
				generations.append(generation_count)
				fitness_scores.append(fitness_score)
				phc_runs.append(f'PHC Run {phc_run+1}')
				generation_count+=1
			# end for fitness_score
		# end for phc_run
		df 					= pd.DataFrame(columns = ["Generation", "Fitness Score", "PHC Run"])
		df['Generation'] 	= generations
		df['Fitness Score'] = fitness_scores
		df['PHC Run']		= phc_runs
		title 		 		= "Fitness Scores Per Generation of Best Parent -- "
		if c.ARMS:
			title += "With Arms & "
		else:
			title += "Without Arms & "
		if c.ROTATING_HIP:
			title += "With Rotating Hip"
		else:
			title += "Without Rotating Hip"
		lines 		 		= list(set(phc_runs))
		filter_df_on 		= 'PHC Run'
		x_axis_param 		= 'Generation'
		x_axis_label 		= 'Generation'
		y_axis_label 		= 'Fitness Score'
		self.multi_line_plot(title=title, lines=lines, filter_df_on=filter_df_on, \
							 x_axis_param=x_axis_param, x_axis_label=x_axis_label, \
							 y_axis_label=y_axis_label, df=df)

	def multi_line_plot(self, title, lines, filter_df_on, x_axis_param, x_axis_label, y_axis_label, df, height=400, width=850):

		output_file_name = f'arms_{c.ARMS}_RT_{c.ROTATING_HIP}'
		output_file(f'arms_{c.ARMS}_RT_{c.ROTATING_HIP}.html', mode='inline')

		# Getting a list of colors based on the number of lines
		colors = {

			'PHC Run 1' : 'blue',
			'PHC Run 2' : 'green',
			'PHC Run 3' : 'red',
			'PHC Run 4' : 'orange',
			'PHC Run 5' : 'purple',
			'PHC Run 6' : 'pink',
			'PHC Run 7' : 'black',
			'PHC Run 8' : 'lime',
			'PHC Run 9' : 'olive',
			'PHC Run 10': 'darkred'

		}

		# Instantiating the graph figure object
		graph = figure(title=title, plot_height=height, plot_width=width)

		# Naming hte x axis
		graph.xaxis.axis_label 	= x_axis_label
		# Naming the y axis
		graph.yaxis.axis_label 	= y_axis_label
		# Defining the HoverTool for the graph
		hover_tool 		 		= graph.select(type=HoverTool)
		hover_tool.names 		= lines
		# Define lists to hold graph lines and circles
		foo 			 = []
		# Putting lines in the graph and storing in an array "foo", to reference later when we build the graph legend
		line_counter 	 = 0
		for line in lines:

			# Define a data dict for the bokeh column data source
			filtered_df   = df[ df[filter_df_on] == line ]
			data_dict 	  = dict()
			attributes 	  = ["Generation", "Fitness Score", "PHC Run"]
			for attribute in attributes:
				data_dict[attribute] = filtered_df[attribute].tolist()
			# end for attribute

			source 		  = 	ColumnDataSource(data_dict)
			color 		  = 	colors[line]
			line_counter  += 1
			foo.append(   graph.line( x='Generation', y='Fitness Score', name=line, source=source, line_width=2, line_color=color ) )
			graph.circle( x='Generation', y='Fitness Score', name=line, source=source, color=color )
			
		# end for line in lines

		count = 0
		items = []
		while count < len(lines):
			items.append( (lines[count], [foo[count]]) )
			count += 1
		# end while

		# Intitializing the legend
		legend = Legend( items=sorted(items), location=(0,0) )

		# Adding HoverTool to the graph
		graph.add_tools(HoverTool(

			tooltips = [

				( "Generation", 	'@{Generation}' ),
				( "Fitness Score", 	'@{Fitness Score}' ),
				( "PHC Run", 		'@{PHC Run}')

			],
			formatters = {
				'adj close': 		'printf'
			}

		))

		# Adding the Legend to the graph and formatting
		graph.add_layout(legend, 			  'right'   )
		graph.legend.location 				= 'top_right'
		#graph.legend.orientation 			= 'veritcal'
		graph.legend.click_policy 			= 'hide'

		# Formatting graph some more
		graph.y_range.start 				= 0
		graph.x_range.range_padding 		= 0.25
		graph.y_range.range_padding 		= 0.25
		graph.xgrid.grid_line_color 		= None
		graph.axis.minor_tick_line_color 	= None
		graph.outline_line_color 			= None
		graph.xaxis.major_label_orientation = math.pi/3

		# Save plot
		script, div 						= components(graph)
		save(graph)


FitnessPlotter()



