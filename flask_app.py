from flask import Flask, render_template, jsonify
import meme_gen

app = Flask(__name__)

@app.route('/')
def index():
    new_img_tag = meme_gen.serve_pil_image(meme_gen.generate())
    return render_template("index.html", image=new_img_tag)

@app.route('/new_meme')
def post_new_meme():
    new_img_tag = meme_gen.serve_pil_image(meme_gen.generate())
    data = {'meme': new_img_tag}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)