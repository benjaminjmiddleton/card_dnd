# MonsterManager.py
#
# This script should allow you to run many enemies more effectively in card d&d than you would in TTS.
#

import xlrd

from Card import Card, read_cards

class Monster:
    def __init__(self, name, hp, _str, dex, con, _int, wis, cha, deck):
        self.name = name
        self.hp = hp
        self.str = _str
        self.dex = dex
        self.con = con
        self.int = _int
        self.wis = wis
        self.cha = cha
        self.deck = deck

# prompts the user for the needed monsters and returns the corresponding list of Monster objects
def get_monsters(monster_manual, valid_monster_names, card_list):
    monster_list = []

    # Get list of names of monsters to add
    print('Adding monsters to encounter.')
    adding_monsters = True
    while adding_monsters:
        monster_name = input('Monster to add: ')
        if monster_name in valid_monster_names:
            monster_list.append(monster_name)
        else:
            print("Not a valid monster name!")
        another = input("Add another monster (y)/n: ")
        if 'n' in another or 'N' in another:
            adding_monsters = False

    # Get monster data from .xlsx files
    for monster_it in range(len(monster_list)):
        monster = monster_list[monster_it]
        sheet = monster_manual.sheet_by_name(monster)

        deck = []
        hp = _str = dex = con = _int = wis = cha = None

        name = sheet.cell_value(0, 0)
        for i in range(50):
            for j in range(10):
                try:
                    if sheet.cell_value(i, j) == 'Hit Points':
                        hp = sheet.cell_value(i, j+1)
                    if sheet.cell_value(i, j) == 'STR':
                        _str = sheet.cell_value(i+1, j)
                    if sheet.cell_value(i, j) == 'DEX':
                        dex = sheet.cell_value(i+1, j)
                    if sheet.cell_value(i, j) == 'CON':
                        con = sheet.cell_value(i+1, j)
                    if sheet.cell_value(i, j) == 'INT':
                        _int = sheet.cell_value(i+1, j)
                    if sheet.cell_value(i, j) == 'WIS':
                        wis = sheet.cell_value(i+1, j)
                    if sheet.cell_value(i, j) == 'CHA':
                        cha = sheet.cell_value(i+1, j)
                    # Get deck data
                    if sheet.cell_value(i, j) == 'Example Deck':
                        row = i
                        cell_value = sheet.cell_value(row+1, j)
                        while cell_value:
                            x_ind = cell_value.rfind('x')
                            copies = int(cell_value[x_ind+1:])
                            card_name = cell_value[:x_ind-1]
                            my_card = None
                            for card in card_list:
                                if card.name == card_name:
                                    my_card = card
                                    break
                            if not my_card:
                                raise Exception('Card Not Found')
                            count = 0
                            while count < copies:
                                deck.append(my_card)
                                count += 1
                            row += 1
                            cell_value = sheet.cell_value(row+1, j)
                except IndexError:
                    pass
        monster_list[monster_it] = Monster(name, hp, _str, dex, con, _int, wis, cha, deck)
    return monster_list

def main():
    monster_manual = xlrd.open_workbook("MonsterManual.xlsx")
    monster_names = monster_manual.sheet_names()
    card_list = read_cards("Cards.xlsx")
    encounter_monsters = get_monsters(monster_manual, monster_names, card_list)

    for monster in encounter_monsters:
        print(monster.__dict__)
    #     for card in monster.deck:
    #         print(card.__dict__)

    # monster_manual.sheet_by_name()
    
if __name__ == "__main__":
    main()
