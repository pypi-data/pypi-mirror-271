
import re

import plotly.graph_objects as go

from mlog import setup_logger
logger = setup_logger('hippo_plot')

def clean_traces(fig):

	trace = fig.data[0]
	if isinstance(trace, go.Sankey):
		trace['node']['hovertemplate'] = None
		trace['node']['hoverinfo'] = "none"
	else:
		trace['hovertemplate'] = None
		trace['hoverinfo'] = "none"

	# fig.update_traces(hoverinfo="none", hovertemplate=None)

def extract_customdata(fig):
	if len(fig.data) != 1:
		logger.warning('Using first Figure trace')

	# print(fig.data)

	trace = fig.data[0]
	if isinstance(trace, go.Sankey):
		hovertemplate = trace['node']['hovertemplate'].replace('%{','{')
		customdata = trace['node']['customdata']
	else:
		hovertemplate = trace['hovertemplate'].replace('%{','{')
		customdata = trace['customdata']

	assert customdata
	assert hovertemplate

	return customdata, hovertemplate

def extract_smiles(customdata, hovertemplate, match_index=0):

	regex = r'<br>(.*?smiles={customdata\[.*?\]})'

	matches = re.findall(regex, hovertemplate)

	cols = {}
	for match in matches:

		print(match)
		col_matches = re.findall(r'<br>(.*?)={', match)
		if not col_matches:
			col_matches = re.findall(r'(.*?)={', match)
		col_name = col_matches[0]

		col_id = int(re.findall(r'={customdata\[(.*?)\]', match)[0])
		cols[col_name] = col_id

	if len(matches):
		logger.warning(f'Choosing the {match_index}th *_smiles column from {list(cols.keys())}')

	smiles_col_name = list(cols.keys())[match_index]
	smiles_col_id = cols[smiles_col_name]
	smiles_strings = [c[smiles_col_id] for c in customdata]

	return smiles_strings
