#!/usr/bin/env python

# Take some plotly HTML from a file and add molecular images to hoverover using molplotly

import argparse
from dash import dcc, html, Input, Output, no_update, Dash
from hipplot.draw import smiles_to_png

################ ARGS ################

parser = argparse.ArgumentParser(prog='hippo-plot', description='Take some plotly HTML from a file and add molecular images to hoverover using molplotly')

parser.add_argument('filename')

args = parser.parse_args()

################ PREPARE FIGURE ################

from hipplot.io import fig_from_html
fig = fig_from_html(args.filename)

from hipplot.prep import clean_traces, extract_smiles
clean_traces(fig)
smiles_strings = extract_smiles(fig)

################ DASH APP ################

app = Dash(__name__)

app.layout = html.Div([
	dcc.Graph(id="graph", figure=fig, clear_on_unhover=True),
	dcc.Tooltip(id="graph-tooltip"),
])

@app.callback(
	Output("graph-tooltip", "show"),
	Output("graph-tooltip", "bbox"),
	Output("graph-tooltip", "children"),
	Input("graph", "hoverData"),
)

def display_hover(hoverData):
	if hoverData is None:
		return False, no_update, no_update

	# demo only shows the first point, but other points may also be available
	pt = hoverData["points"][0]
	bbox = pt["bbox"]
	num = pt["pointNumber"]

	### ENCODE THE IMAGE

	smiles = smiles_strings[num]
	encoded = smiles_to_png(smiles)

	### CREATE THE HOVER DIV

	children = [
		html.Div(children=[
			html.Img(src="data:image/png;base64,{}".format(encoded), style={"width": "100%"})
			# html.H2(f"{name}", style={"color": "darkblue"}),
			# html.P(f"{desc}"),
		],
		style={'width': '150px', 'white-space': 'normal'})
	]

	return True, bbox, children

def main():
	app.run_server(debug=False)

if __name__ == '__main__':
	main()
