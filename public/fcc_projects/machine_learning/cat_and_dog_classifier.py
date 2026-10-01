# Cat and Dog Image Classifier - freeCodeCamp Machine Learning with Python Project 2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Set parameters
batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

def get_data_generators(train_dir, validation_dir, test_dir):
    # 3. Create image generators
    train_image_generator = ImageDataGenerator(rescale=1./255)
    validation_image_generator = ImageDataGenerator(rescale=1./255)
    test_image_generator = ImageDataGenerator(rescale=1./255)

    # 4. Read images from directories
    train_data_gen = train_image_generator.flow_from_directory(
        batch_size=batch_size,
        directory=train_dir,
        shuffle=True,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        class_mode='binary')

    val_data_gen = validation_image_generator.flow_from_directory(
        batch_size=batch_size,
        directory=validation_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        class_mode='binary')

    test_data_gen = test_image_generator.flow_from_directory(
        batch_size=batch_size,
        directory=test_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        classes=['.'],
        shuffle=False,
        class_mode=None)

    # 5. Recreate train_image_generator using data augmentation
    image_gen_train = ImageDataGenerator(
        rescale=1./255,
        rotation_range=45,
        width_shift_range=0.15,
        height_shift_range=0.15,
        horizontal_flip=True,
        zoom_range=0.5
    )
    
    train_data_gen = image_gen_train.flow_from_directory(
        batch_size=batch_size,
        directory=train_dir,
        shuffle=True,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        class_mode='binary')

    return train_data_gen, val_data_gen, test_data_gen

def build_model():
    # 7. Create the model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                  metrics=['accuracy'])
    return model

def predict_images(model, test_data_gen):
    # 9. Get predictions
    probabilities = model.predict(test_data_gen)
    return probabilities
