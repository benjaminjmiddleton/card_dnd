# CardGenerator.py
# 
# Run this script from the code folder to delete assets/cards/all_cards and re-generate the cards.
# 

import CardWriter
import xlrd

from Card import Card, read_cards

card_list = read_cards("Cards.xlsx")

CardWriter.generate_cards(card_list, "all_cards")
CardWriter.generate_card_back()