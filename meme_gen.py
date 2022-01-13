"""
This script makes memes that conform to the modern standard of humor.

"""

from math import prod
from PIL import Image, ImageDraw, ImageFont
import requests

import io
import random
import base64
import string
import json

print("LOADING DATA")
with open("nouns.txt") as nf:
    nouns = nf.readlines()
with open("adjectives.txt") as af:
    adjectives = af.readlines()
with open("verbs.txt") as vf:
    verbs = vf.readlines()
with open("adverbs.txt") as adf:
    adverbs = adf.readlines()
with open("text_templates.json") as jsonf:
    templates = json.load(jsonf)["templates"]
print("FINISHED LOADING DATA")

MAX_IMG_RES = 1280 * 720
MIN_IMG_RES = 640 * 480

MAX_ASPECT = 4
MIN_ASPECT = 1/4

def _fetch_single_image():
    tempchar = [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
    url = "http://i.imgur.com/" + "".join(tempchar) + ".png"
    tmp = io.BytesIO(requests.get(url).content)
    tmp.seek(0)
    return Image.open(tmp)


def get_random_image():
    img = _fetch_single_image()
    # hard code the "removed" image and filter files that don't fit our requirements
    aspect = img.size[0]/img.size[1]
    while img.size == (161, 81) or MIN_IMG_RES > prod(img.size) or prod(img.size) > MAX_IMG_RES or MIN_ASPECT > aspect or aspect > MAX_ASPECT:
        img = _fetch_single_image()
    return img.convert("RGBA")

def overlay_meme_text(img: Image, top: str, bottom: str):
    imWt, imHt = img.size
    d = ImageDraw.Draw(img)

    fontsize = 1 
    img_fraction = random.uniform(0.6, 0.9) # get a little spicy with the font size

    if len(top) > len(bottom):
        larget_txt = top
    else:
        larget_txt = bottom

    font = ImageFont.truetype("impact.ttf", fontsize)
    while font.getsize(larget_txt)[0] < img_fraction * img.size[0]:
        fontsize += 1
        font = ImageFont.truetype("impact.ttf", fontsize)

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
    rnd_tmp = random.choice(templates)

    rnd_top = rnd_tmp["top"].replace(
        "[_NOUN]", random.choice(nouns).lower()
            ).replace(
            "[_ADJ]", random.choice(adjectives).lower()
            ).replace(
            "[_VERB]", random.choice(verbs).lower()
            ).replace(
            "[_ADV]", random.choice(adverbs).lower()
            )

    rnd_bot = rnd_tmp["bot"].replace(
        "[_NOUN]", random.choice(nouns).lower()
            ).replace(
            "[_ADJ]", random.choice(adjectives).lower()
            ).replace(
            "[_VERB]", random.choice(verbs).lower()
            ).replace(
            "[_ADV]", random.choice(adverbs).lower()
            )
    
    return ' '.join(rnd_top.split()), ' '.join(rnd_bot.split())


def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, "PNG", quality=100)
    img_io.seek(0)
    img = base64.b64encode(img_io.getvalue()).decode("ascii")
    return f'<img src="data:image/png;base64, {img}" id="meme-image"/>'

def generate():
    return overlay_meme_text(get_random_image(), *get_random_top_bottom())
