from .simple_vectorizer import MolVectorizer

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdqueries
import numpy as np

class SMILESVectorizer(MolVectorizer):
    def __init__(self, all_species, isodesmic=False):
        self.all_species = all_species
        self.isodesmic = isodesmic

        self.init_basis()

    @staticmethod
    def cleanup_xyz(filename):
        ind = open(filename).readlines()
        if ' ' in ind[0]:
            n_atoms = str(len(ind))
            ind = [n_atoms + '\n\n'] + ind

        return ''.join(ind)

    @staticmethod
    def smiles_to_mol(smi):
        return AllChem.AddHs(Chem.MolFromSmiles(smi))

    def mol_to_vec(self, mol):
        r_vec = [0]*self.dim

        for i, el in enumerate(self.elements):
            q = rdqueries.AtomNumEqualsQueryAtom(int(el))
            r_vec[i] = len(mol.GetAtomsMatchingQuery(q))

        if self.isodesmic:
            for i, b in enumerate(self.bonds):
                r_vec[len(self.elements)+i] = len(mol.GetSubstructMatches(b))

        return r_vec

    def init_basis(self):
        self.mols = [self.smiles_to_mol(r['smiles']) for r in self.all_species]
        self.elements = np.array(sorted(
            {a.GetAtomicNum() for mol in self.mols for a in mol.GetAtoms()}, reverse=True))
        self.bonds = [Chem.MolFromSmarts(s) for s in (
            '[#6]-[#1]', '[#6]-[#6]', '[#6]=[#6]', '[#6]#[#6]', '[#6]:[#6]')]
        self.symbols = np.array(
            [Chem.GetPeriodicTable().GetElementSymbol(int(e)) for e in self.elements])

        self.dim = len(self.symbols) + \
            (len(self.bonds) if self.isodesmic else 0)

        self.basis = np.array([self.mol_to_vec(mol) for mol in self.mols])

