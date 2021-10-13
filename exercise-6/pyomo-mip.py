from typing import Dict
# from pyomo.core import expr
import pyomo.environ as pyo
import numpy as np

# Lokale importer:
from process_data import last_legering_diameter_data, skriv_løsning_til_fil

def test_pyomo():
    model = pyo.ConcreteModel()

    model.x = pyo.Var([1,2], domain=pyo.NonNegativeIntegers)

    model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])

    model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)

    opt = pyo.SolverFactory('glpk')

    opt.solve(model) 

    print("Done solving!")
    model.display()


def bygg_basismodell(data: Dict[str, list]) -> pyo.Model:
    modell = pyo.ConcreteModel("BasisModell")

    diameter_summer = data["diameter_andel_sum"]; legerings_summer = data["legerings_andel_sum"]

    modell.Diametere = range(len(diameter_summer))
    modell.Legeringer = range(len(legerings_summer))

    # Teller rader først: X_ij = Andel (diameter[i], legering[j])
    modell.X = pyo.Var(modell.Diametere, modell.Legeringer, domain=pyo.NonNegativeReals)

    # Legg til begrensning på diameter-summer:
    # Må holde for hvert element i 'modell.Diametere' når vi summer over modell.Legeringer:
    def diameter_betingelse(m: pyo.Model, diameter_i: int):
        return sum(m.X[diameter_i, j] for j in m.Legeringer) == diameter_summer[diameter_i]
    modell.diameterbegrensning = pyo.Constraint(modell.Diametere, rule=diameter_betingelse)

    # Legg til begrensning på legerings-summer. 
    # Må holde for hvert element i 'modell.Legeringer' når vi summer over modell.Diametere:
    def legerings_betingelse(m: pyo.Model, legering_j: int):
        return sum(m.X[i, legering_j] for i in m.Diametere) == legerings_summer[legering_j]
    modell.legeringsbegrensing = pyo.Constraint(modell.Legeringer, rule=legerings_betingelse)

    # Legg til triviellt objektiv: min 0
    modell.null_objektiv = pyo.Objective(expr = 0.0)

    return modell


def løs_modell(m: pyo.Model):
    opt = pyo.SolverFactory('glpk')
    opt.solve(m) 


def løs_og_vis_frem_modell(m: pyo.Model):
    print("Beging solving:\n")
    løs_modell(m)
    print("\nDone solving!")
    m.display()


def problem_1(skriv_til_fil=False, vis_modell=False):
    data = last_legering_diameter_data()
    basis_modell = bygg_basismodell(data)

    if vis_modell:
        løs_og_vis_frem_modell(basis_modell)
    else:
        løs_modell(basis_modell)

    X_matrix = np.array([[basis_modell.X[i, j].value for j in basis_modell.Legeringer] for i in basis_modell.Diametere], dtype=float)
    print(f"Basismodell løsnings-matrise:\n{X_matrix}\n")

    if skriv_til_fil:
        skriv_løsning_til_fil(basis_modell, "Basismodell", "D5")


def main():
    problem_1()

if __name__ == "__main__":
    main()