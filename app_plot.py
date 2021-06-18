from tkinter import *
import pandas as pd
from functools import partial
import webbrowser
import matplotlib.pyplot as plt


articles3 = pd.read_csv('articles.csv')
articles3.head()
articles=articles3.loc[0:1000,['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country'] ]
articles.shape
list_content = articles

def score_content(id, my_theme, content):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
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

	window.title("CCME Application")
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
		window.title("CCME Application")
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
				print(good_result)
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

c1 = Checkbutton(frame, text = "Recherche syntaxique", font = ("courrier", 15), bg = 'black', fg = 'red').pack(expand = YES)
c2 = Checkbutton(frame, text = "Recherche thematique", font = ("courrier", 15), bg = 'black', fg = 'red').pack(expand = YES)

button1 = Button(frame, text = "Commencer", font = ("courrier", 30), bg = 'white', fg = "black", command = partial(recherche_thematique, window))
button1.pack(pady = 20, fill = X)

frame.pack(expand = YES)
window.mainloop()