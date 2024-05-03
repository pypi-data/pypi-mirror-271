
import re

from mlog import setup_logger
logger = setup_logger('hippo_plot')

def clean_traces(fig):
	fig.update_traces(hoverinfo="none", hovertemplate=None)

def extract_customdata(fig):
	if len(fig.data) != 1:
		logger.warning('Using first Figure trace')

	hovertemplate = fig.data[0]['hovertemplate'].replace('%{','{')
	customdata = fig.data[0]['customdata']

	assert customdata
	assert hovertemplate

	return customdata, hovertemplate

def extract_smiles(customdata, hovertemplate, match_index=0):

	regex = r'<br>(.*?smiles={customdata\[.*?\]})'

	matches = re.findall(regex, hovertemplate)

	cols = {}
	for match in matches:
		col_name = re.findall(r'<br>(.*?)={', match)[0]
		col_id = int(re.findall(r'={customdata\[(.*?)\]', match)[0])
		cols[col_name] = col_id

	if len(matches):
		logger.warning(f'Choosing the {match_index}th *_smiles column from {list(cols.keys())}')

	smiles_col_name = list(cols.keys())[match_index]
	smiles_col_id = cols[smiles_col_name]
	smiles_strings = [c[smiles_col_id] for c in customdata]

	return smiles_strings
