# CardWriter.py
#
# Contains methods for generating card images.
#

from PIL import Image, ImageDraw, ImageFont
import os
from shutil import rmtree

WIDTH = int(4096 / 10)
HEIGHT = int(4096 / 7)
NATURALS_TO_100 = []
for i in range(100):
    NATURALS_TO_100.append(str(i))
KEYWORDS_ITALIC = [
    "Exhaust",
    "If",
    "Able",
    "Inflict",
    "Negate",
    "Pacify",
    "Persistent",
    "Prevent",
    "Simple",
    "Unreactable",
    "Useless",
    "Wound",
    "Charge",
    "Ward",
    "Strength",
    "Rooted",
    "Grappled",
    "Grappling",
    "Laughter",
    "Fire",
    "Combo:",
    "Channel:",
    "Thorns",
    "Prone",

]
for i in range(len(KEYWORDS_ITALIC)):
    KEYWORDS_ITALIC.append(KEYWORDS_ITALIC[i]+".")
    KEYWORDS_ITALIC.append(KEYWORDS_ITALIC[i]+",")
KEYWORDS_BOLD = [
    "STR",
    "DEX",
    "CON",
    "INT",
    "WIS",
    "CHA",
    "X",
    "+",
]
for i in range(len(KEYWORDS_BOLD)):
    KEYWORDS_BOLD.append(KEYWORDS_BOLD[i]+".")
    KEYWORDS_BOLD.append(KEYWORDS_BOLD[i]+",")
CLASSES = [
    "BBN",
    "BRD",
    "CLR",
    "DRD",
    "FTR",
    "MNK",
    "PAL",
    "RGR",
    "ROG",
    "SOR",
    "WIZ",
    "WLK",
]
SCM_DICT = {
    "BRD":"CHA",
    "CLR":"WIS",
    "DRD":"WIS",
    "PAL":"CHA",
    "RGR":"WIS",
    "SOR":"CHA",
    "WIZ":"INT",
}

