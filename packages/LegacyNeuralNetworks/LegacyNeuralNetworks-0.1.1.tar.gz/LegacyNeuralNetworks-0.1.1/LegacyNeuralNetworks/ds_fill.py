import os

# String holders for code
Data_Wrangling_1 = """
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('titanic')
df.isnull().sum()
df.describe()
df.drop('deck',axis=1)
median = df['age'].median()
df['age'].fillna(median,inplace = True)
df.drop(['deck','embark_town','embarked'],axis=1)
pd.get_dummies(df,drop_first=True)
"""
Data_Wrangling_2 ="""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('exam.csv')
df.dtypes 
from pandas.plotting import scatter_matrix   # outlier
num_attribs=['raisedhands','VisITedResources','AnnouncementsView','Discussion']
scatter_matrix(df[num_attribs],figsize=(12,8))
import seaborn as sns
sns.pairplot(df)
df['Discussion'].describe()
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
df[['raisedhands']]=sc.fit_transform(df[['raisedhands']])
sns.scatterplot(df['raisedhands'])
df['raisedhands'].describe()
"""
descriptive_stat = """ 
import pandas as pd
# Read the iris dataset
iris_data = pd.read_csv('iris.csv')
# Group data by a categorical variable (e.g., Species) and calculate summary statistics 
# for a numeric variable (e.g., SepalLengthCm)
grouped_stats = iris_data.groupby('Species')['SepalLengthCm'].describe()
# Print the summary statistics
print(grouped_stats)
# Calculate and print additional summary statistics for each category
grouped_stats_additional = iris_data.groupby('Species')['SepalLengthCm'].agg(['mean', 'median', 'min', 'max', 'std'])
print(grouped_stats_additional)
# Calculate and print percentiles for each species
percentiles = iris_data.groupby('Species')['SepalLengthCm'].quantile([0.25, 0.5, 0.75])
print("Percentiles for Iris-setosa:")
print(percentiles.loc['Iris-setosa'])
print("Percentiles for Iris-versicolor:")
print(percentiles.loc['Iris-versicolor'])
print("Percentiles for Iris-virginica:")
print(percentiles.loc['Iris-virginica'])
"""
linear_reg_boston_DA_I = """ 
import numpy as np
import matplotlib.pyplot as plt 

import pandas as pd  
import seaborn as sns 
import matplotlib.pyplot as plt
df=pd.read_csv("BostonHousing.csv")

df.keys()
df

df.head()

sns.heatmap(df.corr(), annot=True)

plt.show()

df['rm'].mean()
df['rm'].fillna(df['rm'].mean(),inplace=True)

X = df.drop('tax',axis=1)
Y = df['tax']

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=5)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

lin_model = LinearRegression()
lin_model.fit(X_train, Y_train)
y_train_predict = lin_model.predict(X_train)
rmse = (np.sqrt(mean_squared_error(Y_train, y_train_predict)))
r2 = r2_score(Y_train, y_train_predict)

lin_model = LinearRegression()
lin_model.fit(X_train, Y_train)
y_train_predict = lin_model.predict(X_train)
rmse = (np.sqrt(mean_squared_error(Y_train, y_train_predict)))
r2 = r2_score(Y_train, y_train_predict)

print("The model performance for training set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))
print("\n")

# model evaluation for testing set

y_test_predict = lin_model.predict(X_test)
# root mean square error of the model
rmse = (np.sqrt(mean_squared_error(Y_test, y_test_predict)))

# r-squared score of the model
r2 = r2_score(Y_test, y_test_predict)

print("The model performance for testing set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))

"""

logistic_reg_DA_II = """ 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
# Load the dataset
x = pd.read_csv('Social_Network_Ads.csv')
data = pd.DataFrame(x)
data
data.drop("Gender", axis=1)
X = data.drop(['Purchased' ,"Gender"],axis=1)
y = data['Purchased']
print(X)
print('--------------------------------------------')
print(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the logistic regression model
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)

# Predict the test set results
y_pred = classifier.predict(X_test)
y_pred
print(classification_report(y_test,y_pred))

# Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred)
print('Confusion matrix:')
print(cm)

# Compute the accuracy, error rate, precision, recall, and F1-score
accuracy = accuracy_score(y_test, y_pred)
error_rate = 1 - accuracy
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print('Accuracy: ', accuracy)
print('Error rate: ', error_rate)
print('Precision: ', precision)
print('Recall: ', recall)
print('F1-score: ', f1)
tn,fp,fn,tp=cm.ravel()
(tn,fp,fn,tp)

"""

