import pandas as pd
import os
import json
import pickle
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline as ImPipeline
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Function to balance classes
def balance_classes(dataframe, label_column='Label_binary'):
    majority_class = dataframe[label_column].mode()[0]
    minority_class = dataframe[dataframe[label_column] != majority_class]
    majority_class = dataframe[dataframe[label_column] == majority_class]

    minority_upsampled = resample(minority_class,
                                  replace=True,
                                  n_samples=len(majority_class),
                                  random_state=123)

    return pd.concat([majority_class, minority_upsampled])

# Function to train the logistic regression model
def train_model(data_file, output_dir='./model'):
    df = pd.read_csv(data_file)
    label_encoder = LabelEncoder()
    df['Label_binary'] = df['Label'].apply(lambda x: 'True' if 'true' in x.lower() else 'False')
    df['Label_encoded'] = label_encoder.fit_transform(df['Label_binary'])
    df = balance_classes(df, 'Label_binary')

    X = df.drop(['Label', 'Label_binary', 'Label_encoded'], axis=1)
    y = df['Label_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    text_features = 'statement'
    text_transformer = TfidfVectorizer()

    categorical_features = ['subjects', 'speaker_name', 'speaker_job', 'speaker_state', 'speaker_affiliation', 'statement_context']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('txt', text_transformer, text_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    classifier = LogisticRegression(max_iter=1000, solver='liblinear')

    pipeline = ImPipeline([
        ('preprocessor', preprocessor),
        ('sampler', RandomOverSampler(random_state=42)),
        ('classifier', classifier)
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, 'logistic_regression_model.pkl'), 'wb') as f:
        pickle.dump(pipeline, f)
    with open(os.path.join(output_dir, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(label_encoder, f)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Function to load a trained logistic regression model
def load_model(model_dir):
    with open(os.path.join(model_dir, 'logistic_regression_model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb') as f:
        label_encoder = pickle.load(f)
    return model, label_encoder

# get predicted class and justification
def predict(statement_data, model_dir='./model'):
    model, label_encoder = load_model(model_dir)
    
    # Convert the dictionary to a DataFrame
    data_df = pd.DataFrame([statement_data])
    
    # Predict the label using the loaded model
    label_encoded = model.predict(data_df)[0]
    label = label_encoder.inverse_transform([label_encoded])[0]
    explanation = call_justification_api(label, statement_data)
    return label, explanation

# Function to call an API for justification
def call_justification_api(prediction, statement_data):
    url = 'https://us-central1-satalia-421919.cloudfunctions.net/generate_statement_assessment2'
    statement_data['prediction'] = prediction
    response = requests.post(url, json=statement_data)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return 'Failed to fetch justification.'

