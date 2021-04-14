# -*- coding: utf-8 -*-
"""LRfBert.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YJjZK3WVJRXk8NiXLrKKDU2M45_5swdN
"""

!pip install --upgrade pip -q
!pip install -q ktrain

from google.colab import drive
drive.mount('/content/gdrive')

# Generic
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings, gc
warnings.filterwarnings("ignore")


# Tensorflow
import tensorflow as tf

# ktrain
import ktrain
from ktrain import text

# sklearn
from sklearn.model_selection import train_test_split

from google.colab import files
upload = files.upload()

from google.colab import files
upload = files.upload()

df = pd.read_csv("drugsComTrain_raw.tsv", sep='\t')
df.info()
df['review'].str.len().plot()
maxer=df[df['review'].str.len()>1000]
maxer.info()



df1 = pd.read_csv("drugsComTrain_raw.tsv", sep='\t')

df1.info()
p=df1[df1['review'].str.len()<=1000]
df1=p
drug1=pd.cut(df1.rating,bins=[0,8.00000,10],labels=[0,1],) 
df1.insert(3,'test',drug1) ##insert the review score
df1.head(4)

df2 = pd.read_csv("drugsComTest_raw.tsv", sep='\t')

df2.info()
p=df2[df2['review'].str.len()<=1000]
df2=p
drug1=pd.cut(df2.rating,bins=[0,8.00000,10],labels=[0,1],) 
df2.insert(3,'test',drug1) ##insert the review score
df2.head(4)

frames = [df1, df2]
df = pd.concat(frames)

df.info()

from sklearn.model_selection import train_test_split

train, testing = train_test_split(df, test_size=0.2, random_state=41)

df=train

train["rating"].mean()

train["rating"].median()

testing["rating"].median()

testing["rating"].mean()

# Data Split
target = ['test']
data = ['review']

X = df[data]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.25, random_state=42)

# Common Parameters
max_len = 512
batch_size = 6
learning_rate = 5e-5
epochs = 7

my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2),
    tf.keras.callbacks.ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
]
# Data Split
target = ['test']
data = ['review']

X = df[data]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)
# Transformer electra
model_ ="bert-base-uncased"
t_mod = text.Transformer(model_, classes = [0,1], maxlen=512)


'''Converting split data to list [so it can processed]'''
#train
X_tr = X_train['review'].tolist()
y_tr = y_train['test'].tolist()

#test
X_ts = X_test['review'].tolist()
y_ts = y_test['test'].tolist()


# Pre-processing training & test data
train = t_mod.preprocess_train(X_tr,y_tr)
test = t_mod.preprocess_train(X_ts,y_ts)

# Model Classifier
model = t_mod.get_classifier()

learner = ktrain.get_learner(model, train_data=train, val_data=test, batch_size=6)
learner.fit_onecycle(learning_rate, epochs = 7, callbacks=my_callbacks)
e = learner.validate(class_names=t_mod.get_classes())

predictor = ktrain.get_predictor(learner.model, t_mod)

model_save_name = 'bert123.pt'
path = F"/content/gdrive/My Drive/{model_save_name}" 
predictor.save(path)

testing

reloaded_predictor = ktrain.load_predictor(path)

a=testing['review'].tolist()
a

c=predictor.predict(a)

from pandas import DataFrame
df_pred = DataFrame(c,columns=['pred'])

df_pred

true=testing['test'].tolist()

df_true = DataFrame(true,columns=['true'])
df_true.head()

import sklearn
from sklearn.metrics import confusion_matrix

sklearn.metrics.confusion_matrix(df_true["true"], df_pred["pred"], labels=[0,1])

from sklearn.metrics import f1_score

sklearn.metrics.f1_score(df_true["true"], df_pred["pred"], labels=[0,1])

from sklearn.metrics import classification_report
matrix = classification_report(df_true["true"],df_pred["pred"],labels=[1,0])

matrix

precision    recall  f1-score   support

           1       0.83      0.85      0.84     21056
           0       0.85      0.84      0.84     21877

    accuracy                           0.84     42933
   macro avg       0.84      0.84      0.84     42933
weighted avg       0.84      0.84      0.84     42933

testing.reindex()

df=testing

anxiety=df[df['condition']=='Anxiety']

df.info()

anxiety.info()

anxiety.head()



a=anxiety['review'].tolist()
a

c=predictor.predict(a)

from pandas import DataFrame
df_pred = DataFrame(c,columns=['pred'])

df_pred

df_pred.info()

true=anxiety['test'].tolist()

df_true = DataFrame(true,columns=['true'])
df_true.head()

import sklearn
from sklearn.metrics import confusion_matrix

