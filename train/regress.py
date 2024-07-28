import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def preprocess_and_regress(file_path):
    # Load the data
    df = pd.read_csv(file_path)
    
    # Convert the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Convert 'time' to seconds since the start
    df['time_seconds'] = (df['time'] - df['time'].min()).dt.total_seconds()
    
    # Drop the original 'time' column
    df.drop(columns=['time'], inplace=True)
    
    # Encode categorical 'Weather' feature
    df = pd.get_dummies(df, columns=['Weather'], drop_first=True)
    
    # Define the feature matrix X and target vector Y
    X = df.drop(columns=['time_seconds'])
    Y = df['time_seconds']
    
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    # Initialize and train the regression model
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    # Make predictions on the test set
    Y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)
    
    # Display coefficients
    coeffs = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
    print("\nCoefficients:")
    print(coeffs)
    
    return model

# Example usage
file_path = r'D:\project\porto\data\data1.csv'
model = preprocess_and_regress(file_path)
