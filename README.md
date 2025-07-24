
# Crop Yield Prediction

## Overview

This project focuses on predicting crop yields based on various factors such as temperature, rainfall, country, crop category, and other relevant features. Accurate yield prediction is crucial for agricultural planning, resource management, and ensuring food security. This repository provides a machine learning-based solution for crop yield prediction, enabling data-driven decision-making in the agricultural sector.

## Features

*   *Data-Driven Prediction:* Utilizes machine learning models to predict crop yields based on historical data and environmental factors.
*   *Multiple Factors Considered:* Takes into account various features such as temperature, rainfall, country, and crop category for accurate predictions.
*   *Scalable Solution:* Designed to handle large datasets and can be scaled to accommodate different regions and crop types.
*   *Easy to Use:* Provides a user-friendly interface for data input and prediction generation.

## Technologies Used

*   *Python:* The primary programming language used for data analysis, model training, and prediction.
*   *Machine Learning Libraries:*
    *   *Scikit-learn:* Used for implementing various machine learning algorithms.
    *   *Pandas:* Used for data manipulation and analysis.
    *   *NumPy:* Used for numerical computations.
*   *Data Visualization Libraries:*
    *   *Matplotlib:* Used for creating visualizations and plots.
    *   *Seaborn:* Used for enhanced data visualization.

## Installation

To set up the project locally, follow these steps:

1.  *Clone the Repository:*

    
    git clone https://github.com/Jastinmb904/Crop-yield-prediction-.git
    cd Crop-Yield-Prediction
    

2.  *Create a conda Environment (Recommended):*

    
    conda env create -p ./env -f environment.yml -y
    conda activate ./env
    

3.  *Install Dependencies:*

    
    pip install -r requirements.txt / `while creating conda env automatically installs required libraries`
    

## Usage

1.  *Prepare Your Data:*
    *   Ensure your data is in a compatible format (e.g., CSV).
    *   The data should include features such as temperature, rainfall, country, crop category, and historical yield data.

2.  *Run the app:*

    
    python app.py
    

3.  *View the Predictions:*
    *  The app will output the predicted crop yields based on the input data.

## Data Description

The dataset used for this project contains the following features:

*   *Country:* The country where the crop is grown.
*   *Item:* The type of crop.
*   *Year:* The year the data was recorded.
*   *Temperature:* Average temperature during the growing season.
*   *Rainfall:* Total rainfall during the growing season.
*   *Yield:* The crop yield (target variable).

## Model Training

1.  *Data Preprocessing:*
    *   Clean and preprocess the data to handle missing values and outliers.
    *   Encode categorical variables using techniques like one-hot encoding.
    *   Split the data into training and testing sets.

2.  *Model Selection:*
    *   Experiment with different machine learning models such as:
        *   Linear Regression
        *   KNeighborsRegressor
        *   DecisionTreeRegressor
        *   Ridge, Lasso Regression

3.  *Training and Evaluation:*
    *   Train the selected model on the training data.
    *   Evaluate the model's performance on the testing data using metrics such as:
        *   Mean Squared Error (MSE)
        *   R-squared (R2)

4.  *Model Tuning:*
    *   Fine-tune the model's hyperparameters to optimize performance.
    *   Use techniques like cross-validation to ensure robust performance.

5.  *Save the Model:*
    *   Save the trained model for future use.

    
    import pickle
    # Example: Saving the model
    pickle.dump(model, open('trained_model.pkl', 'wb'))
    

## File Structure

 project_folder/
    ├── src/
    ├── templates/
    │   ├── index.html  <-- This file must exist here
    ├── models/
    │   ├── dtr.pkl
    │   ├── preprocessor.pkl
    ├── data/
    ├── app.py  <-- This file runs Flask
    ├── notebook.ipynb
    ├── environment.yml - to create conda environment
    ├── requirement.txt


## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please submit an issue or a pull request.

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

[Jastin mb](jastinmb904@gmail.com)

