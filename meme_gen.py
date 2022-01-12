"""
This script makes memes that conform to the modern standard of humor.

"""

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests

import io
import random
import base64

import templates


def get_random_image():
    page_resp = requests.get("https://www.generatormix.com/random-image-generator", timeout=4.0)

    print(page_resp.status_code)

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
