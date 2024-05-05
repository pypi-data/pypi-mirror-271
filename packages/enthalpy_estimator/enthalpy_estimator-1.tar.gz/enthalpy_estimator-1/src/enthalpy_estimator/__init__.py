# read version from installed package
from importlib.metadata import version
__version__ = version("enthalpy_estimator")

def mol_template(xyz, energies, hcorr='', name='', smiles='', dfH=0, u=0):
    return {
        'name': name,
        'smiles': smiles,
        'dfH': dfH,
        'u': u,
        'xyz': xyz,
        'energies': energies,
        'hcorr': hcorr,
    }