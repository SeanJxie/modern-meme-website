"""
This script makes memes that conform to the modern standard of humor.

"""

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import flask
import requests

import io
import random
import base64

import templates

def get_random_image():
    # Slow. But, this will do for now...

    url = "https://flrig.beesbuzz.biz/"
    page_resp = requests.get(url)

    parser1 = BeautifulSoup(page_resp.content, "html.parser")
    href_tags = list(filter(lambda s: "https://www.flickr.com/" in s, map(lambda t: t["href"], parser1.find_all("a"))))
    
    href_resp = requests.get(random.choice(href_tags))
    parser2 = BeautifulSoup(href_resp.content, "html.parser")
    img_tag = parser2.find("img")

    if img_tag is None:
        return get_random_image()

    img_resp = requests.get("https:" + img_tag["src"])

    img = Image.open(io.BytesIO(img_resp.content)).convert("RGBA")
    min_res = min(img.size)
    if min_res < 1000:
        print("HERE:", min_res)
        scale = int(1000 / min_res)
        img = img.resize((img.size[0] * scale, img.size[1] * scale))

    return img


def overlay_meme_text(img: Image, top: str, bottom: str):
    imWt, imHt = img.size
    
    font = ImageFont.truetype("impact.ttf", 100) # This should be dynamic
    d = ImageDraw.Draw(img)

    # Top
    _, txtHtTop = d.textsize(top, font=font) 
    print(img.size)
    d.text((imWt / 2, txtHtTop / 2), top, fill="black", font=font, anchor="mm", stroke_width=2) # outline
    d.text((imWt / 2, txtHtTop / 2), top, fill="white", font=font, anchor="mm")

    # Bottom
    _, txtHtBot = d.textsize(bottom, font=font) 

    d.text((imWt / 2, imHt - txtHtBot / 2), bottom, fill="black", font=font, anchor="mm", stroke_width=2) # outline
    d.text((imWt / 2, imHt - txtHtBot / 2), bottom, fill="white", font=font, anchor="mm")

    return img

def get_random_top_bottom():
    rnd_tmp = random.choice(templates.text)

    rnd_top = rnd_tmp["top"].replace(
        "[_NOUN]", random.choice(templates.nouns)
            ).replace(
            "[_ADJ]", random.choice(templates.adjectives)
            ).replace(
            "[_PNOUN]", random.choice(templates.plural_nouns)
            ).replace(
            "[_VERB]", random.choice(templates.verbs)
            )

    rnd_bot = rnd_tmp["bot"].replace(
        "[_NOUN]", random.choice(templates.nouns)
            ).replace(
            "[_ADJ]", random.choice(templates.adjectives)
            ).replace(
            "[_PNOUN]", random.choice(templates.plural_nouns)
            ).replace(
            "[_VERB]", random.choice(templates.verbs)
            )

    return rnd_top, rnd_bot

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, "PNG", quality=100)
    img_io.seek(0)
    img = base64.b64encode(img_io.getvalue()).decode("ascii")
    return f'<img src="data:image/png;base64, {img}" id="meme-image"/>'

def generate():
    return overlay_meme_text(get_random_image(), *get_random_top_bottom())
