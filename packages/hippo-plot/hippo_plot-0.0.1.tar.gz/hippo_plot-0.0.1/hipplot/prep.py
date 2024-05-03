
def clean_traces(fig):
	fig.update_traces(hoverinfo="none", hovertemplate=None)

def extract_smiles(fig):
	return [c[0] for c in fig.data[0]['customdata']]
