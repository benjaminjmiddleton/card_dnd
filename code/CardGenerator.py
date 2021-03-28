# CardGenerator.py
# 
# Run this script from the code folder to delete assets/cards/ and re-generate them.
# 

import CardWriter
import xlrd

ATTRIBUTES = [
    "STR",
    "DEX",
    "CON",
    "INT",
    "WIS",
    "CHA"
]

class Card:
    def __init__(self, name, card_type, pack, dnd_class, attribute, desc):
        self.name = name
        self.card_type = card_type
        self.pack = pack
        self.dnd_class = dnd_class
        self.attribute = attribute
        self.desc = desc

def read_cards(wb_path):
    wb = xlrd.open_workbook(wb_path)
    sheet = wb.sheet_by_index(0)

    card_list = []
    for i in range(1, sheet.nrows):
        name = sheet.cell_value(i, 0).strip()
        card_type = sheet.cell_value(i, 1).strip()
        pack = str(sheet.cell_value(i, 2)).strip()
        if pack == '-':
            pack = None
        dnd_class = sheet.cell_value(i, 3).strip()
        class_list = dnd_class.split(", ")
        # if dnd_class == "All":
        #     class_list = CardWriter.CLASSES
        attribute = sheet.cell_value(i, 4).strip()
        attribute_list = attribute.split(", ")
        if attribute == "All":
            attribute_list = ATTRIBUTES
        description = sheet.cell_value(i, 5).strip()

        for cl in class_list:
            for att in attribute_list:
                att = att.strip()
                cl = cl.strip()

                card = Card(name, card_type, pack, cl, att, description)
                card_list.append(card)
    return card_list

card_list = read_cards("Cards.xlsx")

CardWriter.generate_cards(card_list, "all_cards")
CardWriter.generate_card_back()