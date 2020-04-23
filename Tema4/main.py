from flask import Flask, render_template, request, flash, redirect, send_file, session
from pymongo import MongoClient
from Cryptodome.Hash import SHA256
import os
from azure.storage.blob import BlockBlobService
import datetime
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import requests

app = Flask(__name__)

app.secret_key = b""
app.permanent_session_lifetime = datetime.timedelta(days=365)


mongo_uri = ""
client = MongoClient(mongo_uri)
db = client['']
user_collection = db['']
photos_collection = db['']

blob_service = BlockBlobService(account_name="", account_key="")

computervision_client = ComputerVisionClient(endpoint="", credentials="")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_to_find = {'username': username, 'password': SHA256.new(password.encode(encoding='utf-8')).hexdigest()}
        login = user_collection.find_one(user_to_find)
        if login is not None:
            session['user'] = username
            return redirect('/storage')
        else:
            return render_template('login.html', login_error="Email or password incorrect!")
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['passwordConfirm']
        print(username, password, confirm_password)
        if len(password) < 6:
            return render_template('register.html', short_password_error="Password should be at least 6 characters!")
        if password == confirm_password:
            query_result = user_collection.find_one({'username': username})
            if query_result is None:
                new_user = {'username': username, 'password': SHA256.new(password.encode(encoding='utf-8')).hexdigest()}
                user_id = user_collection.insert_one(new_user).inserted_id
                return redirect("/")
            else:
                return render_template('register.html', used_data_error="Credentials already in use!")
        else:
            return render_template('register.html', passwords_error="Passwords don't match!")
    return render_template('register.html')


@app.route('/storage', methods=['POST', 'GET'])
def store_search():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        if request.files:
            file_to_upload = request.files["file"]
            extension = os.path.splitext(file_to_upload.filename)[1]
            name = os.path.splitext(file_to_upload.filename)[0]
            if extension.lower() not in ['.jpg', '.png', '.bmp', '.jpeg']:
                return render_template('file_storage.html', upload_error="You have to choose a photo!", username=session['user'])

            generator = blob_service.list_blobs("photos")
            if session['user'] + "/" + file_to_upload.filename in [blob.name for blob in generator]:
                return render_template('file_storage.html', upload_error="You have already a photo with the same name!", username=session['user'])

            blob_service.create_blob_from_stream("photos", session['user'] + "/" + file_to_upload.filename, file_to_upload.stream)
            ref = 'https://' + "" + '.blob.core.windows.net/' + "photos" + '/' + session['user'] + "/" + file_to_upload.filename
            description_results = computervision_client.describe_image(ref)
            description = ""
            if len(description_results.captions) == 0:
                description = "No description detected."
            else:
                for caption in description_results.captions:
                    info = caption.text[0].upper() + caption.text[1:]
                    description = info + "\n"

            language = request.form.get('language')
            result = translate(description, language)[0]['translations'][0]['text']

            new_photo = {"photo_name": file_to_upload.filename, "user": session['user'], "tags": str(description_results.tags)}
            photo_id = photos_collection.insert_one(new_photo).inserted_id
            return render_template('file_storage.html', image_url=ref, photo_description=result, username=session['user'])

    return render_template('file_storage.html', username=session['user'])


def translate(text, lang):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + lang
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': "",
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)
