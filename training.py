from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from nltk.corpus import stopwords


from context import *
import sqlite3
from unicodedata import normalize


sentences = []
labels = []
tags = {
    'media': 0,
    'us': 1,
    'politics': 2,
    'world':3,
    'entertainment':4 #,
    #'sports':5,
    #'health':6
}

words = []
with sqlite3.connect(base_of_links) as conn:
    cursor = conn.cursor()
    inclause = "','".join(tags)
    cursor.execute(f"SELECT tag, file FROM metadata "
                   f"WHERE file is not NULL AND tag in ('{inclause}')")
    for tag, filename in cursor.fetchall():
        labels.append(tags[tag])
        with open(filename.replace('/root/news_parser/', ''), 'r') as f1:
            sentences.append(normalize('NFKD', f1.read()))


sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.2, random_state=1000)

vectorizer = CountVectorizer(min_df=0, stop_words=stopwords.words('english'))
vectorizer.fit(sentences_train)

X_train = vectorizer.transform(sentences_train)
X_test  = vectorizer.transform(sentences_test)
print(X_train.shape)
print(X_test.shape)


classifier = LogisticRegression(solver='lbfgs')
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)
y_pred = classifier.predict(X_test)

print("Accuracy:", score)
print(confusion_matrix(y_test, y_pred))