# @param folder_name: name of folder within assets/cards/ to be deleted and re-generated full of cards from card_list
def generate_cards(card_list, folder_name):
    text_color = "#BBBBBB"
    class_font = ImageFont.truetype("arial.ttf", 36)
    type_font = ImageFont.truetype("arial.ttf", 32)
    type_y = 54
    attr_font = ImageFont.truetype("arial.ttf", 36)
    desc_font = ImageFont.truetype("arial.ttf", 24)
    desc_bold = ImageFont.truetype("arialbd.ttf", 24)
    desc_italic = ImageFont.truetype("ariali.ttf", 24)
    spell_font = ImageFont.truetype("arial.ttf", 20)
    
    # delete and re-make assets/cards/folder_name/
    if not os.path.exists("assets/cards"):
        os.mkdir("assets/cards")
    if os.path.exists("assets/cards/"+folder_name):
        rmtree("assets/cards/"+folder_name)

    try:
        os.mkdir("assets/cards/"+folder_name)
    except FileExistsError:
        pass

    for cl in CLASSES:
        try:
            os.mkdir("assets/cards/"+folder_name+"/"+cl)
        except FileExistsError:
            pass
    try:
        os.mkdir("assets/cards/"+folder_name+"/Other")
    except FileExistsError:
        pass

    # create card image
    for card in card_list:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#FFFFFF')
        canvas = ImageDraw.Draw(img)

        # draw name
        name_font = ImageFont.truetype("arial.ttf", 48)
        text_width, text_height = canvas.textsize(card.name, font=name_font)
        if text_width > WIDTH:
            size = 48
            while text_width > WIDTH:
                size -= 4
                name_font = ImageFont.truetype("arial.ttf", size)
                text_width, text_height = canvas.textsize(card.name, font=name_font)
            x = WIDTH / 2 - text_width / 2
            y = (48 - size) / 2
            canvas.text((x, y), card.name, font=name_font, fill=text_color)
        else:
            x = WIDTH / 2 - text_width / 2
            y = 0
            canvas.text((x, y), card.name, font=name_font, fill=text_color)

        # draw type
        text_width, text_height = canvas.textsize(card.card_type, font=type_font)
        x = WIDTH / 2 - text_width / 2
        y = type_y
        canvas.text((x, y), card.card_type, font=type_font, fill=text_color)

        # draw class
        if card.dnd_class != '-':
            text_width, text_height = canvas.textsize(card.dnd_class, font=class_font)
            x = 2
            y = HEIGHT - text_height - 2
            canvas.text((x, y), card.dnd_class, font=class_font, fill=text_color)

        # draw attribute
        text_width, text_height = canvas.textsize(card.attribute, font=attr_font)
        x = WIDTH - text_width - 2
        y = HEIGHT - text_height - 2
        if card.attribute == "SCM":
            canvas.text((x, y), SCM_DICT[card.dnd_class], font=attr_font, fill=text_color)
        else:
            canvas.text((x, y), card.attribute, font=attr_font, fill=text_color)

        # draw description
        desc_list = card.desc.split(' ')
        it = iter(desc_list)
        line_y = 0
        word = None
        done = False
        while desc_list:
            if word:
                line = [word]
            else:
                line = []
            while True:
                try:
                    word = next(it)
                except StopIteration:
                    done = True
                    break
                text_width, text_height = canvas.textsize(' '.join(line)+' '+word, font=desc_font)
                # if we can fit the word on the line
                if text_width < WIDTH - 20:            
                    line.append(word)
                # otherwise, start the next line with word
                else:
                    break
            # draw the line
            text_width, text_height = canvas.textsize(' '.join(line), font=desc_font)
            x = WIDTH / 2 - text_width / 2
            y = HEIGHT / 2 + line_y
            line_y += text_height
            for word_to_draw in line:
                if word_to_draw == "SCM":
                    word_to_draw = SCM_DICT[card.dnd_class]
                if word_to_draw in NATURALS_TO_100 or word_to_draw in KEYWORDS_BOLD:
                    text_width, text_height = canvas.textsize(word_to_draw+' ', font=desc_bold)
                    canvas.text((x, y), word_to_draw, font=desc_bold, fill=text_color)
                elif word_to_draw in KEYWORDS_ITALIC:
                    text_width, text_height = canvas.textsize(word_to_draw+' ', font=desc_italic)
                    canvas.text((x, y), word_to_draw, font=desc_italic, fill=text_color)
                else:
                    text_width, text_height = canvas.textsize(word_to_draw+' ', font=desc_font)
                    canvas.text((x, y), word_to_draw, font=desc_font, fill=text_color)
                x += text_width

            if done:
                break

        # draw pack
        if card.pack and card.pack != '-':
            text_width, text_height = canvas.textsize(card.pack, font=spell_font)
            x = WIDTH / 2 - text_width / 2
            y = HEIGHT - text_height - 2
            canvas.text((x, y), card.pack, font=spell_font, fill=text_color)

        # save image
        img_path = "assets/cards/"+folder_name
        if card.dnd_class in CLASSES:
            img_path += "/"+card.dnd_class
        else:
            img_path += "/Other"
        if card.pack:
            img_path += "/"+card.pack
        try:
            os.mkdir(img_path)
        except FileExistsError:
            pass
        img_path += "/"+card.name+".png"
        cnt = 1
        if os.path.exists(img_path):
            img_path = img_path[:-4] + str(cnt) + ".png"
            while(os.path.exists(img_path)):
                img_path = img_path[:-5] + str(cnt) + ".png"
                cnt += 1
        img.save(img_path)

def generate_card_back():
    font = ImageFont.truetype("arial.ttf", 72)
    img = Image.new('RGB', (WIDTH, HEIGHT), color="#AAAAFF")
    canvas = ImageDraw.Draw(img)

    str_to_draw = "Card"
    text_width, text_height = canvas.textsize(str_to_draw, font=font)
    x = WIDTH / 2 - text_width / 2
    y = HEIGHT / 2 - text_height
    canvas.text((x, y), str_to_draw, font=font, fill='#AA55FF')

    str_to_draw = "DnD"
    text_width, text_height = canvas.textsize(str_to_draw, font=font)
    x = WIDTH / 2 - text_width / 2
    y = HEIGHT / 2
    canvas.text((x, y), str_to_draw, font=font, fill='#AA55FF')

    img.save("assets/cards/back.png")