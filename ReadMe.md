# Flask app to handle Blob uploads of MP4 files/images.

## Flow
- User makes a network request to application with a Blob file as the body of the request
- The applicaiton keeps the request open, reads the blob, and saves the mp4 locally on the server 
_ `blur_face_video.py` scripg gets trigger and breaks up mp4 frame by frame 
- Runs a model to find a face in the frame, blurs the face and writes new images into a new mp4
- Server sends back the new mp4 and deletes the original

## Setting up Flask
- Make sure pip3 and python3 are set up on your computer
- Activate the virtual environment to set up the python interpreter
```shell script
sh venv/bin/activate
```
- Install requirements from requirements file
```shell script
pip3 install -r requirements.txt
```
- Export the name of the flask server file in your terminal session
```shell script
export FLASK_APP=fb_server.py
```   
- Run the server
```shell script
python3 -m flask run
```

This should activate the server on port 5000
* Reference https://flask.palletsprojects.com/en/1.1.x/quickstart/ for details

## Setting up Docker
- Run `docker build -t faceblur . `
- After the image has built, run `docker run -p 5000:5000 -it faceblur`
- The container should be serving over localhost 5000

## To Do 
- [ ] Deblob object send to pyscript
- [ ] Send data back as blurred video
- [ ] Image url for image uploads
- [ ] Create DockerFile for server code
- [ ] Set up ALB (with https) or APIGW to ping Server
