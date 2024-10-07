from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img

model = load_model('my_model.h5')
# predictions = model.predict(new_data)
label = ['angry','disgust','fear','happy','neutral','sad','surprise']

def ef(image):
    try:
        img = load_img(image, color_mode="grayscale")
        feature = np.array(img)
        feature.reshape(1,48,48,1)
        return feature/255.0
    except Exception as e:
        print(f"Error loading image {image}: {e}")
    


image = 'captured_images/captured_photo.png'

img = ef(image)  
img = np.expand_dims(img, axis=-1)  
img = np.expand_dims(img, axis=0)  
pred = model.predict(img)
pred_label = label[pred.argmax()]

