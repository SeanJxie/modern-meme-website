"""
This script makes memes that conform to the modern standard of humor.

"""

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests

import io
import random

import templates


def get_random_image():
    page_resp = requests.get("https://www.generatormix.com/random-image-generator", timeout=4.0)

    if page_resp.content == None:
        return get_random_image()

    parser = BeautifulSoup(page_resp.content, "html.parser")
    img_tag = parser.find("img", {"class": "lazy thumbnail"})

    if img_tag == None:
        return Image.new("RGB", (100, 100))

    img_resp = requests.get(img_tag["data-src"])

    return Image.open(io.BytesIO(img_resp.content))


def overlay_meme_text(img: Image, top: str, bottom: str):
    imWt, imHt = img.size
    
    font = ImageFont.truetype("impact.ttf", 100) # This should be dynamic
    d = ImageDraw.Draw(img)

    # Top
    _, txtHtTop = d.textsize(top, font=font) 

    d.text((imWt / 2, txtHtTop / 2), top, fill="black", font=font, anchor="mm", stroke_width=2) # outline
    d.text((imWt / 2, txtHtTop / 2), top, fill="white", font=font, anchor="mm")

    # Bottom
    _, txtHtBot = d.textsize(bottom, font=font) 

    d.text((imWt / 2, imHt - txtHtBot / 2), bottom, fill="black", font=font, anchor="mm", stroke_width=2) # outline
    d.text((imWt / 2, imHt - txtHtBot / 2), bottom, fill="white", font=font, anchor="mm")

    return img

def get_random_top_bottom():
    rnd_tmp = templates.text[random.randint(0, len(templates.text) - 1)]

    rnd_top = rnd_tmp["top"].replace(
        "[_NOUN]", templates.nouns[random.randint(0, len(templates.nouns) - 1)]
            ).replace(
            "[_ADJ]", templates.adjectives[random.randint(0, len(templates.adjectives) - 1)]
            ).replace(
            "[_PNOUN]", templates.plural_nouns[random.randint(0, len(templates.plural_nouns) - 1)]
            ).replace(
            "[_VERB]", templates.verbs[random.randint(0, len(templates.verbs) - 1)]
            )

    rnd_bot = rnd_tmp["bot"].replace(
        "[_NOUN]", templates.nouns[random.randint(0, len(templates.nouns) - 1)]
            ).replace(
            "[_ADJ]", templates.adjectives[random.randint(0, len(templates.adjectives) - 1)]
            ).replace(
            "[_PNOUN]", templates.plural_nouns[random.randint(0, len(templates.plural_nouns) - 1)]
            ).replace(
            "[_VERB]", templates.verbs[random.randint(0, len(templates.verbs) - 1)]
            )

    return rnd_top, rnd_bot


def generate():
    name = '/tmp/meme.png'

    meme = overlay_meme_text(get_random_image(), *get_random_top_bottom())
    meme.save(name, "PNG")
    
    print('meme generated.')

    return name
