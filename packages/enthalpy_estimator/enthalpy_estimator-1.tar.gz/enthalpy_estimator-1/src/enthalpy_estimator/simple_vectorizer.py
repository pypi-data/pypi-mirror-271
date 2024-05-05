import numpy as np

class MolVectorizer:
    def __init__(self, all_species, isodesmic=False):
        self.all_species = all_species

        if isodesmic:
            print('Warning: simple vectorizer does not support isodesmic reactions')
        
        self.init_basis()
    
    def read_atoms(self, r):
        try:
            with open(r['xyz'], 'r') as f:
                atoms = {}
                for l in f:
                    if ' ' not in l: continue
                    a = l.split()[0].strip()
                    atoms[a] = atoms.get(a, 0) + 1

                return atoms
        except OSError:
            print(f'Error reading file {r["xyz"]}')
            return {}

    def init_basis(self):
        self.mols = [self.read_atoms(r) for r in self.all_species]
        self.symbols = np.array(sorted({el for atoms in self.mols for el in atoms.keys()}))
        self.dim = len(self.symbols)
        self.basis = np.array([[atoms.get(e, 0) for e in self.symbols] for atoms in self.mols], dtype=np.int32)
    
    @staticmethod
    def coef_to_str(c):
        return str(c) if c!=1 else ''

    def vector_to_str(self, v):
        els = np.where(v[:len(self.symbols)] != 0)
        el_n = np.column_stack([self.symbols[els], v[els]])
        el_n[el_n[:, 1] == '1', 1] = ''
        s = ''.join(''.join(el_n.flatten()))
                    
        return s
    
    def reaction_to_str(self, rxn):
        r = rxn * np.sign(rxn[0])
        reagents = np.where(r > 0)[0]
        products = np.where(r < 0)[0]

        s = ''
        s += '+'.join(
                ''.join([self.coef_to_str(r[i].item()), self.vector_to_str(self.basis[i])]) 
                for i in reagents)
        s += '->'
        s += '+'.join(
                ''.join([self.coef_to_str(-r[i].item()), self.vector_to_str(self.basis[i])]) 
                for i in products)

        return s
    
    def reaction_to_names(self, rxn):
        r = rxn * np.sign(rxn[0])
        reagents = np.where(r > 0)[0]
        products = np.where(r < 0)[0]

        s = ''
        s += '+'.join(
                ''.join([str(r[i].item()) + '*'
                         if abs(r[i].item()) != 1
                         else '', 
                         self.all_species[i]['name']
                         if 'name' in self.all_species[i]
                         else self.vector_to_str(self.basis[i])]) 
                for i in reagents)
        s += '->'
        s += '+'.join(
                ''.join([str(-r[i].item()) + '*'
                         if abs(r[i].item()) != 1
                         else '', 
                         self.all_species[i]['name']
                         if 'name' in self.all_species[i]
                         else self.vector_to_str(self.basis[i])]) 
                for i in products)

        return s