naviebayes_classifi_DA_III   = """ 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
iris_df = pd.read_csv('iris.csv')
iris_df
iris_df.shape
X  = iris_df.drop('Species',axis=1)
Y = iris_df['Species'].values
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2, random_state=8)
classifier = GaussianNB()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
y_pred
cm = confusion_matrix (y_test,y_pred)
sns.heatmap(cm ,annot =True)
plt.xlabel('predict label')
plt.ylabel('actual label')
plt.title('confusion matrix')
plt.show()
print(cm)
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
result = confusion_matrix(y_test , y_pred)
print('confusion_matrix : ',result)
print('accuracy score : ',accuracy_score(y_test,y_pred))
print('classification_report : ',classification_report(y_test,y_pred))
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
y_pred = classifier.predict(X_test)
y_pred
accuracy = accuracy_score(y_test, y_pred)
error_rate = 1 - accuracy
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')


print('Accuracy: ', accuracy)
print('Error rate: ', error_rate)
print('Precision: ', precision)
print('Recall: ', recall)
print('F1-score: ', f1)
tn,fp,fn,tp=cm.ravel()
(tn,fp,fn,tp)

"""

text_analysis = """ 
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

document = "This is an example document for tokenization. , This is an example document for POS tagging ,stemming"
#Document Preprocessing
tokens = word_tokenize(document)
print(tokens)
#POS Tagging
pos_tags = pos_tag(tokens)
print(pos_tags)
#Stop Words Removal
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
print(filtered_tokens)
#Stemming
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in tokens]
print(stemmed_tokens)
#Lemmatization
lemmatizer = WordNetLemmatizer()

lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
print(lemmatized_tokens)
import math
from collections import Counter

# Function to calculate TF
def calculate_tf(tokens):
    tf = Counter(tokens)
    total_words = len(tokens)
    tf_normalized = {word: count / total_words for word, count in tf.items()}
    return tf_normalized

# Function to calculate IDF
def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        for token in set(document):
            idf[token] = idf.get(token, 0) + 1

    idf_normalized = {word: math.log(total_documents / (count + 1)) for word, count in idf.items()}
    return idf_normalized

# Calculate TF for the given document
tf_document = calculate_tf(tokens)
print("TF for the document:")
print(tf_document)

# Calculate IDF for the given document
documents = [word_tokenize(document)]
idf_document = calculate_idf(documents)
print("\nIDF for the document:")
print(idf_document)

"""

data_visualization_I= """ 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
dataset = sns.load_dataset('titanic')
dataset.head()
sns.barplot(x='sex',y='age',data=dataset)
sns.catplot(x='sex',hue='survived',kind='count',data=dataset)
sns.histplot(data=dataset ,x='fare')
sns.histplot(data=dataset ,x='fare',binwidth=30)
sns.lineplot(data=dataset,x='sex',y='age')

########################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

titanic=pd.read_csv("titanic.csv")

titanic

titanic.isnull().sum()

import seaborn as sns
import matplotlib.pyplot as plt

# Countplot
sns.catplot(x ="Sex", hue ="Survived",kind ="count", data = titanic)

# Group the dataset by Pclass and Survived and then unstack them
group = titanic.groupby(['Pclass', 'Survived'])
pclass_survived = group.size().unstack()

# Heatmap - Color encoded 2D representation of data.
sns.heatmap(pclass_survived, annot = True, fmt ="d")

# Violinplot Displays distribution of data
# across all levels of a category.
sns.violinplot(x ="Sex", y ="Age", hue ="Survived",
data = titanic, split = True)

# Divide Fare into 4 bins
titanic['Fare_Range'] = pd.qcut(titanic['Fare'], 4)

# Barplot - Shows approximate values based
# on the height of bars.
sns.barplot(x ='Fare_Range', y ='Survived',
data = titanic)

# Countplot
sns.catplot(x ='Embarked', hue ='Survived',
kind ='count', col ='Pclass', data = titanic)
"""

data_visualization_II = """ 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
dataset = sns.load_dataset('titanic')
dataset.head()
sns.barplot(data=dataset,x='sex',y='age')
sns.boxenplot(data=dataset,x='sex',y='age')
sns.boxplot(data=dataset,x='sex',y='age')
plt.figure(figsize=(8,10))
sns.boxplot(data=dataset,x='sex',y='age',hue='survived')
plt.show()

#######################################

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

dataset = sns.load_dataset('titanic')

dataset.head()

d1=dataset

dataset = dataset.dropna()

dataset=dataset[["survived","pclass","age","sibsp","parch","fare"]]

sns.pairplot(dataset)

sns.rugplot(dataset['fare'])

sns.barplot(x='sex', y='age', data=d1)

import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

sns.barplot(x='sex', y='age', data=d1, estimator=np.std)

sns.countplot(x='sex', data=d1)

sns.boxplot(x='sex', y='age', data=d1)

sns.boxplot(x='sex', y='age', data=d1, hue="survived")

sns.violinplot(x='sex', y='age', data=d1)

sns.violinplot(x='sex', y='age', data=d1, hue='survived')

sns.violinplot(x='sex', y='age', data=d1, hue='survived', split=True)
sns.stripplot(x='sex', y='age', data=d1)

sns.stripplot(x='sex', y='age', data=d1, jitter=True)

sns.stripplot(x='sex', y='age', data=d1, jitter=True, hue='survived')

sns.stripplot(x='sex', y='age', data=d1, jitter=True, hue='survived', split=True)
sns.swarmplot(x='sex', y='age', data=d1)

sns.swarmplot(x='sex', y='age', data=d1, hue='survived')

sns.swarmplot(x='sex', y='age', data=d1, hue='survived', split=True)

sns.violinplot(x='sex', y='age', data=d1)
sns.swarmplot(x='sex', y='age', data=d1, color='black')
"""

