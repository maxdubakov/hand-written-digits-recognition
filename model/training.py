from model.Load import Load
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
from pickle import dump

TRAINING_SET_SIZE = 60000
TEST_SET_SIZE = 10000
IMAGE_SIZE_PX = 28


def model():
    model = Sequential()
    model.add(Dense(784, activation='relu'))
    # model.add(Dropout(rate=0.5))

    model.add(Dense(98, activation='relu'))
    # model.add(Dropout(rate=0.5))

    model.add(Dense(49, activation='relu'))
    # model.add(Dropout(rate=0.5))

    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


if __name__ == '__main__':
    load = Load('train-images-idx3-ubyte.gz',
                't10k-images-idx3-ubyte.gz',
                'train-labels-idx1-ubyte.gz',
                't10k-labels-idx1-ubyte.gz',
                28)

    X_train, X_test, y_train, y_test = load.read_images_labels(TRAINING_SET_SIZE, TEST_SET_SIZE)

    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    early_stop = EarlyStopping(monitor='loss',
                               mode='min',
                               verbose=1,
                               patience=10)

    estimator = KerasClassifier(build_fn=model, epochs=10, batch_size=100, verbose=1, callbacks=[early_stop])
    print(estimator.get_params())
    estimator.fit(X_train, y_train)

    estimator.model.save('./model/savings/model.h5')
    dump(scaler, open('./model/savings/scaler.pkl', 'wb'))

    losses = pd.DataFrame(estimator.model.history.history)
    losses.plot()
    predictions = estimator.predict(X_test)
    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

    plt.show()
