# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 17:18:44 2019


"""

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk.corpus import stopwords

allsentences=[]
filename = 'srs4'
file = open('./exported/'+filename+'.csv')
"""Count one canditate"""
for line in file:
    allsentences.append(line)
file.close()

sw = stopwords.words('english')
remove_exception = ['have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'before', 'after', 'above', 'below', 'up', 'down', 'no', 'nor', 'not', 'only', 'can', 'will', 'don', "don't", 'should', "should've",  "aren't", "couldn't", "didn't", "doesn't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't", "needn't", "shouldn't", "wasn't", "weren't", "won't", 'wouldn', "wouldn't"]
for rem_word in remove_exception:
        sw.remove(rem_word)

tfidf = TfidfVectorizer(min_df=1,max_df=0.5,ngram_range=(2,3),stop_words=sw,use_idf=True)#(1,2)
features = tfidf.fit_transform(allsentences)
df2 = pd.DataFrame(
        features.todense(), columns=tfidf.get_feature_names()
        )
df2.to_excel('./finalanalysisreports/'+filename+'.xlsx')