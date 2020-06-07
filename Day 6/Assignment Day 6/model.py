import pandas as pd
import pickle

dataset = pd.read_csv('http://iali.in/datasets/Social_Network_Ads.csv')

dataset.describe()

dataset.sample(10)

x = dataset.iloc[:,[2,3]].values
y = dataset.iloc[:,4].values

from sklearn.model_selection import train_test_split

x_train , x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)

from sklearn import tree

clf = tree.DecisionTreeClassifier()

clf = clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)

y_pred

from sklearn.metrics import accuracy_score

a = accuracy_score(y_pred,y_test)

from sklearn.metrics import classification_report

classes = ['0','1']

classification_report(y_test,y_pred,target_names=classes)

df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

pickle.dump(clf, open('model.pkl','wb'))

model = pickle.load(open('model.pkl','rb'))

