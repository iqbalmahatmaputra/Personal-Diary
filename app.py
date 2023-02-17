import os
from os.path import join, dirname
from dotenv import load_dotenv

from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
ca = certifi.where()


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI", tlsCAFile=ca)
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/diary", methods=["POST"])
def web_diary_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'picture-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
         'file': filename
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': 'Selamat Data Berhasil Masuk!'})


@app.route("/diary", methods=["GET"])
def web_diary_get():
    diary_list = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles':diary_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)