from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import pandas as pd
import csv
import dateparser
from tkinter import *
from functools import partial
import webbrowser
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import geopandas as gpd
import matplotlib.pyplot as plt
from descartes import PolygonPatch



#exemple du format du data des articles
s = {'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
'country': ["Jordan", "Kuwait", "Ghana", "Mexico", "France", "Germany", "Ghana", "Mexico", "Mexico", "France", "Germany", "Russia", "Brazil", "Brazil", "Ghana"]}
artic=pd.DataFrame(data = s)
#freq=list(articles.groupby('country').count())
SS=[list(artic.groupby('country')['country'].transform('count')), artic['country'].tolist()]
keys = SS[1]
values =SS[0]
dictio = dict(zip(keys, values))
#lecture from data
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities.head()




#affichage
#result=cities[cities['country']=="morocco"]
#fig, ax = plt.subplots(1, 1, figsize=(15, 15))
#ax.set_aspect('equal')
#world.plot(ax=ax, color='white', edgecolor='black')
#result.plot(ax=ax, marker='o', color='red', markersize=20)
#ax.set_title('Carte avec geopandas');   



def plotCountryPatch(axes, country_name, fcolor ):
    # plot a country on the provided axes
    nami = world[world.name == country_name]
    namigm = nami.__geo_interface__['features']  # geopandas's geo_interface
    namig0 = {'type': namigm[0]['geometry']['type'], \
              'coordinates': namigm[0]['geometry']['coordinates']}
    axes.add_patch(PolygonPatch( namig0, fc=fcolor, ec="black", alpha=0.85, zorder=2 ))

# plot the whole world
#ax2 = world.plot( figsize=(8,4), edgecolor=u'gray', cmap='Set2' )

# or plot Africa continent
#ax2 = world[world.continent == 'Africa'].plot(figsize=(8,8), edgecolor=u'gray', cmap='Pastel1')
def plot_show():
	ax2 = world.plot(figsize=(25,25), edgecolor=u'gray', cmap='Pastel1')
	# then plot some countries on top
	for x in dictio:
	  print(x)
	  plotCountryPatch(ax2, x , 'red')

	# the place to plot additional vector data (points, lines)

	plt.ylabel('Latitude')
	plt.xlabel('Longitude')

	#ax2.axis('scaled')
	plt.show()


