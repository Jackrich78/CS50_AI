import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy and array with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # initialise empty list for images_data
    images_data = []
    # initialise empty list for labels_data
    labels_data = []

    # for loop going through num_categories - 1
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))
        # loop through each  file
        for image_name in os.listdir(category_path):
            # determine exact location for each file in directory
            image_path = os.path.join(category_path, image_name)
                        
            # for all files in the category directory:
            # read image using cv2.imread
            image = cv2.imread(image_path)
            # resize image to (IMG_WIDTH x IMG_HEIGHT x 3) cv2.resize?  also tf.keras.layers.Resizing
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            # add image to image_data list
            images_data.append(image)
            # add category label to labels_data and convert to integer
            labels_data.append(int(category))   

    # convert image_data and label_data to numpy for tensorflow compatibility
    images_data = np.array(images_data)
    labels_data = np.array(labels_data)

    # return image_data, label_data
    return images_data, labels_data

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a Sequential model
    model = tf.keras.models.Sequential()

    # ensure it accepts the input shape of our image (IMG_WIDTH, IMG_HEIGHT, 3)
    model.add(tf.keras.layers.Input(
        shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # Add a convolutional layer
    model.add(tf.keras.layers.Conv2D( 
        # includes kernel size, and relu activiation
        filters=64,
        kernel_size=(5,5),
        activation='relu',
    ))
        
    # Add a max pooling layer to reduce spatial dimensions
    model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2,2),
        strides=(2,2), # common to have the same as pool size
        padding='same' # valid = no padding
    ))

    # Second convultional and pooling layers
        # Add a convolutional layer
    model.add(tf.keras.layers.Conv2D( 
        # includes kernel size, and relu activiation
        filters=128,
        kernel_size=(3,3),
        activation='relu',
    ))
        
    # Add a max pooling layer to reduce spatial dimensions
    model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2,2),
        strides=(2,2), # common to have the same as pool size
        padding='same' # valid = no padding
    ))

    # Flatten the output image to feed into dense network
    model.add(tf.keras.layers.Flatten())

    # A dropout layer to reduce overfitting
    model.add(tf.keras.layers.Dropout(0.3))

    # Add a dense layer with some(?) neurons 
    model.add(tf.keras.layers.Dense(
        units=128, # number of neurons
        activation='relu',
    ))

    # Add an output dense layer with num_categories neurons - one for each category
    model.add(tf.keras.layers.Dense(
        units=NUM_CATEGORIES, # to match number of categories
        activation='softmax' # use softmax for multi-class classification
    ))

    # compile the model 
    model.compile(
        optimizer='Adamax', 
        loss='categorical_crossentropy', # categorical_crossentropy for multiple categories
        metrics=['accuracy'] # track accuracy during training
    )
    # return compiled model
    return model

if __name__ == "__main__":
    main()
