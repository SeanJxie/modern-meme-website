from flask import Flask, render_template, jsonify

import threading
import time

import meme_gen



app = Flask(__name__)

#CACHE_LIMIT = 100
image_cache = []
threads = []
N_THREADS = 2

def loader():
    while 1:
        image_cache.append(meme_gen.generate())
        print("Cache size:", len(image_cache))

def load_threads():
    for _ in range(N_THREADS):
        th = threading.Thread(target=loader, daemon=True)
        threads.append(th)
        th.start()

    print(f"Filled threads with {len(threads)} threads.")


@app.route('/')
def index():
    print("Loading threads...")
    load_threads()
    print("Threads loaded.")
    return render_template("index.html")


@app.route('/new_meme')
def post_new_meme():
    start = time.time()
    print("Loading image...")
    if len(image_cache) > 0: 
        new_img_tag = meme_gen.serve_pil_image(image_cache[0])
        image_cache.pop(0)
    else:
        new_img_tag = "Uh oh, you've ran out of memes! Please wait for more to generate and try again :)"
        
    data = {'meme': new_img_tag}
    print(f"Image load took {time.time() - start}s")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)