import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# preprocess data
df = pd.read_csv('output1.csv')
df['Description'] = df['Description'].fillna('')
df['combined_text'] = df['Drug_Name'] + ' ' + df['Reason'] + ' ' + df['Description']

# Encoding
le = LabelEncoder()
df['Reason_encoded'] = le.fit_transform(df['Reason'])

# vectors
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
X = tfidf.fit_transform(df['combined_text'])
y = df['Reason_encoded']

# RandomForestClassifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X, y)

# Save the model outputs
with open('rf_classifier.pkl', 'wb') as f:
    pickle.dump(rf_classifier, f)

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

def recommend_drugs(description, top_n=3):
    # objects
    with open('rf_classifier.pkl', 'rb') as f:
        rf_classifier = pickle.load(f)
    
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    
    with open('label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    
    input_vector = tfidf.transform([description])
    probabilities = rf_classifier.predict_proba(input_vector)
    top_classes = probabilities.argsort()[0][::-1][:top_n]
    
    recommendations = []
    for class_index in top_classes:
        reason = le.inverse_transform([class_index])[0]
        drugs = df[df['Reason'] == reason]['Drug_Name'].unique()
        recommendations.append((reason, drugs))
    
    return recommendations