sklearn.metrics.confusion_matrix(df_true["true"], df_pred["pred"], labels=[0,1])

from sklearn.metrics import f1_score

sklearn.metrics.f1_score(df_true["true"], df_pred["pred"], labels=[0,1])

from sklearn.metrics import classification_report
matrix = classification_report(df_true["true"],df_pred["pred"],labels=[1,0])

matrix

precision    recall  f1-score   support

           1       0.83      0.88      0.85       893
           0       0.82      0.75      0.78       649

    accuracy                           0.82      1542
   macro avg       0.82      0.81      0.82      1542
weighted avg       0.82      0.82      0.82      1542

def speed():
  a=anxiety['review'].tolist()
  a

  c=predictor.predict(a)

  from pandas import DataFrame
  df_pred = DataFrame(c,columns=['pred'])

  df_pred

  true=anxiety['test'].tolist()

  df_true = DataFrame(true,columns=['true'])
  df_true.head()

  import sklearn
  from sklearn.metrics import confusion_matrix

  sklearn.metrics.confusion_matrix(df_true["true"], df_pred["pred"], labels=[0,1])

  from sklearn.metrics import f1_score

  sklearn.metrics.f1_score(df_true["true"], df_pred["pred"], labels=[0,1])

  from sklearn.metrics import classification_report
  matrix = classification_report(df_true["true"],df_pred["pred"],labels=[1,0])


  return matrix

df["condition"].value_counts().head(50)

anxiety=df[df['condition']=='Birth Control']

speed()

precision    recall  f1-score   support

           1       0.84      0.80      0.82      2745
           0       0.89      0.92      0.90      4956

    accuracy                           0.88      7701
   macro avg       0.87      0.86      0.86      7701
weighted avg       0.87      0.88      0.87      7701

anxiety=df[df['condition']=='Depression']

speed()

precision    recall  f1-score   support

           1       0.83      0.85      0.84      1121
           0       0.86      0.83      0.85      1195

    accuracy                           0.84      2316
   macro avg       0.84      0.84      0.84      2316
weighted avg       0.84      0.84      0.84      2316

anxiety=df[df['condition']=='Pain']

speed()

"""              precision    recall  f1-score   support

           1       0.80      0.86      0.83       938
           0       0.82      0.75      0.78       781

    accuracy                           0.81      1719
   macro avg       0.81      0.80      0.81      1719
weighted avg       0.81      0.81      0.81      1719

"""

anxiety=df[df['condition']=='Acne']

speed()

precision    recall  f1-score   support

           1       0.83      0.86      0.85       816
           0       0.82      0.79      0.80       672

    accuracy                           0.83      1488
   macro avg       0.83      0.82      0.83      1488
weighted avg       0.83      0.83      0.83      1488

anxiety=df[df['condition']=='Bipolar Disorde']

speed()

precision    recall  f1-score   support

           1       0.80      0.86      0.83       512
           0       0.87      0.81      0.84       577

    accuracy                           0.83      1089
   macro avg       0.83      0.83      0.83      1089
weighted avg       0.83      0.83      0.83      1089

precision    recall  f1-score   support

           1       0.80      0.86      0.83       512
           0       0.87      0.81      0.84       577

    accuracy                           0.83      1089
   macro avg       0.83      0.83      0.83      1089
weighted avg       0.83      0.83      0.83      1089

anxiety=df[df['condition']=='Insomnia']

speed()

precision    recall  f1-score   support

           1       0.79      0.81      0.80       499
           0       0.83      0.81      0.82       556

    accuracy                           0.81      1055
   macro avg       0.81      0.81      0.81      1055
weighted avg       0.81      0.81      0.81      1055

anxiety=df[df['condition']=='Weight Loss']

speed()

precision    recall  f1-score   support

           1       0.86      0.86      0.86       581
           0       0.76      0.75      0.75       337

    accuracy                           0.82       918
   macro avg       0.81      0.80      0.81       918
weighted avg       0.82      0.82      0.82       918

anxiety=df[df['condition']=='Obesity']

speed()

precision    recall  f1-score   support

           1       0.84      0.85      0.85       550
           0       0.80      0.78      0.79       416

    accuracy                           0.82       966
   macro avg       0.82      0.82      0.82       966
weighted avg       0.82      0.82      0.82       966

anxiety=df[df['condition']=='ADHD']

speed()

precision    recall  f1-score   support

           1       0.83      0.88      0.85       443
           0       0.87      0.82      0.84       449

    accuracy                           0.85       892
   macro avg       0.85      0.85      0.85       892
weighted avg       0.85      0.85      0.85       892

anxiety=df[df['condition']=='Diabetes, Type 2']

speed()

