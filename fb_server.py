from flask import Flask
from flask import request
from flask_cors import CORS
import json


print(__name__)
app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'\

@app.route('/video', methods=['POST'])
def deblob():
    app.logger.debug(request)
    if request.data is not None:
        try:
            blobObject = request.get_data()
            app.logger.debug("Blobonj", blobObject)
            # f = open("myfile.mp4", "w")
            # f.write(blobObject)
        except Exception as e:
            app.logger.debug("e", e)


    # print("REQUEST", request.form)
    # print("REQUEST", request.get_data())
    # print("REQUEST", request.json)
    return "Trying"
