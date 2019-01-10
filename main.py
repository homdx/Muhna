#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''	
	* Kivy version 1.10.1
	* Matheus Felipe Teodoro Correia
	* matheuscorreia559@gmail.com
	*
	* Aplicativo Muhna
	----implementado
	* Jogo da memoria
	* banco de dados com placar 
	*
	
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image,AsyncImage
from kivy.properties import StringProperty,NumericProperty, ListProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.popup import Popup
from random import randint
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.logger import LoggerHistory
import sqlite3
import os
import time
import random
import json
import os

# soh tirar quando for compilar
# adc vibracao aos botoes
# try:
# 	from jnius import autoclass

# except KeyError:
# 	os.environ['JDK_HOME'] = "/usr/lib/jvm/java-8-openjdk-amd64"
# 	os.environ['JAVA_HOME'] = "/usr/lib/jvm/java-8-openjdk-amd64"
# 	from jnius import autoclass

#Variaveis globais
tempo = 0
qtdimagens = 0
contador = 0
texto = []
pontos = 0
inicio = 0
fim = 0
flag = 0
erro = 0
nome = ''
ident = []

#globais do quiz
quiz_inicial = 0
quiz_final = 0
quiz_nome = ''
quiz_pontos = 0

''' 
	*lembrar
	*	nao se esquecer que compila em python 2 (VM-buildozer)
	*	setxkbmap br = teclado em pt-br kivy (VM-buildozer)
	*	acerto.jpeg eh usado apenas como marcacao de acerto, nao eh uma imagem
	*
'''
class Gerenciador(ScreenManager):#gerenciador de telas
	def __init__(self,**kwargs):
		super(Gerenciador,self).__init__(**kwargs)

class Inserenome(BoxLayout):

	def __init__(self,**kwargs):
		super(Inserenome,self).__init__(**kwargs)
	def salvanome(self):
		global nome
		nome = self.ids.texinp.text
		self.ids.texinp.text=""
		print(nome)
	def guardabanco(self):#da pra usar o on_dismiss
		global nome,pontos,tempo,erros
		
		if(nome == ''):
			print("Nenhum nome salvo")

		else:
			print("Salvo no banco de dados = "+str(nome))
			banco = sqlite3.connect('teste.db')
			c = banco.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text, pontos integer, tempo real, erros integer)''')
			parametros = (nome,pontos,tempo,erro)
			c.execute("INSERT INTO rank VALUES (?,?,?,?)",parametros)
			banco.commit()
			nome = ''

class Menu(Screen):
	def __init__(self,**kwargs):
		super(Menu,self).__init__(**kwargs)

class Pronto(BoxLayout):
	def __init__(self,**kwargs):
		super(Pronto,self).__init__(**kwargs)

class Teste(Screen):
	
	def __init__(self,**kwargs):
		super(Teste,self).__init__(**kwargs)
	def on_pre_enter(self):
		banco = sqlite3.connect('quiz.db')
		c = banco.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real)''')
		dump = c.execute("SELECT nome,pontos,tempo from rank order by tempo asc limit 3")##conta os de cima
		j = dump.fetchall()

		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,0
		box.add_widget(LabelBotao(text='Os 3 melhores no quiz',color=(0,0,0,1)))
		#MyLabel(text='Os 3 melhores',size_hint_y=None,height='60dp')
		self.ids.qg.add_widget(box)
		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,.9
		box.add_widget(Tarefa_two(text='N°'))
		box.add_widget(Tarefa_two(text='Nome'))
		box.add_widget(Tarefa_two(text='Pontos'))
		box.add_widget(Tarefa_two(text='Tempo'))
		
	
		
		self.ids.qf.add_widget(box)
		ind = 1
		cor = 0.10,0.05,0,.8
		for dumps in j:
			box = BoxLayoutCustom2()
			if (ind % 2 == 0):
				cor = [0.30,0.14,0,1]
			else:
				cor = [0.30,0.14,0,.3]
			
			box.cor = cor
			
			box.add_widget(Tarefa_two(text=str(ind)))
			box.add_widget(Tarefa_two(text=str(dumps[0])))
			box.add_widget(Tarefa_two(text=str(dumps[1])))
			box.add_widget(Tarefa_two(text=str(dumps[2])+'s'))
			self.ids.qf.add_widget(box)
			ind+=1

	def previous_screen_limpa(self, *args):
	
		global pontos,qtdimagens,erro,tempo,inicio,fim

		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart_limpa)
		
		# for key,val in self.ids.items():
		#  	print("key={0}, val={1}".format(key,val))
		Pergunta.pontos = 0

	def restart_limpa(self,  *args):
		global contador,texto

		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart_limpa)
		self.limpatela()


	def limpatela(self,*args):#botao recomecar, limpa a tela e cria uma nova tela		
		self.parent.remove_widget(self)
		teste = Teste(name='teste')
		self.parent.add_widget(teste)
	def carregaWidgets(self):
		global quiz_inicial

		conteudo = open('quiz.json').read()
		arquivos = json.loads(conteudo)
		#print(arquivos[19])
		
		for j in range(5):	
			selecionado = random.choice(arquivos)
			#print(selecionado)
			
			pergunta = selecionado['Pergunta']
			#print(pergunta)
			
			salvar = []
			
			for respostas in selecionado[u'Respostas']:			
				salvar.append(respostas)
		
			random.shuffle(salvar)

			adc = []
			for i in salvar:

				#print(i['resp'])
				#print(i['flag'])

				adc.append(i['resp'])
				adc.append(i['flag'])
				
			arquivos.remove(selecionado)
			#print(adc)
			adc.append(j)
			self.ids.qz.add_widget(Pergunta(pergunta=pergunta,args=adc))
			quiz_inicial = time.time() 

		