def recherche_syntaxique(window):
	data = pd.read_csv('Articles_.csv', low_memory = False, encoding = 'utf-8')
	def get_outputs(window, list_inputs, list_links, list_content, list_titles, list_dates, V_date):
	    answer = []
	    answer2 = pd.DataFrame(columns = ['Author'])
	    for i in range(0, len(list_Ids)):

	        list_inputs[0] = list_inputs[0].lower()
	        if type(list_content[i]).__name__ == 'str':
	        	res = list_content[i].lower().find(list_inputs[0])
	        	if res != -1 and pd.to_datetime(list_dates[i]) >= V_date:
	        		answer.append(["Title : " + str(list_titles[i]), "Publication : " + str(list_publications[i]), "Author : " + str(list_authors[i]), "Date : " + str(list_dates[i]), ("URL : ", str(list_links[i])), "Language : " + str(list_languages[i]), "Country : " + str(list_countrys[i]), "sentiment : " + str(list_sentiments[i])])
	        		answer2 = answer2.append({'Author' : list_authors[i]}, ignore_index = True, verify_integrity = False, sort = None)
	    return answer, answer2


	list_links = data['URL']
	list_authors = data['Author']
	list_titles = data['Title']
	list_publications = data['Publication']
	list_dates = data['Date']
	list_content = data['Content']
	list_Ids = data['Id']
	list_languages = data['Language']
	list_countrys = data['Country']
	list_sentiments = data['sentiment']


	window.destroy()
	window = Tk()
	frame = Frame(window, bg = 'black')
	window.title("Recherche Syntaxique")
	window.geometry("1240x1080")
	window.minsize(480, 360)
	window.iconbitmap("ccme.ico")
	window.config(background = "black")
	"""#8acafe"""
	width = 500
	height = 500
	canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
	image = PhotoImage(master = canvas, file = "ccme.png")
	canvas.create_image(width/2, height/2, image = image)
	canvas.pack()
	label_title = Label(window, text = 'Veuillez donner la phrase que vous cherchez:', font = ("courrier", 30), bg = 'black', fg = "red")
	label_title.pack()
	words = StringVar()
	my_input = Entry(window, textvariable = words, font = ("Helvetica", 30), bg = 'white', fg = "black")
	my_input.pack()
	def date(window):

	    list_inputs = [str(words.get())]
	    #print(list_inputs)
	    window.destroy()
	    window = Tk()
	    frame = Frame(window, bg = 'black')
	    window.title("Recherche Syntaxique")
	    window.geometry("1240x1080")
	    window.minsize(480, 360)
	    window.iconbitmap("ccme.ico")
	    window.config(background = "black")
	    label_title = Label(frame, text = "Voulez vous préciser une date comme début de la recherche ?", font = ("Courrier", 30), bg = 'black', fg = 'red')
	    label_title.pack(expand = YES)
	    
	    def oui_func(window):
	        window.destroy()
	        window = Tk()
	        frame = Frame(window, bg = 'black')
	        date = StringVar()
	        window.title("Recherche Syntaxique")
	        window.geometry("1240x1080")
	        window.minsize(480, 360)
	        window.iconbitmap("ccme.ico")
	        window.config(background = "black")
	        label_title = Label(frame, text = "Saisissez la date depuis laquelle vous voulez commencer la recherche (jj-mm-aaaa):", font = ("Courrier", 20), bg = 'black', fg = 'red')
	        label_title.pack(expand = YES)
	        entry = Entry(frame, textvariable = date, font = ("Helvetica", 30), bg = 'white', fg = "black").pack(expand = YES)
	        
	        def execution(window):
	            window.destroy()
	            window = Tk()
	            window.title("Recherche Syntaxique")
	            window.geometry("1240x1080")
	            window.minsize(480, 360)
	            window.iconbitmap("ccme.ico")
	            window.config(background = "black")
	            #print(str(date.get()))
	            V_date = pd.to_datetime(str(date.get()))
	            out_put = get_outputs(window, list_inputs, list_links, list_content, list_titles, list_dates, V_date)
	            if len(out_put[0]) == 0:
	                label_title = Label(window, text = "Malhereusement on n'a pas pu trouvé les résultats souhaités, veuillez effectuer la recherche avec d'autres termes", font = ("Courrier", 10), bg = 'black', fg = 'red')
	            else:
	                fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country']
	                scroll = Scrollbar(window)
	                scroll.pack(side = RIGHT, fill = Y)
	                listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                scroll.config(command = listbox.yview)
	                label_title = Label(window, text = "Les articles contenants votre phrase sont: (" + str(len(out_put[0]))+ " resultats)", font = ("courrier", 25), bg = 'black', fg = "red")
	                label_title.pack()
	                comp = 0
	                for k in out_put[0]:
	                    listbox.insert(comp, "************************************************************************************************************************************************************************************")
	                    comp = comp + 1
	                    for i in k:
	                        listbox.insert(comp, i)
	                        comp = comp + 1
	                def access():
	                    webbrowser.open_new(str(listbox.get('active')[1]))

	                def showstatistics(good_result):
	                    ax1 = plt.subplot(121, aspect = 'equal') 
	                    good_result['Author'].value_counts().plot.pie()
	                    plt.show()

	                right_frame = Frame(window, bg = "black")
	                right_frame.pack(side = RIGHT)  
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)

	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, out_put[1]))
	                statistics_button.pack()
	                plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = plot_show).pack(expand = YES)

	            window.mainloop()
	        
	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(execution, window)).pack(expand = YES)
	        frame.pack(expand = YES)
	        window.mainloop()
	    
	    def non_func():
	        date = datetime(2019, 1, 1, 1, 1)

	        def execution(window):
	            window.destroy()
	            window = Tk()
	            window.title("Recherche Syntaxique")
	            window.geometry("1240x1080")
	            window.minsize(480, 360)
	            window.iconbitmap("ccme.ico")
	            window.config(background = "black")
	            out_put = get_outputs(window, list_inputs, list_links, list_content, list_titles, list_dates, date)
	            if len(out_put[0]) == 0:
	                label_title = Label(window, text = "Malheureusement on n'a pas pu trouvé les résultats souhaités, veuillez effectuer la recherche avec d'autres termes", font = ("Courrier", 30), bg = 'black', fg = 'red')
	            else:
	                fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'sentiment']
	                scroll = Scrollbar(window)
	                scroll.pack(side = RIGHT, fill = Y)
	                listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                scroll.config(command = listbox.yview)
	                label_title = Label(window, text = "Les articles contenants votre phrase sont: (" + str(len(out_put[0]))+ " resultats)", font = ("courrier", 25), bg = 'black', fg = "red")
	                label_title.pack()
	                comp = 0
	                for k in out_put[0]:
	                    listbox.insert(comp, "*******************************************************************************************************************************************************************************************************************")
	                    comp = comp + 1
	                    for i in k:
	                        listbox.insert(comp, i)
	                        comp = comp + 1
	                def access():
	                    webbrowser.open_new(str(listbox.get('active')[1]))

	                def showstatistics(good_result):
	                    ax1 = plt.subplot(121, aspect = 'equal') 
	                    good_result['Author'].value_counts().plot.pie()
	                    plt.show()

	                right_frame = Frame(window, bg = "black")
	                right_frame.pack(side = RIGHT)  
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)

	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, out_put[1]))
	                statistics_button.pack()

	                plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = plot_show).pack(expand = YES)


	            window.mainloop()

	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(execution, window)).pack(expand = YES, fill = X)

	    Oui = Button(frame, text = "Oui", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(oui_func, window)).pack(expand = YES, fill = X)
	    Non = Button(frame, text = "Non", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = non_func).pack(expand = YES, fill =X)

	    frame.pack(expand = YES)
	    window.mainloop()

	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = "black", command = partial(date, window))
	search_button.pack()
	#search_button = Button(right_frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black")
	#right_frame.grid(row = 0, column = 1, sticky = W)
	#frame.grid()
	frame.pack(expand = YES)
	window.mainloop()


