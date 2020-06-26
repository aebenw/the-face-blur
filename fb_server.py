from flask import Flask
from flask import request
from flask_cors import CORS
import base64
import json
import codecs


print(__name__)
app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'\

@app.route('/video', methods=['POST'])
def deblob():
    if request.data is not None:
        try:
            # TODO: make file name unique
            fh = open("imageToSave.png", "wb")
            fh.write(request.data)
            fh.close()
            return "File saved to server"

        except Exception as e:
            app.logger.debug("e", e)
            return "Unable to save file"
