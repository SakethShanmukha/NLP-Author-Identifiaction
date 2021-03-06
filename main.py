# NLTK is a must
import nltk
nltk.download('wordnet')
nltk.download('stopwords')

#1. Importing pandas to read the CSV file.

import pandas as pd
df = pd.read_csv('train.csv')
df.head(50)

#2. Performing Text Preprocessing
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatiser = WordNetLemmatizer()

def text_pre_processing(tex):
    no_punctuations=[char for char in tex if char not in string.punctuation]
    no_punctuations=''.join(no_punctuations)
    a=''
    i=0
    for i in range(len(no_punctuations.split())):
        b=lemmatiser.lemmatize(no_punctuations.split()[i], pos="v")
        a=a+b+' '
    return [word for word in a.split() if word.lower() not 
            in stopwords.words('english')]

#3. Label Encoding Categorical Data
from sklearn.preprocessing import LabelEncoder
y = df['author']
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)

#4. Using wordcloud to find the most-frequently used words by the authors ( Just for 10 records only, it can be changed ).
%matplotlib inline
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
X = df['text']

for i in range(10):
  wcloud = WordCloud().generate(X[i])
  print(X[i])
  print(df['author'][i])
  plt.imshow(wcloud, interpolation='bilinear')
  plt.show()
  
#5. Splitting data into train and test sets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=1234)

bag_of_words=CountVectorizer(analyzer=text_process).fit(X_train)

bog_train=bag_of_words.transform(X_train)

bog_test=bag_of_words.transform(X_test)


#6. Training the model
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model = model.fit(bog_train, y_train)

#7. Finding train and test sets model score respectively
model.score(bog_train, y_train)
model.score(bog_test, y_test)

#8. Printing the classification report for the train dataset
from sklearn.metrics import classification_report
predictions = model.predict(bog_test)
print(classification_report(y_test,predictions))

#9. Printing the confusion matrix
from sklearn.metrics import confusion_matrix
import numpy as np
import itertools
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0])
                                  , range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
cm = confusion_matrix(y_test,predictions)
plt.figure()
plot_confusion_matrix(cm, classes=[0,1,2], normalize=True, title='Confusion Matrix')

#10. Testing against model accuracy
newCSV = pd.read_csv('test.csv')
test_input_text = newCSV['text']
print(test_input_text)

#11. Applying model onto the provided test data
test_input = bag_of_words.transform(test_input_text)
#print(test_input)
output = model.predict(test_input)

#12. Printing the output
print(output)
