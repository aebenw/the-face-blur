from flask import Flask
from flask import request
from flask_cors import CORS
import uuid


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
            content_header = request.headers['Content-Type']
            # Basing content type off of JS blob type: "image/png"
            ctype = content_header.rsplit('/', 1)[-1]
            rand = uuid.uuid4().hex
            fh = open(rand + "." + ctype, "wb")
            fh.write(request.data)
            fh.close()
            return "File saved to server"

        except Exception as e:
            app.logger.debug("e", e)
            return "Unable to save file"