#list_content = pd.read_csv('Articles_.csv')
#articles3.head()
#articles = articles3.loc[0:1000,['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'sentiment'] ]
#articles.shape
#list_content = articles

def score_content(my_theme, content):

    result = []
    vectorizer = TfidfVectorizer(stop_words = "english", use_idf = True, smooth_idf = True)
    vectorizer.fit(content+my_theme)
    vector_list_contents = vectorizer.transform(content)
    vector_my_theme = vectorizer.transform(my_theme)
    #print(vector_list_contents)
    result = linear_kernel(vector_my_theme, vector_list_contents)
    score = sum(result)/len(result)
    return score

def recherche_thematique(window):
	list_content = pd.read_csv('Articles_.csv')
	window.destroy()
	window = Tk()

	frame = Frame(window, bg = 'black')

	window.title("Recherche thematique")
	window.geometry("1240x1080")
	window.minsize(480, 360)
	window.iconbitmap("ccme.ico")
	window.config(background = "black")
	"""#8acafe"""
	width = 500
	height = 500
	canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
	image = PhotoImage(master = canvas, file = "ccme.png")
	canvas.create_image(width/2, height/2, image = image)
	#canvas.grid(row = 0, column = 0, sticky = W)
	canvas.pack()

	#right_frame = Frame(frame, bg = 'black')

	#label_title = Label(right_frame, text = "Veuillez saisir votre theme:", font = ("Helvetica", 30), bg = 'black', fg = "red")
	#label_title.pack()
	label_title = Label(window, text = "Veuillez saisir votre theme:", font = ("courrier", 30), bg = 'black', fg = "red")
	label_title.pack()

	#my_input = Entry(right_frame, font = ("Helvetica", 30), bg = 'white', fg = "black")
	ment = StringVar()
	my_input = Entry(window, textvariable = ment, font = ("Helvetica", 30), bg = 'white', fg = "black")
	my_input.pack()
	#search_button = Button(right_frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black")
	#right_frame.grid(row = 0, column = 1, sticky = W)

	#frame.grid()
	frame.pack(expand = YES)

	def execution():
		my_input = [str(ment.get())]
		print(my_input[0])
		fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'score', 'sentiment']
		#window.destroy()
		window = Tk()
		window.title("Recherche thematique")
		window.geometry("1240x1080")
		window.minsize(480, 360)
		window.iconbitmap("ccme.ico")
		window.config(background = "black")
		
		themes_publishers = []
		
		for k in range(0, len(list_content['Id'])):
			if type(list_content['Content'][k]).__name__ == 'str':
				S = score_content(my_input, [list_content['Content'][k]])
				themes_publishers.append(S[0])
			else:
				themes_publishers.append(0)
		list_content['score'] = themes_publishers 
		list_content.sort_values(by = ["score"], inplace = True, ascending = False)
		print(list_content.loc[list_content.index[0], "score"])
		if list_content.loc[list_content.index[0], "score"] < 0.001:

			label_title = Label(window, text = "Malheureusement, on n'a pas pu trouver une recommandation convenable.", font = ("courrier", 20), bg = 'black', fg = "red")
			label_title.pack()
		
		else:
			scroll = Scrollbar(window)
			scroll.pack(side = RIGHT, fill = Y)
			listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
			scroll.config(command = listbox.yview)
			
			def access():
				webbrowser.open_new(str(listbox.get('active')[1]))

			right_frame = Frame(window, bg = "black")
			right_frame.pack(side = RIGHT)	
			access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
			access_button.pack(expand = YES)

			def showstatistics(good_result, affichage):
			
				good_result.hist(column = 'score')
				plt.title("Affichage des statistiques", color = 'r')
				plt.xlabel("Score", color = 'blue')
				plt.ylabel("Nombre d'articles", color ='blue')
				plt.figure(figsize = (16, 8))
				ax1 = plt.subplot(121, aspect = 'equal') 
				good_result[affichage].value_counts().plot.pie()
				plt.show()

			statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, list_content[list_content['score']>0] ,'Author'))
			statistics_button.pack()
			plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = plot_show).pack(expand = YES)
			comp = 0

			nbre = 0
			for i, element in list_content.iterrows():
				if(element["score"] >= 0.001):
					listbox.insert(comp, "**************************************************************************************************************************************************************************************************************")
					l = []
					comp = comp + 1
					for c in range (1, 9):
						if c != 6:
							listbox.insert(comp, (str(fieldnames[c]) + " : ", str(element[fieldnames[c]])))
							comp = comp + 1
					listbox.insert(comp, "score = " + str("%.4f" % element['score']))
					comp = comp + 1
					listbox.insert(comp, "sentiment = " + str(element[fieldnames[10]]))
					comp = comp + 1
					nbre = nbre + 1
				else:
					break  

			label_title = Label(window, text = "Les TOP articles traitants votre theme sont: (" + str(nbre) + " résultats)", font = ("courrier", 30), bg = 'black', fg = "red")
			label_title.pack()
			listbox.pack(expand = YES)

	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = "black", command = execution)
	search_button.pack()	
	window.mainloop()
	return


window = Tk()
window.title("CCME Application")
window.geometry("1240x1080")
window.minsize(480, 360)
window.iconbitmap("ccme.ico")
window.config(background = "black")
width = 500
height = 500
canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
image = PhotoImage(master = canvas, file = "ccme.png")
canvas.create_image(width/2, height/2, image = image)
canvas.pack(expand = YES)
frame = Frame(window, bg = "black")

label_title = Label(window, text = "Bienvenue sur notre application", font = ("courrier", 30), bg = 'black', fg = "red")
label_title.pack(expand = YES)

b1 = Button(frame, text = "Recherche syntaxique", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(recherche_syntaxique, window)).pack(expand = YES, fill = X)
b2 = Button(frame, text = "Recherche thematique", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(recherche_thematique, window)).pack(expand = YES, fill = X)

"""button1 = Button(frame, text = "Commencer", font = ("courrier", 30), bg = 'white', fg = "black", command = partial(recherche_thematique, window))
button1.pack(pady = 20, fill = X)
"""
frame.pack(expand = YES)
window.mainloop()