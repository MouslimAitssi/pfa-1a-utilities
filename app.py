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


def recherche_syntaxique(window):
	data = pd.read_csv('Articles_.csv', low_memory = False, encoding = 'utf-8')
	def get_outputs(window, list_inputs, list_links, list_content, list_titles, list_dates, V_date):
	    answer = []
	    answer2 = pd.DataFrame(columns = ['Author'])
	    for i in range(0, len(list_Ids)):

	        list_inputs[0] = list_inputs[0].lower()
	        res = list_content[i].lower().find(list_inputs[0])
	        if res != -1 and pd.to_datetime(list_dates[i]) >= V_date :
	            answer.append(["Title : " + str(list_titles[i]), "Publication : " + str(list_publications[i]), "Author : " + str(list_authors[i]), "Date : " + str(list_dates[i]), ("URL : ", str(list_links[i])), "Language : " + str(list_languages[i]), "Country : " + str(list_countrys[i])])
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
	    print(list_inputs)
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
	            print(str(date.get()))
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
	                label_title = Label(window, text = "Les articles contenants votre phrase sont:", font = ("courrier", 25), bg = 'black', fg = "red")
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
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "#8acafe", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)

	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "#8acafe", command = partial(showstatistics, out_put[1]))
	                statistics_button.pack()

	            window.mainloop()
	        
	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = 'black', command = partial(execution, window)).pack(expand = YES)
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
	                fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country']
	                scroll = Scrollbar(window)
	                scroll.pack(side = RIGHT, fill = Y)
	                listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                scroll.config(command = listbox.yview)
	                label_title = Label(window, text = "Les articles contenants votre phrase sont:", font = ("courrier", 25), bg = 'black', fg = "red")
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
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "#8acafe", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)

	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "#8acafe", command = partial(showstatistics, out_put[1]))
	                statistics_button.pack()


	            window.mainloop()

	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = 'black', command = partial(execution, window)).pack(expand = YES)

	    Oui = Button(frame, text = "Oui", font = ("Helvetica", 30), bg = 'white', fg = 'black', command = partial(oui_func, window)).pack(expand = YES)
	    Non = Button(frame, text = "Non", font = ("Helvetica", 30), bg = 'white', fg = 'black', command = non_func).pack(expand = YES)

	    frame.pack(expand = YES)
	    window.mainloop()

	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black", command = partial(date, window))
	search_button.pack()
	#search_button = Button(right_frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black")
	#right_frame.grid(row = 0, column = 1, sticky = W)
	#frame.grid()
	frame.pack(expand = YES)
	window.mainloop()


articles3 = pd.read_csv('Articles_.csv')
articles3.head()
articles=articles3.loc[0:1000,['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country'] ]
articles.shape
list_content = articles

def score_content(id, my_theme, content):

    result = []
    vectorizer = TfidfVectorizer(stop_words = "english", use_idf = True, smooth_idf = True)
    vectorizer.fit(content+my_theme)
    vector_list_contents = vectorizer.transform(content)
    vector_my_theme = vectorizer.transform(my_theme)
    result = linear_kernel(vector_my_theme, vector_list_contents)
    score = sum(result)/len(result)
    return score, id

def recherche_thematique(window):
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
		fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'score']
		#window.destroy()
		window = Tk()
		window.title("Recherche thematique")
		window.geometry("1240x1080")
		window.minsize(480, 360)
		window.iconbitmap("ccme.ico")
		window.config(background = "black")
		
		themes_publishers = []
		
		for k in range(0, len(list_content['Id'])):
			S = score_content(list_content['Id'][k], my_input, [list_content['Content'][k]])
			themes_publishers.append(S[0][0])
		list_content['score'] = themes_publishers 
		list_content.sort_values(by = "score", inplace = True, ascending = False)
		
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
			access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "#8acafe", command = access)
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

			statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "#8acafe", command = partial(showstatistics, list_content[list_content['score']>0] ,'Author'))
			statistics_button.pack()
			label_title = Label(window, text = "Les TOP articles traitants votre theme sont:", font = ("courrier", 30), bg = 'black', fg = "red")
			label_title.pack()
			comp = 0
			listbox.pack(expand = YES)


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
				else:
					break  
	

	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black", command = execution)
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

b1 = Button(frame, text = "Recherche syntaxique", font = ("courrier", 15), bg = 'black', fg = 'red', command = partial(recherche_syntaxique, window)).pack(expand = YES)
b2 = Button(frame, text = "Recherche thematique", font = ("courrier", 15), bg = 'black', fg = 'red', command = partial(recherche_thematique, window)).pack(expand = YES)

"""button1 = Button(frame, text = "Commencer", font = ("courrier", 30), bg = 'white', fg = "black", command = partial(recherche_thematique, window))
button1.pack(pady = 20, fill = X)
"""
frame.pack(expand = YES)
window.mainloop()