data_visualization_III = """ 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('Iris.csv')
df
df.hist(figsize=(10,10))
import plotly.express as px
px.box(df ,x='SepalLengthCm',y='PetalLengthCm' )

##############################################################

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("Iris.csv")

df

df.info()

df.describe()

df.isnull().sum()

data = df.drop_duplicates(subset ="Species")
data

df.value_counts("Species")

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


sns.countplot(x="Species", data=df, )
plt.show()

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


sns.scatterplot(x='SepalLengthCm', y='SepalWidthCm',
				hue="Species", data=df, )

# Placing Legend outside the Figure
plt.legend(bbox_to_anchor=(1, 1), loc=2)

plt.show()

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


sns.scatterplot(x='PetalLengthCm', y='PetalWidthCm',
				hue="Species", data=df, )

# Placing Legend outside the Figure
plt.legend(bbox_to_anchor=(1, 1), loc=2)

plt.show()

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


sns.pairplot(df,hue="Species", height=2)

df

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


fig, axes = plt.subplots(2, 2, figsize=(10,10))

axes[0,0].set_title("Sepal Length")
axes[0,0].hist(df['SepalLengthCm'], bins=7)

axes[0,1].set_title("Sepal Width")
axes[0,1].hist(df['SepalWidthCm'], bins=5);

axes[1,0].set_title("Petal Length")
axes[1,0].hist(df['PetalLengthCm'], bins=6);

axes[1,1].set_title("Petal Width")
axes[1,1].hist(df['PetalWidthCm'], bins=6);

df.head()

df.corr(method='pearson')

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt


sns.heatmap(df.corr(method='pearson'),annot = True)

plt.show()

df.head()

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt

def graph(y):
	sns.boxplot(x="Species", y=y, data=df)

plt.figure(figsize=(10,10))
	
# Adding the subplot at the specified
# grid position
plt.subplot(221)
graph('SepalLengthCm')

plt.subplot(222)
graph('SepalWidthCm')

plt.subplot(223)
graph('PetalLengthCm')

plt.subplot(224)
graph('PetalWidthCm')

plt.show()

# importing packages
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('iris.csv')

sns.boxplot(x='SepalWidthCm', data=df)

# Importing
import pandas as pd
import seaborn as sns

# Load the dataset
df = pd.read_csv('iris.csv')

# IQR
Q1 = np.percentile(df['SepalWidthCm'], 25,
				interpolation = 'midpoint')

Q3 = np.percentile(df['SepalWidthCm'], 75,
				interpolation = 'midpoint')
IQR = Q3 - Q1

print("Old Shape: ", df.shape)

# Upper bound
upper = np.where(df['SepalWidthCm'] >= (Q3+1.5*IQR))

# Lower bound
lower = np.where(df['SepalWidthCm'] <= (Q1-1.5*IQR))

# Removing the Outliers
df.drop(upper[0], inplace = True)
df.drop(lower[0], inplace = True)

print("New Shape: ", df.shape)

sns.boxplot(x='SepalWidthCm', data=df)
"""

scala = """ 
object Hello { 
def main(args: Array[String]) = { 
println("Hello, world") 
} 
} 
"""


masterDict = {
    'Data_Wrangling_1' : Data_Wrangling_1,
    'Data_Wrangling_2': Data_Wrangling_2,
    'descriptive_stat': descriptive_stat,
    'linear_reg_boston_DA_I': linear_reg_boston_DA_I,
    'logistic_reg_DA_II': logistic_reg_DA_II,
    'naviebayes_classifi_DA_III': naviebayes_classifi_DA_III,
    'text_analysis':text_analysis,
    'data_visualization_I':data_visualization_I,
    'data_visualization_II':data_visualization_II,
    'data_visualization_III':data_visualization_III,
    'scala':scala
}

class Writer:
    def __init__(self, filename):
        self.filename = os.path.join(os.getcwd(), filename)
        self.masterDict = masterDict
        self.questions = list(masterDict.keys())

    def getCode(self, input_string):
        input_string = self.masterDict[input_string]
        with open(self.filename, 'w') as file:
            file.write(input_string)
        print(f'##############################################')

if __name__ == '__main__':
    write = Writer('output.txt')
    # print(write.questions)
    write.getCode('descision_region_perceptron')