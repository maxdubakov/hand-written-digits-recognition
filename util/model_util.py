from tensorflow.keras.models import load_model
from pickle import load
import numpy as np


def predict(image: np.array):
    scaler = load(open('../model/savings/scaler.pkl', 'rb'))
    model = load_model('../model/savings/model.h5')

    image = image.reshape(-1, 784)

    image = scaler.transform(image)
    predictions = model.predict(image)
    print([np.round(d, 2) for d in predictions])
    prediction = np.argmax(predictions)
    return prediction

