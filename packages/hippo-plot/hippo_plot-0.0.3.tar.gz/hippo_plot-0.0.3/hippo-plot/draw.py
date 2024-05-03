
import io
import molparse as mp
from rdkit.Chem import Draw, MolFromSmiles
import base64

def smiles_to_png(smiles):	
	mol = MolFromSmiles(smiles)
	image = Draw.MolToImage(mol)
	buff = io.BytesIO()
	image.save(buff, format='png')
	return base64.b64encode(buff.getvalue()).decode("utf-8")
