
import io
import molparse as mp
from rdkit.Chem import Draw
import base64

def smiles_to_png(smiles):	
	mol = mp.rdkit.mol_from_smiles(smiles)
	image = Draw.MolToImage(mol)
	buff = io.BytesIO()
	image.save(buff, format='png')
	return base64.b64encode(buff.getvalue()).decode("utf-8")
