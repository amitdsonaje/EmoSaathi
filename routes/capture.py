from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from PIL import Image
import io
import base64
import numpy as np
from tensorflow.keras.models import load_model

capture_bp = Blueprint('capture', __name__)

# Load the pre-trained model
model = load_model('my_model.h5')

class_options = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "neutral",
    5: "sad",
    6: "surprise"
}

"""
convert the image to grayscale, resize to 48x48 pixels, reshape to match the model input and then normalize the image.
"""
def preprocess_image(image):
    img = Image.open(image).convert('L')  
    img = img.resize((48, 48))  
    img_array = np.array(img)
    img_array = img_array.reshape(1, 48, 48, 1)  
    return img_array / 255.0  

@capture_bp.route('/', methods=['GET', 'POST'])
def capture():
    if request.method == 'POST':
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])

        # Load image from the binary data
        image = Image.open(io.BytesIO(image_data))

        # Resize the image to the required dimensions (48x48) and convert to grayscale
        image = image.resize((48, 48)).convert('L')

        # Define a directory to save the captured images
        save_dir = 'captured_images'
        os.makedirs(save_dir, exist_ok=True)

        # Save the image
        filename = os.path.join(save_dir, 'captured_photo.png')
        image.save(filename)

        # Preprocess the image and make a prediction
        img = preprocess_image(filename)
        pred = model.predict(img)
        pred_label = pred.argmax()  
        print(pred)
        print("Predicted label: ",class_options[pred_label])
        # Store the predicted label in the session
        session['selected_class'] = int(pred_label)

        return redirect(url_for('chat.chat'))

    return render_template('capture.html')