class MyLabel(Image):#redimensiona os textos
	text = StringProperty('')
	def __init__(self,**kwargs):
		super(MyLabel,self).__init__(**kwargs)
	def on_text(self, *args):
		# Just get large texture:
		l = Label(text="Selecione a quantidade de imagens para o novo jogo",color=(0,0,0,1),bold=True)#,outline_width=40,outline_color=(0.22,0.10,0.03))
		l.font_size = '50dp'  # something that'll give texture bigger than phone's screen size
		l.texture_update()
		# Set it to image, it'll be scaled to image size automatically:
		self.texture = l.texture

class Quiz(Screen):#tela do quiz
	def __init__(self,**kwargs):
		super(Quiz,self).__init__(**kwargs)
	def previous_screen(self, *args):
		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart)
	
	def restart(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart)
class GridLayout_custom(GridLayout):
	def __init__(self,**kwargs):
		super(GridLayout_custom,self).__init__(**kwargs)
class Jogo(Screen):#Tela do jogo da memoria
	
	def __init__(self,**kwargs):
		super(Jogo,self).__init__(**kwargs)

	def on_pre_enter(self):
		banco = sqlite3.connect('teste.db')
		c = banco.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real,erros integer)''')
		dump = c.execute("SELECT nome,pontos,tempo,erros from rank order by tempo asc limit 3")##conta os de cima
		j = dump.fetchall()

		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,0
		box.add_widget(LabelBotao(text='Os 3 melhores no jogo da memória',color=(0,0,0,1)))
		#MyLabel(text='Os 3 melhores',size_hint_y=None,height='60dp')
		self.ids.label.add_widget(box)
		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,.9
		box.add_widget(Tarefa_two(text='N°'))
		box.add_widget(Tarefa_two(text='Nome'))
		box.add_widget(Tarefa_two(text='Pontos'))
		box.add_widget(Tarefa_two(text='Tempo'))
		box.add_widget(Tarefa_two(text='Erros'))
		
	
		
		self.ids.tbox2.add_widget(box)
		ind = 1
		cor = 0.10,0.05,0,.8
		for dumps in j:
			box = BoxLayoutCustom2()
			if (ind % 2 == 0):
				cor = [0.30,0.14,0,1]
			else:
				cor = [0.30,0.14,0,.3]
			
			box.cor = cor
			box.add_widget(Tarefa_two(text=str(ind)))
			box.add_widget(Tarefa_two(text=str(dumps[0])))
			box.add_widget(Tarefa_two(text=str(dumps[1])))
			box.add_widget(Tarefa_two(text=str(dumps[2])+'s'))
			box.add_widget(Tarefa_two(text=str(dumps[3])))
			self.ids.tbox2.add_widget(box)
			ind+=1
	def addImagem(self,valor):#adc os widgets com o text contendo os nomes das imagens		
		global inicio
		global qtdimagens
		
		
		qtdimagens = valor
		inicio = time.time()#inicia a contagem de tempo
		cont=0

		result = random.sample(range(1,29), valor)#gera um vetor de tamanho valor(4,6,10) entre 1 e 28(quantidade de imagens na pasta)
		nova = result[:]#copia do vetor
		random.shuffle(result)#result foi embaralhado

		self.ids.gridlayout.size_hint_y = 1
		for j in range(valor):
			selecionado = random.choice(result)#sorteia um item do vetor
			selecionadoT = random.choice(nova)#sorteia um item do vetor
	
			result.remove(selecionado)#remove o item sorteado
			nova.remove(selecionadoT)#remove o item sorteado

			texto = "imagens/"+str(selecionado)+'.jpg'#gera o nome da imagem
			self.ids.gridlayout.add_widget(ImageButton(text=str(texto)))#adc a imagem no gridlayot

			texto = "imagens/"+str(selecionadoT)+'.jpg'
			self.ids.gridlayout.add_widget(ImageButton(text=str(texto)))

			cont+=2

	def previous_screen(self, *args):
		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart)
	
	def restart(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart)
	
	def previous_screen_limpa(self, *args):
	
		global pontos,qtdimagens,erro,tempo,inicio,fim

		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart_limpa)
		erro = 0
		pontos = 0
		qtdimagens = 0
		inicio = 0
		fim=0

	def restart_limpa(self,  *args):
		global contador,texto

		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart_limpa)
		self.limpatela()
		
		contador = 0
		texto = []

	def limpatela(self,*args):#botao recomecar, limpa a tela e cria uma nova tela		
		self.parent.remove_widget(self)
		jogo = Jogo(name='jogo')
		self.parent.add_widget(jogo)

class ImageButton(ButtonBehavior, AsyncImage):

	#lendo o json com os nomes dos anime/plantas
	conteudo = open('arquivo.json').read()
	arquivos = json.loads(conteudo)
	erro = 0
	def __init__(self,text='',**kwargs):
		super(ImageButton,self).__init__(**kwargs)
		global flag
		global fim
		self.id = str(flag)
		self.text = text
		flag+=1
	def on_press(self):
		pass
		# retirar quando for compilar, vibracao android
		# print(self)
		# PythonActivity = autoclass('org.renpy.android.PythonActivity')
		# Context = autoclass('android.content.Context')
		# activity = PythonActivity.mActivity
		# vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
		# if vibrator.hasVibrator():
		# 	vibrator.vibrate(200)
		# else:
		# 	print("Your device does not have a vibration motor.")

	def on_release(self):
		pass
	def guardabanco_t(self):#da pra usar o on_dismiss
		global nome,tempo,pontos,erro

		
		
		
		if(nome == ''):
			print("Nenhum nome salvo")

		else:
			print("Salvo no banco de dados teste = "+str(nome)+' '+str(tempo))
			
			banco = sqlite3.connect('teste.db')
			c = banco.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real,erros integer)''')
			parametros = []
			parametros = (nome,pontos,tempo,erro)
			c.execute("INSERT INTO rank VALUES (?,?,?,?)",parametros)
			banco.commit()
			nome = ''
			tempo = 0
			ponto = 0
			
	def pop(self):
		global inicio,fim,tempo,erro,pontos
		
		tempo = ('{:.2f}'.format(fim - inicio))
		
		
		banco = sqlite3.connect('teste.db')
		c = banco.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real,erros integer)''')
		dump = c.execute("SELECT count(tempo)from rank where tempo < ?",[tempo])##conta os de cima
		
		j = dump.fetchall()
		
		dump = []
		dump = c.execute("SELECT * FROM(SELECT * FROM(SELECT tempo,nome,pontos,erros FROM rank WHERE tempo < ?)  as A ORDER BY tempo DESC limit 3) as B ORDER BY tempo ASC",[tempo])
		teste = dump.fetchall()
		

		teste.append((tempo,'%&marca&%',pontos,erro))
		i = 0
		qtd_bank = j[0][0]
		indice = []
		
		if(qtd_bank > 0):
			if(qtd_bank >= 3):
				inic = qtd_bank-2
			else:
				if(qtd_bank == 2):
					inic = qtd_bank -1
				else:
					inic = qtd_bank
			qtd_bank+=1 
			for i in range(inic,qtd_bank,1):
				indice.append(i)
			#adc o do jogador
		else:
			
			indice.append(0)
			#adc o do jogador
		
		dump = c.execute("SELECT count(tempo)from rank where tempo > ?",[tempo])#conta os de baixo
		j = dump.fetchall()
		
		qtd_bank = j[0][0]
		i+=1
		indice.append(i)
		
		qtd_bank += (i+1)

		for k in range(i+1,qtd_bank,1):
			indice.append(k)	

		dump = c.execute("SELECT * FROM(SELECT * FROM(SELECT tempo,nome,pontos,erros FROM rank WHERE tempo > ?) as A ORDER BY tempo asc limit 3)",[tempo])
		
		qb = dump.fetchall()
		for i in qb:
			teste.append(i)

		cont = indice[0]

		pop = Popcustom(title='Fim de jogo',title_size='30sp',title_align='center',size_hint=(.1,.1),auto_dismiss=False,background = 'imagens/fundo.png', background_color=(0,0,0,.9),separator_color=(0,0,0,0))
		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,.9
		box.add_widget(Tarefa_two(text='N°'))
		box.add_widget(Tarefa_two(text='Nome'))
		box.add_widget(Tarefa_two(text='Pontos'))
		box.add_widget(Tarefa_two(text='Tempo'))
		box.add_widget(Tarefa_two(text='Erros'))
		pop.ids.box.add_widget(box)
		for tupla in teste:
			#print(str(cont)+' '+str(tupla[0])+' '+tupla[1]+' '+tupla[2])
			
			if (cont % 2 == 0):
				cor = [0.30,0.14,0,.6]
			else:
				cor = [0.30,0.14,0,.4]

			box = BoxLayoutCustom2()
			box.cor = cor
			if(tupla[1] == '%&marca&%'):
				box.add_widget(Tarefa_two(text=str(cont)))
				box.add_widget(InserenomeMemory())#nome
				box.add_widget(Tarefa_two(text=str(pontos)))
				box.add_widget(Tarefa_two(text=str(tempo)+'s'))#tempo(real)
				box.add_widget(Tarefa_two(text=str(erro)))
			else:
				box.add_widget(Tarefa_two(text=str(cont)))
				box.add_widget(Tarefa_two(text=str(tupla[1])))#nome
				box.add_widget(Tarefa_two(text=str(tupla[2])))
				box.add_widget(Tarefa_two(text=str(tupla[0])+'s'))#tempo(real)
				box.add_widget(Tarefa_two(text=str(tupla[3])))
		
			pop.ids.box.add_widget(box)
			cont+=1

		b2 = BoxLayoutCustom2(orientation='vertical',cor=(1,1,1,0))
		b2.add_widget(Botao_custom(text='Fechar Popup',on_press = ImageButton.guardabanco_t ,on_release=pop.dismiss))
		pop.ids.box.add_widget(b2)
		#self.ids.scroll.scroll_to(box)
		anim = Animation(size_hint=(1,1),duration=1,t='out_back')
		anim.start(pop)
		Clock.schedule_once(pop.open, 1.1)
	

	def AcertoImg(self,text=[]):

		box = BoxLayout(orientation = 'vertical')#,padding=10,spacing=10)

		figura = Image(source=str(text))		
		box.add_widget(figura)
		
		pop = Popup(title=self.arquivos[text],title_font='DejaVuSans',separator_height='0dp',title_color=(1,1,1,1),title_size='30sp', content = box,size_hint=(.1,.1),title_align='center',background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))#,size=(100,100))

		anim = Animation(size_hint=(1,1),duration=0.2,t='out_back')
		anim.start(pop)
		
		pop.open()
		
		Clock.schedule_once(pop.dismiss, 1)

	def troca(self,text=[]):#troca as imagens do botao
		global contador,texto,ident

		if(contador<2 and text != 'acerto.jpeg'):
			contador+=1
			texto.append(str(text))
			ident.append(self.id)
			if(self.source and self.text != 'acerto.jpeg'):
				self.source = self.text
				self.canvas.ask_update()

		Clock.schedule_once(self.conta, 1)#chama a funcao 1s a frente

	def conta(self,text=[]):#verifica se as imagens sao iguais e altera para acerto.png, se nao ele volta para pergunta.png

		global contador,texto,ident,pontos,qtdimagens,fim,erro

		
		if(contador == 2):
			if( (texto[0] == texto[1]) and (ident[0] != ident[1]) ):
				self.AcertoImg(texto[0])
				for child in self.parent.children:
					if(child.text == texto[0] and child.text != 'acerto.jpeg' ):			
						child.source = child.text
						child.text = 'acerto.jpeg'
				pontos+=1;
				if(pontos == qtdimagens):
					fim = time.time()
					self.pop()			
			else:
				erro+=1

				for child in self.parent.children:
					if(child.source != 'imagens/pergunta.png' and child.source != 'acerto.jpeg' and child.text != 'acerto.jpeg'  ):
						child.source = 'imagens/pergunta.png'						
			
			contador=0
			texto=[]
			ident=[]
class Tarefa_two(BoxLayout):
	def __init__(self,text='',**kwargs):
		super(Tarefa_two,self).__init__(**kwargs)
		self.ids.label.text = text
class Tarefa(BoxLayout):

	def __init__(self,text='',**kwargs):
		super(Tarefa,self).__init__(**kwargs)
		self.ids.label.text = text

class BoxLayoutCustom(BoxLayout):
	def __init__(self,**kwargs):
		super(BoxLayoutCustom,self).__init__(**kwargs)
class BoxLayoutCustom2(BoxLayout):
	def __init__(self,**kwargs):
		super(BoxLayoutCustom2,self).__init__(**kwargs)

class Ranking(Screen):

	def __init__(self,tarefas=[],**kwargs):
		super(Ranking,self).__init__(**kwargs)
	def addWidget(self):
		texto = self.ids.texto.text
		self.ids.box.add_widget(Tarefa(text=texto))
		self.ids.texto.text = ''
	def teste(self):
		banco = sqlite3.connect('teste.db')
		c = banco.cursor()
		dump = c.execute("SELECT nome,pontos,erros,tempo from rank ORDER BY tempo ASC, erros ASC, pontos DESC limit 20")

		contador = 1
		for linha in dump.fetchall():
			
			if (contador % 2 == 0):
				cor = [0,0,0, .4]
			else:
				cor = [0,0,0,.2]

			box = BoxLayoutCustom()
			box.cor = cor
			box.add_widget(Tarefa(text=str(contador)))
			box.add_widget(Tarefa(text=str(linha[0])))
			box.add_widget(Tarefa(text=str(linha[1])))
			box.add_widget(Tarefa(text=str(linha[2])))
			box.add_widget(Tarefa(text=str(linha[3])+'s'))
			contador+=1
			
			self.ids.box.add_widget(box)
		self.ids.scroll.scroll_to(box)
		self.ids.action.parent.remove_widget((self.ids.action))

	def previous_screen_limpa(self, *args):

		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart_limpa)


	def restart_limpa(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart_limpa)
		self.limpatela()


	def limpatela(self,*args):#botao recomecar, limpa a tela e cria uma nova tela		
		self.parent.remove_widget(self)
		teste = Ranking(name='ranking')
		self.parent.add_widget(teste)



class LabelBotao(Image):

	text = StringProperty('')
	
	def __init__(self , **kwargs):
		super(LabelBotao, self).__init__(**kwargs)

	def on_text(self, *args):
		# Just get large texture:
		l = Label(text=self.text,font_name='RobotoMono-Regular.ttf',color=(1,1,1,1))#,outline_width=40,outline_color=(0.22,0.10,0.03))
		l.font_size = '50dp'  # something that'll give texture bigger than phone's screen size
		l.texture_update()
		# Set it to image, it'll be scaled to image size automatically:
		self.texture = l.texture

class Botao(ButtonBehavior,LabelBotao): 

	branco = ListProperty([1,1,1,1])
	preto = ListProperty([0,0,0,1])
	

	def __init__(self, **kwargs):
		super(Botao, self).__init__(**kwargs)
	def on_press(self):
		self.color = self.preto
		
	def on_release(self):
		self.color = self.branco
		

class Roundedbotao(ButtonBehavior,LabelBotao):

	branco = ListProperty([1,1,1,1])
	preto = ListProperty([0,0,0,1])
	
	def __init__(self, **kwargs):
		super(Roundedbotao, self).__init__(**kwargs)
	def on_press(self):
		self.color = self.preto 
	def on_release(self):
		self.color = self.branco
class Pergunta(BoxLayout):
	pontos = 0
	selec = 0
	tempo = 0
	
	def __init__(self,pergunta='',args = [],**kwargs):
		
		super(Pergunta,self).__init__(**kwargs)
		# for key,val in self.ids.items():
		# 	print("key={0}, val={1}".format(key,val))
		
		self.ids.perg.text = pergunta
		
		self.ids.r1.text = args[0]#reposta
		self.ids.r10.flag = args[1]#flag certo ou errado(1 == certo, 0 == errado)
		self.ids.r10.group = str(args[8])

		self.ids.r2.text = args[2]
		self.ids.r20.flag = args[3]
		self.ids.r20.group = str(args[8])

		self.ids.r3.text = args[4]
		self.ids.r30.flag = args[5]
		self.ids.r30.group = str(args[8])

		self.ids.r4.text = args[6]
		self.ids.r40.flag = args[7]
		self.ids.r40.group = str(args[8])
	def guardabanco_t(self):#da pra usar o on_dismiss
		global quiz_nome,quiz_inicial,quiz_final,quiz_pontos

		self.tempo = ('{:.2f}'.format(quiz_final - quiz_inicial))
		
		
		if(quiz_nome == ''):
			print("Nenhum nome salvo")

		else:
			print("Salvo no banco de dados quiz = "+str(quiz_nome)+' '+str(self.tempo))
			
			banco = sqlite3.connect('quiz.db')
			c = banco.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real)''')
			parametros = []
			parametros = (quiz_nome,quiz_pontos,self.tempo)
			c.execute("INSERT INTO rank VALUES (?,?,?)",parametros)
			banco.commit()
			quiz_nome = ''
			self.__class__.tempo = 0
			quiz_pontos = 0
			
	def pop(self):
		global quiz_final, quiz_inicial,quiz_pontos
		
		# self.tempo = ('{:.2f}'.format(quiz_inicial - quiz_final))
		
		banco = sqlite3.connect('quiz.db')
		c = banco.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS rank (nome text,pontos integer,tempo real)''')
		dump = c.execute("SELECT count(tempo)from rank where tempo < ?",[self.tempo])##conta os de cima
		
		j = dump.fetchall()
		
		dump = []
		dump = c.execute("SELECT * FROM(SELECT * FROM(SELECT tempo,nome,pontos FROM rank WHERE tempo < ?)  as A ORDER BY tempo DESC limit 3) as B ORDER BY tempo ASC",[self.tempo])
		teste = dump.fetchall()
		

		teste.append((self.tempo,'%&marca&%',quiz_pontos))
		i = 0
		qtd_bank = j[0][0]
		indice = []
		
		if(qtd_bank > 0):
			if(qtd_bank >= 3):
				inic = qtd_bank-2
			else:
				if(qtd_bank == 2):
					inic = qtd_bank -1
				else:
					inic = qtd_bank
			qtd_bank+=1 
			for i in range(inic,qtd_bank,1):
				indice.append(i)
			#adc o do jogador
		else:
			
			indice.append(0)
			#adc o do jogador
		
		dump = c.execute("SELECT count(tempo)from rank where tempo > ?",[self.tempo])#conta os de baixo
		j = dump.fetchall()
		
		qtd_bank = j[0][0]
		i+=1
		indice.append(i)
		
		qtd_bank += (i+1)
		for k in range(i+1,qtd_bank,1):
			indice.append(k)
		
		
		dump = c.execute("SELECT * FROM(SELECT * FROM(SELECT tempo,nome,pontos FROM rank WHERE tempo > ?) as A ORDER BY tempo asc limit 3)",[self.tempo])
		
		qb = dump.fetchall()
		for i in qb:
			teste.append(i)
		cont = indice[0]

		pop = Popcustom(title='Fim de jogo',title_size='30sp',title_align='center',size_hint=(.1,.1),auto_dismiss=False,background = 'imagens/fundo.png', background_color=(0,0,0,.9),separator_color=(0,0,0,0))
		
		box = BoxLayoutCustom2()
		box.cor = 0.10,0.05,0,.9
		box.add_widget(Tarefa_two(text='N°'))
		box.add_widget(Tarefa_two(text='Nome'))
		box.add_widget(Tarefa_two(text='Pontos'))
		box.add_widget(Tarefa_two(text='Tempo'))
		pop.ids.box.add_widget(box)
		for tupla in teste:
			#print(str(cont)+' '+str(tupla[0])+' '+tupla[1]+' '+tupla[2])
			
			if (cont % 2 == 0):
				cor = [0.30,0.14,0,.6]
			else:
				cor = [0.30,0.14,0,.4]

			box = BoxLayoutCustom2()
			box.cor = cor
			if(tupla[1] == '%&marca&%'):
				box.add_widget(Tarefa_two(text=str(cont)))
				box.add_widget(Inserenome2())#nome
				box.add_widget(Tarefa_two(text=str(quiz_pontos)))
				box.add_widget(Tarefa_two(text=str(self.tempo)+'s'))#tempo(real)
			else:
				box.add_widget(Tarefa_two(text=str(cont)))
				box.add_widget(Tarefa_two(text=str(tupla[1])))#nome
				box.add_widget(Tarefa_two(text=str(tupla[2])))
				box.add_widget(Tarefa_two(text=str(tupla[0])+'s'))#tempo(real)
		
			pop.ids.box.add_widget(box)
			cont+=1

		b2 = BoxLayoutCustom2(orientation='vertical',cor=(1,1,1,0))
		b2.add_widget(Botao_custom(text='Fechar Popup',on_press = Pergunta.guardabanco_t ,on_release=pop.dismiss))
		pop.ids.box.add_widget(b2)
		#self.ids.scroll.scroll_to(box)
		anim = Animation(size_hint=(1,1),duration=1,t='out_back')
		anim.start(pop)
		Clock.schedule_once(pop.open, 0.5)

		
	def verifica(self,flag):
		global quiz_final,quiz_inicial,quiz_pontos
		
		
		self.__class__.selec+=1
		if(flag):
			print("Acertou")
			quiz_pontos+=1
			
		else:
			print("Errou")
		for child in self.children:
			
			flag = 0
			for child1 in reversed(child.children):
				#print(type(child1))
				if(child1.name == 'checkbox'):
					child1.disabled = True
					if(child1.flag == 1):
						flag = 1
				if(flag == 1):
					if(child1.name == 'label'):
						child1.color = 0.12,0.5,0,1
						flag = 0
		if(self.selec == 5): 
			quiz_final = time.time() 
			self.__class__.tempo = ('{:.2f}'.format(quiz_final - quiz_inicial))
			self.__class__.selec=0
			self.pop()


		
class InserenomeMemory(BoxLayout):
	nome = ''
	def __init__(self,**kwargs):
		super(InserenomeMemory,self).__init__(**kwargs)
	def salvanome(self):
		global nome
		self.nome = self.ids.texinp.text
		nome = self.nome
		self.ids.box1.add_widget(Tarefa_two(text=self.nome))
		
class Inserenome2(BoxLayout):
	nome = ''
	def __init__(self,**kwargs):
		super(Inserenome2,self).__init__(**kwargs)
	def salvanome(self):
		global quiz_nome
		
		self.nome = self.ids.texinp.text
		quiz_nome = self.nome
		self.ids.box1.add_widget(Tarefa_two(text=self.nome))
class Popcustom(Popup):
	def __init__(self,**kwargs):
		super(Popcustom,self).__init__(**kwargs)

class Botao_custom(ButtonBehavior,LabelBotao):
	def __init__(self,**kwargs):
		super(Botao_custom,self).__init__(**kwargs)
class Novo(App):
	title = 'Muhna'
		
	def build(self):
		print(LoggerHistory.history)
		return Gerenciador()
	
	def on_pause(self):
		'''
		Aqui voce pode salvar alguma coisa, caso necessario.
		Como dados de um banco de dados ainda em aberto.
		O que estiver na tela nao e necessario. Normalmente so retorne True.
		'''
		return True
	
	def on_resume(self):
		'''
		Aqui voce estara retornando ao seu App.
		Normalmente voce nao precisara fazer nada.
		'''
		pass
Novo().run()