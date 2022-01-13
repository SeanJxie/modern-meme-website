from flask import Flask, render_template

import threading

import meme_gen

app = Flask(__name__)

#CACHE_LIMIT = 100
image_cache = []
threads = []
N_THREADS = 5

def loader():
    while 1:
        image_cache.append(meme_gen.generate())
        print("Cache size:", len(image_cache))

def load_thread():
    for _ in range(N_THREADS):
        th = threading.Thread(target=loader, daemon=True)
        threads.append(th)
        th.start()


@app.route('/')
def index():
    if len(image_cache) > 0: 
        new_img_tag = meme_gen.serve_pil_image(image_cache[0])
        image_cache.pop(0)
        return render_template("index.html", image=new_img_tag)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    load_thread()
    app.run(debug=True, threaded=True)