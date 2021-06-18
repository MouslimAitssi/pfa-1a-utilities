import pandas as pd
#Lecture de dataset
#articles3 = pd.read_csv(path+'articles3.csv')
#articles3.head()
#articles.loc[[0], ['content']]

dfs = []
dfs.append(pd.read_csv(path+'articles1.csv'))
dfs.append(pd.read_csv(path+'articles2.csv'))
dfs.append(pd.read_csv(path+'articles3.csv'))
# Concatenate all data into one DataFrame
articles3 = pd.concat(dfs, ignore_index=True)
articles3['url']=articles3['url'].fillna("lien non dispo")
articles3['content']=articles3['content'].fillna("contenu non dispo")
articles3.shape

#for i in range (len(articles['url'][1:50])):
#  if (articles['url'][i].isnull()) : print("yes")
#articles.head()

articles=articles3.loc[0:10000 , ['id', 'title', 'publication','author','date','year','month','url','content'] ]
articles['language']="english"
articles['country']="USA"
articles.shape

def score_content(id, my_theme, content):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
    result = []
    vectorizer = TfidfVectorizer(stop_words = "english", use_idf = True, smooth_idf = True)
    vectorizer.fit(content+my_theme)
    vector_list_contents = vectorizer.transform(content)
    vector_my_theme = vectorizer.transform(my_theme)
    result = linear_kernel(vector_my_theme, vector_list_contents)
    score=sum(result)/len(result)
    return score, id
def Recommendation(list_content, my_theme):
    themes_publishers = []
    for k in range(0, len(list_content['id'])):
        S = score_content(list_content['id'][k], my_theme, [list_content['content'][k]])
        themes_publishers.append(S[0])
    list_content['score']=themes_publishers 
    list_content.sort_values(by=["score"] , inplace=True , ascending = False )
    list2=list_content
    if(list_content.loc[list_content.index[0],"score"]< 0.001):
        print("Malheureusement, on n'a pas pu trouver une recommandation convenable\n")
        print("test2",list2[1:10])
    else:
      print("test2",list2[1:10])
      print("\nLes TOP articles traitants votre theme sont :\n")
      e = 0
      for i, element in list_content.iterrows():
        if(element["score"] > 0.001):
              print("\n********************\n")
              for c in range (11):
                print(fieldnames[c], ": ", element[fieldnames[c]])
              print("\n score = ", "%.4f" % element['score'])
        else:
              break    
    return list_content

import pandas as pd
fieldnames = ['id', 'title', 'publication','author','date','year','month','url','content', 'language', 'country','score']
list_content=articles
print('Veuillez donner votre theme:')
my_theme = input()
my_theme = [my_theme]
print("Veuillez patienter ...")
result=Recommendation(list_content, my_theme)
print("Voulez vous continuer ? (o/n):")
c = input()
if c == 'o':
    while True :
        print('Veuillez donner votre theme:')
        my_theme = input()
        print("Veuillez patienter ...")
        Recommendation(list_content, article_name, topN)
        print("Voulez vous continuer ? (o/n) :")
        c = input()
        if c == 'n':
            break
print("Au revoir !!")
