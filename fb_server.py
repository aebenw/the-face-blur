import io
from flask import Flask, request, send_file
from flask_cors import CORS
import uuid
from blur_face import blur_image


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
            # Basing content type off of JS blob type: "image/png"
            meme_type = request.headers['X-Content-Type']
            ctype = meme_type.rsplit('/', 1)[-1]
            rand = uuid.uuid4().hex
            file_name = rand + "." + ctype
            fh = open(file_name, "wb")
            fh.write(request.data)
            fh.close()
            # TODO: IF ctype == .png / jpeg / etc etc - go to image
            # TODO: IF ctype == .mp4 / etc etc - go to video
            new_file = blur_image(file_name)
            with open(new_file, 'rb') as bites:
                return send_file(
                    io.BytesIO(bites.read()),
                    attachment_filename=new_file,
                    mimetype=meme_type
                )

        except Exception as e:
            app.logger.debug("e", e)
            return "Unable to save file"
