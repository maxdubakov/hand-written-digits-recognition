from os.path import join
import gzip as g
import numpy as np
import matplotlib.pyplot as plt

def digit_to_input(data_in) -> np.array:
    rows = len(data_in)
    cols = len(data_in[0])
    return data_in.reshape(rows * cols)


class Load:

    def __init__(self, images_train_name, images_test_name, labels_train_name, labels_test_name, image_size):
        self.images_train_path = join('./images', images_train_name)
        self.images_test_path = join('./images', images_test_name)
        self.labels_train_path = join('./labels', labels_train_name)
        self.labels_test_path = join('./labels', labels_test_name)

        self.IMAGE_SIZE_PX = image_size

    def read_images_labels(self, train_size, test_size):
        output = list()

        # READING TRAIN IMAGES
        with g.open(self.images_train_path, 'rb') as file:
            file.read(16)
            buf = file.read(self.IMAGE_SIZE_PX * self.IMAGE_SIZE_PX * train_size)
            data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
            print(data[0])
            data = data.reshape(train_size, self.IMAGE_SIZE_PX, self.IMAGE_SIZE_PX, 1)
        output.append(np.array([digit_to_input(digit) for digit in data]))

        # READING TEST IMAGES
        with g.open(self.images_test_path, 'rb') as file:
            file.read(16)
            buf = file.read(self.IMAGE_SIZE_PX * self.IMAGE_SIZE_PX * test_size)
            data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
            data = data.reshape(test_size, self.IMAGE_SIZE_PX, self.IMAGE_SIZE_PX, 1)
        output.append(np.array([digit_to_input(digit) for digit in data]))

        # READING TRAIN LABELS
        with g.open(self.labels_train_path, 'rb') as file:
            file.read(8)
            buf = file.read(train_size)
            data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        output.append(np.array(data))

        # READING TEST LABELS
        with g.open(self.labels_test_path, 'rb') as file:
            file.read(8)
            buf = file.read(test_size)
            data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        output.append(np.array(data))

        return tuple(output)

    # PRINT DIGIT FUNCTION
    def print_digit(self, data_in):
        data_in = data_in.reshape(1, self.IMAGE_SIZE_PX, self.IMAGE_SIZE_PX, 1)
        image = np.asarray(data_in).squeeze()
        plt.imshow(image)
        plt.show()
