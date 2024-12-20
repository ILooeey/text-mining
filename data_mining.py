# -*- coding: utf-8 -*-
"""Data Mining.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XFMVLKKEtWjXh3Q7XAhnY00PYX7oCNu9

### DUA VARIABEL
### **hotel rating**
"""

import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('hotel_rating2.csv')
df

X, Y = df['reviewtext'], df['Sentiment']

X.dropna(inplace=True)
Y = Y[X.index]

print(Y.value_counts())

df['Sentiment'] = df['Sentiment'].replace('excellent', 'good', regex=True)
df['Sentiment']

X, Y = df[['reviewtext']], df['Sentiment']

X.dropna(inplace=True)
Y = Y[X.index]

print(Y.value_counts())

from imblearn.under_sampling import RandomUnderSampler



sentiment = df['Sentiment']

under_sampler = RandomUnderSampler(sampling_strategy={'good':1590})

undersampling_ratio = 0.5
if undersampling_ratio < 1:
    majority_class_count = df['Sentiment'].value_counts().max()
    undersampled_count = int(majority_class_count * undersampling_ratio)

X_resampled, y_resampled = under_sampler.fit_resample(df[['reviewtext']], df['Sentiment'])
df['Sentiment'] = sentiment =  y_resampled
df['reviewtext'] = X_resampled

df.dropna(subset=['reviewtext', 'Sentiment'], inplace=True)

print("Setelah undersampling:",y_resampled)
print(X_resampled)

import matplotlib.pyplot as plt
jumlah_good = sentiment.value_counts().get('good')
jumlah_bad = sentiment.value_counts().get('bad')

plt.bar(['Good', 'Bad'], [jumlah_good, jumlah_bad])
plt.xlabel('Sentiment')
plt.ylabel('Jumlah Kalimat')
plt.title('Distribusi Sentimen')
plt.show()

from wordcloud import WordCloud, STOPWORDS

def plot_cloud(wordcloud):
  plt.figure(figsize=(10, 8))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')
  plt.show()

all_words = ''.join([reviewtext for reviewtext in df['reviewtext']])

wordcloud = WordCloud(
    width = 4000,
    height=3000,
    random_state=3,
    background_color='black',
    colormap= 'Blues_r',
    collocations=False,
    stopwords=STOPWORDS
).generate(all_words)

plot_cloud(wordcloud)

if sentiment.isna().any():
  df['Sentiment'] = sentiment.dropna()

df.isnull().sum()

"""Clean Text"""

PUNCTUATION = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def clean_text(reviewtext):
  reviewtext = re.sub(r'[^\x00-\x7F]+', '', reviewtext)
  reviewtext = re.sub(r'\s+', ' ', reviewtext)
  reviewtext = reviewtext.replace('!', '').replace('*', '')
  reviewtext = reviewtext.lower()
  reviewtext = "".join([c for c in reviewtext if c not in PUNCTUATION])
  return reviewtext.strip()

df['reviewtext'] = df['reviewtext'].apply(clean_text)
print(df['reviewtext'])

"""*Stopword*

"""

nltk.download('punkt')
nltk.download('stopwords')


def remove_stopwords(reviewtext):
    stop_words_german = set(stopwords.words('german'))
    stop_words_spanish = set(stopwords.words('spanish'))
    stop_words_french = set(stopwords.words('french'))
    stop_words_italian = set(stopwords.words('italian'))
    stop_words_dutch = set(stopwords.words('dutch'))

    stop_words_all = stop_words_german.union(stop_words_spanish).union(stop_words_french).union(stop_words_italian).union(stop_words_dutch)

    wordss = nltk.word_tokenize(reviewtext)
    filtered_words = [word.lower() for word in wordss if word.lower() not in stop_words_all]

    return ' '.join(filtered_words)


df['reviewtext'] = df['reviewtext'].apply(remove_stopwords)

df['Sentiment']

df

df

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['reviewtext'])
y = df['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(X_train)

print(X_test)

print(y_train)

print(y_test)

model = MultinomialNB(alpha=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(y_pred)

accuracy = accuracy_score(y_test, y_pred)
accuracy = accuracy*100

print("Accuracy:", accuracy)

print(jumlah_good)
print(jumlah_bad)

"""### **TIGA SENTIMENT**"""

import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# df = pd.read_csv('hotel_rating2.csv', nrows=500)
df = pd.read_csv('hotel_rating2.csv')

df

"""Clean Text"""

PUNCTUATION = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def clean_text(reviewtext):
    reviewtext = re.sub(r'[^\x00-\x7F]+', '', reviewtext)
    reviewtext = re.sub(r'\s+', ' ', reviewtext)
    reviewtext = reviewtext.replace('!', '').replace('*', '')
    reviewtext = reviewtext.lower()
    reviewtext = "".join([c for c in reviewtext if c not in PUNCTUATION])
    return reviewtext.strip()

df['reviewtext'] = df['reviewtext'].apply(clean_text)
print(df['reviewtext'])

"""Stop words"""

nltk.download('punkt')
nltk.download('stopwords')


def remove_stopwords(reviewtext):
    stop_words_german = set(stopwords.words('german'))
    stop_words_spanish = set(stopwords.words('spanish'))
    stop_words_french = set(stopwords.words('french'))
    stop_words_italian = set(stopwords.words('italian'))
    stop_words_dutch = set(stopwords.words('dutch'))

    stop_words_all = stop_words_german.union(stop_words_spanish).union(stop_words_french).union(stop_words_italian).union(stop_words_dutch)

    wordss = nltk.word_tokenize(reviewtext)
    filtered_words = [word.lower() for word in wordss if word.lower() not in stop_words_all]

    return ' '.join(filtered_words)


df['reviewtext'] = df['reviewtext'].apply(remove_stopwords)
df.to_csv('hotel_rating2.csv', index=False)

X, Y = df['reviewtext'], df['Sentiment']

X.dropna(inplace=True)
Y = Y[X.index]

print(Y.value_counts())

print(df['reviewtext'])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['reviewtext'])
y = df['Sentiment']

df['reviewtext'] = df['reviewtext'].astype(str)

print(X)

from wordcloud import WordCloud, STOPWORDS

def plot_cloud(wordcloud):
  plt.figure(figsize=(10, 8))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')
  plt.show()

all_words = ''.join([reviewtext for reviewtext in df['reviewtext']])

wordcloud = WordCloud(
    width = 4000,
    height=3000,
    random_state=3,
    background_color='black',
    colormap= 'Blues_r',
    collocations=False,
    stopwords=STOPWORDS
).generate(all_words)

plot_cloud(wordcloud)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=42)

print(X_train)

print(X_test)

print(y_train)

print(y_test)

model = MultinomialNB(alpha=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(y_pred)

accuracy = accuracy_score(y_test, y_pred)
accuracy = accuracy*100

print("Accuracy:", accuracy)