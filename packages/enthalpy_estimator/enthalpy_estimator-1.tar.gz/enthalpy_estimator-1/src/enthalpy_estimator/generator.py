from .cfg import *

import numpy as np
import ctypes
import sys
import os

dll_path = os.path.dirname(os.path.abspath(__file__))

rgen = ctypes.CDLL(os.path.join(dll_path, 'rgen{}'.format('.dll' if sys.platform[:3].lower() == 'win' else '.so')))
rgen.generate.argtypes = (np.ctypeslib.ndpointer(ctypes.c_longlong, flags='C_CONTIGUOUS'),
                          ctypes.POINTER(ctypes.c_int),
                          np.ctypeslib.ndpointer(ctypes.c_int, flags='C_CONTIGUOUS'),
                          ctypes.c_int, ctypes.c_int, ctypes.c_int)
rgen.generate.restype = None

class ReactionGenerator:
    def __init__(self, target, reference, vectorizer, isodesmic=False):
        self.target = target
        self.reference = reference
        self.all_species = [self.target] + [r for r in self.reference if r != self.target]

        self.vectorizer = vectorizer(self.all_species, isodesmic=isodesmic)

        self.init_energies()

    def get_basis(self):
        return self.vectorizer.basis

    def init_energies(self):
        def read_energies(entry, r):
            try:
                with open(r['energies'], 'r') as f:
                    for l in f.readlines()[2:]:
                        if '=' in l:
                            l_split = [s.strip() for s in l.split('=')]
                            entry[l_split[0]] = float(l_split[-1])
            except Exception:
                print(f'Error reading file {r["energies"]}')

        def read_Hcorr(entry, r):
            try:
                with open(r['hcorr'], 'r') as f:
                    entry['Hcorr'] = [float(l.split()[-1]) for l in f
                                    if 'Thermal correction to Enthalpy' in l][0]
            except Exception:
                print(f'Error reading file {r["hcorr"]}')

        for r in self.all_species:
            entry = {}
            
            read_energies(entry, r)
            read_Hcorr(entry, r)

            if r != self.target:
                entry['dfH'] = r['dfH']
                entry['u'] = r['u']

            r['data'] = entry

    def run(self, out_dir='./out/', max_rxns=1000):
        S = np.zeros((max_rxns, len(self.get_basis())), dtype=np.int64)
        len_S = ctypes.pointer(ctypes.c_int(0))
        
        rgen.generate(S, len_S, self.get_basis(), self.vectorizer.dim, len(self.get_basis()), max_rxns)
        rxns = S[:int(len_S.contents.value)]
        if len(rxns) > 0:
            rxns = rxns[np.apply_along_axis(lambda row: abs(np.sum(row)) + np.sum(np.abs(row)), 1, rxns).argsort()]

        self.reactions = rxns
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(out_dir + self.target['xyz'].split('/')[-1][:-4] + '.all', 'w') as f:
            for rxn in self.reactions:
                entry = []
                entry.append(self.vectorizer.reaction_to_str(rxn))
                entry.append(abs(sum(rxn)))
                entry.append(sum(abs(rxn)))
                entry.append(entry[1] + entry[2])

                E_sum = {}
                for r in range(len(rxn)):
                    c_frac = -rxn[r].item()/rxn[0].item()
                    E_all = self.all_species[r]['data']
                    
                    for n, e in E_all.items():
                        if n=='u':
                            E_sum[n] = E_sum.get(n, 0) + (c_frac*e)**2
                        else:
                            E_sum[n] = E_sum.get(n, 0) + c_frac*e
                
                if not 'E' in E_sum:
                    E_CV = E_sum['E(CV correction (TZ))']
                    E_IT = E_sum['E(DLPNO-CCSD(T)/TZ-IT)']-E_sum['E(DLPNO-CCSD(T)/CC-PVTZ)']
                    E_SO = E_sum['E(DKH correction)']
                    E_r = E_sum['E(DLPNO-CCSD(T)/CBS)'] + E_CV + E_IT + E_SO
                else:
                    E_CV = 0
                    E_IT = 0
                    E_SO = 0
                    E_r = E_sum['E']
                    
                E_r_HF = E_sum['E(HF/CBS)'] + E_SO
                E_corr_r = E_r - E_r_HF
                
                H_r = E_r + E_sum['Hcorr']
                H_f = E_sum['dfH'] - H_r*eh_to_cal

                u = E_sum['u']**0.5

                entry.append(round(H_f, 3))
                entry.append(round(E_corr_r*eh_to_cal, 3))
                entry.append(round(E_sum['Hcorr']*eh_to_cal, 3))
                entry.append(round(entry[-1]+entry[-2], 3))
                entry.append(round(u, 3))
                entry.append(round(2*u, 3))
                entry.append(round(H_r*eh_to_cal, 3))
                entry.append(0)
                entry.append(round(E_CV*eh_to_cal, 3))
                entry.append(round(E_IT*eh_to_cal, 3))
                entry.append(0)
                entry.append(round(E_SO*eh_to_cal, 3))

                entry.append(self.vectorizer.reaction_to_names(rxn))

                f.write(';'.join(map(str, entry)) + '\n')
