from flask import Flask, render_template, url_for
import meme_gen

app = Flask(__name__)

@app.route('/')
def index():
    meme_gen.generate()
    return render_template("index.html")

@app.route('/background_process_test')
def background_process_test():
    meme_gen.generate()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)