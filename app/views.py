import flask
from flask import render_template
from app import app
from app.ImageAnnotator import get_emotions
from app.ImageAnnotator import get_landmark
import request
#===================================================================================
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import url_for
import pandas as pd



photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route('/')
@app.route('/index')
def index():
    print("Rendering index...")
    parameters = {'face_request':False,
                  'monument_request':False}

    return render_template('index.html',
                           parameters=parameters,
                           title='Home')


@app.route('/monument-form')
def monument_form():
    return render_template('index.html',
                           name='monument_url')

@app.route('/face-form')
def face_form():
    return render_template('index.html',
                           name='face_url')


@app.route('/monument-results', methods=['POST'])
def monument_results():
    recibed_url = request.form['monument_url']
    print(recibed_url)

    monument_results = get_landmark(image_url=recibed_url)
    print(monument_results)

    return render_template('index.html',
                           title='Monument results',
                           imageurl=recibed_url,
                           monument_results=monument_results)


@app.route('/face-results', methods=['POST'])
def face_results():
    recibed_url = request.form['face_url']

    emotions_response = get_emotions(image_url=recibed_url)
    emotions = dict(emotions_response[0])
    series = pd.Series(emotions)
    series.sort_values(inplace=True, ascending=False)
    emotions_dict = series.to_dict()

    return render_template('index.html',
                           title='Face results',
                           imageurl=recibed_url,
                           face_results=emotions_dict)


@app.route('/form-face', methods=['POST'])
def evaluate_face():
    recibed_url = request.form['text']

    emotions_response = get_emotions(recibed_url)
    emotions = dict(emotions_response[0])
    series = pd.Series(emotions)
    series.sort_values(inplace=True, ascending=False)
    emotions_dict = series.to_dict()

    # return emotions
    return render_template('postform.html',
                           title='Loaded image',
                           imageurl=recibed_url,
                           emotions=emotions_dict)







#