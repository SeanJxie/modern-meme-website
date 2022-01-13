"""
This script makes memes that conform to the modern standard of humor.

"""

from PIL import Image, ImageDraw, ImageFont
import requests

import io
import random
import base64
import string

import templates

def get_random_image():
    tempchar = [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
    url = "http://i.imgur.com/" + "".join(tempchar) + ".png"

    img_resp = requests.get(url)

    img = Image.open(io.BytesIO(img_resp.content)).convert("RGBA")

    if img.size == (161, 81): # hard code the removed image
        return get_random_image()

    min_res = min(img.size)

    if min_res < 1000:
        scale = int(1000 / min_res)
        img = img.resize((img.size[0] * scale, img.size[1] * scale))

    return img


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
