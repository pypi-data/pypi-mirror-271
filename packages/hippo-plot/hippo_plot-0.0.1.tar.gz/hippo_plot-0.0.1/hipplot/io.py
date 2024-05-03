
import plotly
import re

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
