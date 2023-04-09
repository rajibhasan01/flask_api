"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
from flask import Flask, request, jsonify
import os
import uuid
from PIL import Image
import numpy as np
from flask_cors import CORS


def create_app(config=None):
    app = Flask(__name__)

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})
    # Configure the static folder to serve processed images
    app.config['STATIC_FOLDER'] = 'processed_images'
    app.static_folder = app.config['STATIC_FOLDER']
    app.config['UPLOAD_FOLDER'] = 'uploads'



    # Setup cors headers to allow all domains
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def hello_world():
        return "Hello World"

    @app.route('/process_images', methods=['POST'])
    def process_images():
        # Get the input images from the request
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        image1 = request.files.get('image1')
        image2 = request.files.get('image2')

        # Generate a unique filename for the processed image
        filename = str(uuid.uuid4()) + '.jpg'

        # Save the input images to the server
        image1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg'))
        image2.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg'))

        # Process the images here using your preferred image processing library, e.g. PIL or OpenCV
        processed_image = Image.blend(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')),
                                    Image.open(os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')),
                                    alpha=0.5)
        if not os.path.exists(app.config['STATIC_FOLDER']):
            os.makedirs(app.config['STATIC_FOLDER'])

        # Save the processed image to the server
        processed_image.save(os.path.join(app.config['STATIC_FOLDER'], filename))

        # Return the URL of the processed image
        return jsonify({'url': f'http://localhost:5000/static/{filename}'})


    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
