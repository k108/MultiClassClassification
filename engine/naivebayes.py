import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import pickle
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/myapp.log',
                    filemode='w')


clf=None
def trainClass():
    df=pd.read_csv("ProblemClass.csv",header=None,names=['Class', 'Text'])
    df.head()

    # Select the columns and check for the not null values and categorize/factorize the class.

    df=df[pd.notnull(df['Text'])]
    df['Class_id']=df['Class'].factorize()[0]
    df.head()

    # Get the dictinory of class and classid mapping.

    class_id_df = df[['Class', 'Class_id']].drop_duplicates().sort_values('Class_id')
    class_to_id=dict(class_id_df.values)
    print(class_to_id)
    logging.info(class_to_id)
    id_to_class=dict(class_id_df[['Class_id','Class']].values)
    print(id_to_class)
    logging.info(id_to_class)

    # check for the class and its count value visually

    #data=df.groupby('Class').Text.count()
    #data.plot.bar(ylim=0)
    #plt.show()

    # Text frequency and Inverse Document Frequency

    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(df.Text).toarray()
    labels = df[['Class_id']]
    #print(len(features))
    #print(len(labels))

    # Find most correlated words with their products

    N=2
    for Class, class_id in sorted(class_to_id.items()):
        features_chi2 = chi2(features, labels == class_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        #print("# '{}':".format(Class))
        #print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
        #print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

    # Naive Bayes Classifier

    X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Class'], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    #global clf
    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    count_pkl = 'count.pkl'
    model_pickle_path = 'model_pickle.pkl'
 
    # Create an variable to pickle and open it in write mode
    count_pickle = open(count_pkl, 'wb')
    pickle.dump(count_vect, count_pickle)
    count_pickle.close()
    model_pickle = open(model_pickle_path, 'wb')
    pickle.dump(clf, model_pickle)
    model_pickle.close()


def predictClass(text):
    # Need to open the pickled list object into read mode
    
    model_pickle_path = 'model_pickle.pkl'
    model_unpickle = open(model_pickle_path, 'r')
 
    # load the unpickle object into a variable
    clf = pickle.load(model_unpickle)
    
    count_pickle_path = 'count.pkl'
    count_unpickle = open(count_pickle_path, 'r')

    # load the unpickle object into a variable
    count_vect = pickle.load(count_unpickle)
    

    value=clf.predict(count_vect.transform([text]))
    conf=max(clf.predict_proba(count_vect.transform([text]))[0])
    print(value,conf)
    logging.info(value)
    logging.info(conf)
    return (value,conf)
    
