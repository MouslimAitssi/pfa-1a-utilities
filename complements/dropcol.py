import pandas as pd

articles = pd.read_csv('articles3.csv', low_memory = False, encoding = 'latin-1')
news3 = articles.loc[ : , ['id', 'title', 'publication','author','date','year','month','url','content'] ]
news3['language'] = "english"
news3['country'] ="USA"
news3.head()
news3.to_csv("articles4.csv", index = False, encoding = 'utf8')
print("done")