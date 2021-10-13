import openpyxl as xl
import pyomo.environ as pyo

from openpyxl.utils import column_index_from_string, coordinate_to_tuple

def last_legering_diameter_data():
    wb = xl.load_workbook("Produkt_miks.xlsx")

    # sheet_names = wb.get_sheet_names()

    basis_sheet = wb.get_sheet_by_name("Legering-Diameter-Data")

    # diameter_names = [cell[0].value for cell in basis_sheet["A2:A6"]]
    # diameter_values = [cell[0].value for cell in basis_sheet["B2:B6"]]

    # Extract diameters and diameter percentages: 
    diameter_navn = []
    diametere = []
    for row in basis_sheet.iter_rows(min_row=2, max_row=6, min_col=1, max_col=2):
        diameter_navn.append(row[0].value)
        diametere.append(row[1].value)

    legerings_navn = []
    legeringer = []
    for row in basis_sheet.iter_rows(min_row=2, max_row=5, min_col=3, max_col=4):
        legerings_navn.append(row[0].value)
        legeringer.append(row[1].value)

    return {"diameter_andel_sum": diametere, "diameter_navn": diameter_navn, "legerings_andel_sum": legeringer, "legerings_navn": legerings_navn}


def skriv_løsning_til_fil(m: pyo.Model, sheet_name: str, upper_left_corner_cell: str, filename="Produkt_miks.xlsx"):
    rad, kolonne = coordinate_to_tuple(upper_left_corner_cell)

    wb = xl.load_workbook("Produkt_miks.xlsx")
    sheet = wb.get_sheet_by_name(sheet_name)

    løsning = m.X
    for i in m.Diametere:
        for j in m.Legeringer:
            sheet.cell(rad + i, kolonne + j, value = løsning[i, j].value)
    wb.save(filename=filename)

# skriv_løsning_til_fil(None, None, None)