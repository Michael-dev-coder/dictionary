from flask import Flask, jsonify, render_template, request, send_file
import requests
from gtts import gTTS
from jsonpath_rw import jsonpath, parse

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/define", methods=["POST"])
def define():
    global definition
    word = request.form["word"]
    api_key = "352f3ff0-77a9-4ded-8392-2e6340c65e94"
    url = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # Extract the definition from the API response using jsonpath-rw
        from jsonpath_rw import jsonpath, parse
        definitions = [match.value for match in parse('$..dt[*]').find(data)]
        definition = ', '.join(definitions)
    except:
        # If the definition is not found, use Google to get the definition
        from googlesearch import search
        query = "define " + word
        for url in search(query, num_results=1):
            definition = url

    return render_template("define.html", word=word, definition=definition)


@app.route("/speak", methods=["POST"])
def speak():
    text = request.form["text"]
    tts = gTTS(text)
    tts.save("definition.mp3")
    return send_file("definition.mp3", mimetype="audio/mp3")


if __name__ == "__main__":
    app.run()
