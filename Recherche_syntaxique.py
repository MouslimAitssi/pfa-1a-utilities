from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from datetime import datetime
import pandas as pd
import csv
import dateparser

def get_outputs(list_inputs, list_links,list_content,list_titles,list_dates,V_date):
    answer=False
    for i in range(len(list_links)-1):
        for j in list_inputs:
            j=j.lower()
            res=list_content[i].lower().find(j)
            
            if res != -1 and pd.to_datetime(list_dates[i]) >= V_date :
                print(list_titles[i])
                print(list_links[i]+"\n")
                
                
                answer= True
                break
        
    return answer

data = pd.read_csv('Articles_.csv', low_memory=False, encoding='utf-8')
list_links=data['URL']
list_authors=data['Author']
list_titles=data['Title']
list_publications=data['Publication']
list_dates=data['Date']
list_content=data['Content']
list_Ids=data['Id']


list_inputs=[]
again=True
while again:
    print('Veuillez donner le mot que vous cherchez: ')
    inp=input()
    list_inputs.append(inp)
    
    choix_invalide = True
    while choix_invalide: 

        print("voulez vous ajouter un autre mot? (oui/non)")
        choix = input()


        if choix == 'non':
            again = False
            choix_invalide = False
        elif choix == 'oui':
            again = True
            choix_invalide = False
        else :
            choix_invalide = True
        

print("voulez vous précises une date pour la recherche ? (oui/non)")
choix_date=input()
if choix_date == 'oui':
    print("veillez donner une date :")
    V_date = input() 
    V_date = pd.to_datetime(V_date)
else :
    V_date = datetime(1, 1, 1, 1, 1)
out_put=get_outputs(list_inputs, list_links,list_content,list_titles,list_dates,V_date)
if out_put==False:
    print("Malhereusement on n'a pas pu trouvé les réultats souhaités, veuillez effectuer la recherche avec d'autres termes")


