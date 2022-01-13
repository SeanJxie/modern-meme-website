from flask import Flask, render_template, jsonify

import threading

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

def load_thread():
    for _ in range(N_THREADS):
        th = threading.Thread(target=loader, daemon=True)
        threads.append(th)
        th.start()


app_start = False

@app.route('/')
def index():
    global app_start
    if not app_start:
        print(app_start)
        load_thread()
        app_start = True

    return render_template("index.html")

@app.route('/new_meme')
def post_new_meme():
    if len(image_cache) > 0: 
        new_img_tag = meme_gen.serve_pil_image(image_cache[0])
        image_cache.pop(0)
    else:
        new_img_tag = 'Meme'
        
    data = {'meme': new_img_tag}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)