# Linear Regression Health Costs Calculator - freeCodeCamp Machine Learning with Python Project 4
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def predict_health_costs():
    # Import data
    dataset = pd.read_csv('insurance.csv')
    
    # Convert categorical data to numbers
    # Features: age, sex, bmi, children, smoker, region, expenses
    dataset['sex'] = dataset['sex'].map({'female': 0, 'male': 1})
    dataset['smoker'] = dataset['smoker'].map({'no': 0, 'yes': 1})
    dataset['region'] = dataset['region'].map({'southwest': 1, 'southeast': 2, 'northwest': 3, 'northeast': 4})
    
    # Split the data into train and test datasets
    # The instructions say use 80% of the data for the train dataset and 20% for the test dataset
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    # Pop off the expenses column from the datasets
    train_labels = train_dataset.pop('expenses')
    test_labels = test_dataset.pop('expenses')

    # Normalize data
    # Normalizing is highly recommended for NN models when features have different ranges
    # We can use tf.keras.layers.Normalization or simple pandas normalization
    train_stats = train_dataset.describe().transpose()
    
    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']
        
    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)
    
    # Build the model
    model = Sequential([
        Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    
    model.compile(loss='mae',
                  optimizer=tf.keras.optimizers.RMSprop(0.001),
                  metrics=['mae', 'mse'])
                  
    # Train the model
    model.fit(normed_train_data, train_labels, epochs=100, validation_split=0.2, verbose=0)
    
    # Evaluate model
    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)
    
    print("Testing set Mean Abs Error: {:5.2f} expenses".format(mae))
    return model, normed_test_data, test_labels
