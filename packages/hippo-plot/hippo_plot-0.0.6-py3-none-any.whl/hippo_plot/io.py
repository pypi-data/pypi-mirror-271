
import plotly
import re

import logging
logger = logging.getLogger('hippo_plot')

def fig_from_json():
	return plotly.io.fig_json('plot.json')

def fig_from_html(filename):
	import json
	
	with open(filename) as f:
		html = f.read()

	call_arg_str = re.findall(r'Plotly\.newPlot\((.*)\)', html)[0]
	call_args = json.loads(f'[{call_arg_str}]')
	plotly_json = {'data': call_args[1], 'layout': call_args[2]}    

	return plotly.io.from_json(json.dumps(plotly_json))

def html_from_fig(fig):

	"""Construct some static HTML that includes the plotly.js headers, the graph in a div"""
	
	from plotly.offline import plot

	# html header
	html = ['<!DOCTYPE html>\n']
	html.append('<html>\n')
	html.append('<head>\n')

	# title
	title = fig.layout.title.text or 'Figure'
	html.append(f'<title>{title}</title>\n')
	
	# end header, start body
	html.append('</head>\n')
	html.append('<body>\n')
	
	# plotly
	html.append('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

	# Get HTML of the figure as a div
	fig_html = plot(fig, output_type='div', include_plotlyjs=False).removeprefix('<div>').strip()

	html.append(fig_html)
	html.append('</body>\n')
	html.append('</html>\n')

	return ''.join(html)

def write_html(filename, fig):
	"""Write this plotly figure as an HTML file that is both stand-alone viewable and with hippo_plot"""
	with open(filename, 'wt') as f:
		logger.writing(filename)
		f.write(html_from_fig(fig))
