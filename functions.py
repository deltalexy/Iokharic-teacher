import requests
import os
import string
import random
from PIL import Image

def iokharic_downloader():
    characters = [*string.ascii_uppercase, *[str(i) for i in range(10)]]
    for char in characters:
        charpath = os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'iokharic-{}.png'.format(char))
        response = requests.get("https://geocachen.nl/wp-content/uploads/2023/03/Iokharic-{}.png".format(char))
        with open(charpath, mode="wb") as file:
            file.write(response.content)
        img = Image.open(charpath)
        cropped_img = img.crop((35, 0, 115, 150))
        cropped_img.save(charpath)

def wordlist_downloader():
    response = requests.get("https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt")
    with open(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'wordlist.txt'), mode="wb") as file:
        file.write(response.content)

def generate_wordlist():
    with open(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'wordlist.txt'), mode="r") as file:
        wordlist = file.read().split('\n')
    return wordlist

def symbollink(character):
    return os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'Iokharic-{}.png'.format(character))

def randomcharacter():
    return random.choice([*string.ascii_uppercase, *[str(i) for i in range(10)]])

def get_sample_characters():
    sample = random.sample([*string.ascii_uppercase, *[str(i) for i in range(10)]], 4)
    correct = random.choice(sample)
    return correct, sample

def get_word(listy):
    charcount = 100
    while charcount > 10:
        word = random.choice(listy)
        charcount = len(word)
    return word

def iokharic_word(word):
    picturelist = []
    for letter in word:
        picturelist.append(Image.open(symbollink(letter.upper())))

    combined_width = len(picturelist)*picturelist[0].width
    combined_height = picturelist[0].height
    combined_image = Image.new('RGBA', (combined_width, combined_height))

    for i in range(len(picturelist)):
        combined_image.paste(picturelist[i], (i*picturelist[0].width, 0))
        combined_image.save(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'temp.png'))