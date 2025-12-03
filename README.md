# Customer Sentiment Analysis (Amazon)

## Overview
This project is a **Sentiment Analysis System** designed to classify Amazon customer reviews into sentiments (Positive, Negative, Neutral). It utilizes a **Support Vector Machine (SVM)** model trained on a dataset of filtered Amazon reviews.

The application processes text data using TF-IDF vectorization and includes a hyperparameter-tuned model to ensure high accuracy on unseen data.

## Key Features
- **Data Processing**: Cleans and vectorizes review text using TF-IDF.
- **Machine Learning**: Implements an SVM classifier (Linear Kernel).
- **Optimization**: Includes GridSearchCV for hyperparameter tuning to find the optimal regularization parameter (`C`).
- **Evaluation**: Provides detailed performance metrics including Accuracy, Classification Reports, and Confusion Matrix visualizations.
- **Interactive Prediction**: Allows users to input their own product reviews and get instant sentiment predictions.

## Technologies Used
- **Python 3.x**
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning model building, vectorization, and evaluation.
- **Matplotlib & Seaborn**: Data visualization (Confusion Matrix).

## Installation

1. Clone the repository or download the files.
2. Install the required Python packages:

```bash
pip install pandas scikit-learn matplotlib seaborn
```

## Usage

1. Ensure the dataset `Customer_Sentiment_filtered_amazon.csv` is in the correct directory (or update the path in `sentiment.py`).
2. Run the script:

```bash
python sentiment.py
```

3. The script will:
   - Train the model.
   - Display evaluation metrics.
   - Show a confusion matrix.
   - Prompt you to enter a product summary to predict its sentiment.

## Model Performance
The model achieves high accuracy (approx. 98%) on the test set. It has been evaluated on unseen examples to verify its ability to generalize to new reviews.
