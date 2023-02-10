from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb://iqbalmp:iqbalmp@ac-azgceyx-shard-00-00.ligsrx6.mongodb.net:27017,ac-azgceyx-shard-00-01.ligsrx6.mongodb.net:27017,ac-azgceyx-shard-00-02.ligsrx6.mongodb.net:27017/?ssl=true&replicaSet=atlas-144b7i-shard-0&authSource=admin&retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbspartaPoliteknik
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