# Neural Network SMS Text Classifier - freeCodeCamp Machine Learning with Python Project 5
import tensorflow as tf
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
import numpy as np

MAX_LEN = 50
MAX_WORDS = 1000

def get_model(train_data, test_data):
    # Prepare labels
    train_labels = train_data[0].map({'ham': 0, 'spam': 1}).values
    test_labels = test_data[0].map({'ham': 0, 'spam': 1}).values
    
    # Prepare text
    train_text = train_data[1].values
    test_text = test_data[1].values
    
    # Tokenize
    tokenizer = Tokenizer(num_words=MAX_WORDS, char_level=False)
    tokenizer.fit_on_texts(train_text)
    
    # Pad sequences
    train_sequences = tokenizer.texts_to_sequences(train_text)
    train_padded = pad_sequences(train_sequences, maxlen=MAX_LEN)
    
    test_sequences = tokenizer.texts_to_sequences(test_text)
    test_padded = pad_sequences(test_sequences, maxlen=MAX_LEN)
    
    # Build model
    model = Sequential([
        Embedding(MAX_WORDS, 32, input_length=MAX_LEN),
        SpatialDropout1D(0.2),
        LSTM(32, dropout=0.2, recurrent_dropout=0.2),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    
    # Train
    model.fit(train_padded, train_labels, epochs=10, batch_size=64, validation_split=0.2, verbose=0)
    
    return model, tokenizer

def predict_message(pred_text, model, tokenizer):
    sequence = tokenizer.texts_to_sequences([pred_text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)
    
    prediction = model.predict(padded)[0][0]
    
    label = "spam" if prediction > 0.5 else "ham"
    return [prediction, label]

if __name__ == "__main__":
    print("Run `get_model` with train_data and test_data dataframes to retrieve the compiled model.")
