import numpy as np
from flask import Flask, request, jsonify, render_template,Response
import pickle
from feature import FeatureExtraction 
from sklearn import *

app = Flask(__name__,template_folder='template')
model = pickle.load(open('Phishing.pkl', 'rb'))

@app.route('/')
def predict1_response():
    return render_template('index.html')

@app.route('/predict')
def predict_response():
    return render_template('web.html')

@app.route('/y_predict',methods=['GET','POST'])
def y_predict_response():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        url = request.form['URL']
        checkprediction = FeatureExtraction(url)
        prediction = model.predict(np.array(checkprediction.features).reshape(-1,30))
        output=prediction[0]
        print(prediction)
        
        if(output==1):
            prediction="Your are safe!!  This is a Legitimate Website."
        else:
            prediction="You are on the wrong site. Be cautious!"
        return render_template('web.html', prediction_text='{}'.format(prediction),url=url)
    return request.json

@app.route('/predict_api',methods=['POST'])
def predict_api_response():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(**output.json)

if __name__=="__main__":
    app.run(host='localhost', debug=True, threaded=False)