import pandas as pd
import pyomo.environ as pyo

# Lokale importer:
from load_data import last_legering_diameter_data

def test_pyomo():
    model = pyo.ConcreteModel()

    model.x = pyo.Var([1,2], domain=pyo.NonNegativeIntegers)

    model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])

    model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)

    opt = pyo.SolverFactory('glpk')

    opt.solve(model) 

    print("Done solving!")
    model.display()


def main():
    data = last_legering_diameter_data()
    print(data)
    pass


if __name__ == "__main__":
    main()