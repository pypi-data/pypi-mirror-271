#!/usr/bin/env python

# Take some plotly HTML from a file and add molecular images to hoverover using molplotly

import argparse
from dash import dcc, html, Input, Output, no_update, Dash
from .draw import smiles_to_png
import dash_dangerously_set_inner_html

################ ARGS ################

parser = argparse.ArgumentParser(prog='hippo-plot', description='Take some plotly HTML from a file and add molecular images to hoverover using molplotly')

parser.add_argument('filename')

args = parser.parse_args()

################ PREPARE FIGURE ################

from .io import fig_from_html
fig = fig_from_html(args.filename)

from .prep import clean_traces, extract_smiles, extract_customdata
customdata, hovertemplate = extract_customdata(fig)
smiles_strings = extract_smiles(customdata, hovertemplate, match_index=0)
clean_traces(fig)

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

	### HOVER TEXT
	hovertext = hovertemplate.format(**pt).removesuffix('<extra></extra>')

	### CREATE THE HOVER DIV

	children = [
		html.Div(children=[
			# html.H2(f"{name}", style={"color": "darkblue"}),
			html.Img(src="data:image/png;base64,{}".format(encoded), style={"width": "100%"}),
			# html.P(hovertext),
			dash_dangerously_set_inner_html.DangerouslySetInnerHTML(hovertext),
		],
		style={'width': '150px', 'white-space': 'normal'})
	]

	return True, bbox, children

def main():
	app.run_server(debug=False)

if __name__ == '__main__':
	main()
