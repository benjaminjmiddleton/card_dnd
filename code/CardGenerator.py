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
    def __init__(self, name, card_type, spell_lv, dnd_class, attribute, desc):
        self.name = name
        self.card_type = card_type
        self.spell_lv = spell_lv
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
        spell_lv = sheet.cell_value(i, 2).strip()
        if spell_lv == '-':
            spell_lv = None
        dnd_class = sheet.cell_value(i, 3).strip()
        class_list = dnd_class.split(", ")
        # if dnd_class == "All":
        #     class_list = CardWriter.CLASSES
        attribute = sheet.cell_value(i, 5).strip()
        attribute_list = attribute.split(", ")
        if attribute == "All":
            attribute_list = ATTRIBUTES
        description = sheet.cell_value(i, 6).strip()

        for cl in class_list:
            for att in attribute_list:
                att = att.strip()
                cl = cl.strip()

                card = Card(name, card_type, spell_lv, cl, att, description)
                card_list.append(card)
    return card_list

card_list = read_cards("Cards.xlsx")

CardWriter.generate_cards(card_list, "all_cards")
CardWriter.generate_card_back()