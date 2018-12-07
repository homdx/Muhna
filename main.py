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
	----falta fazer
	* Quiz
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
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.popup import Popup
from random import randint
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
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

''' 
	*lembrar
	*	nao se esquecer que compila em python 2 (VM-buildozer)
	*	setxkbmap br = teclado em pt-br kivy (VM-buildozer)
	*	acerto.jpeg eh usado apenas como marcacao de acerto, nao eh uma imagem
	*
'''
class Gerenciador(ScreenManager):#gerenciado de telas
	pass 

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

	def fimdejogo(self,*args):
		# Espera o dismis do popup de imagem 
		global tempo,erro

		box = BoxLayout(orientation = 'vertical',padding=10,spacing=10)
		botoes = BoxLayout(padding=10,spacing=10)

		pop = Popup(title='Fim de jogo',title_size='30sp',title_align='center', content = box,size_hint=(.1,.1),background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))

		pontuacao = Botao(text = "Pontos = 0")
		final = Botao(text = "Tempo = 0s")
		erros = Botao(text='Erros = 0')
		
		botoes.add_widget(pontuacao)
		botoes.add_widget(final)
		botoes.add_widget(erros)

		textoF = Inserenome()

		fechar = Botao(text = "Fechar popup",on_release = pop.dismiss,on_press = Inserenome.guardabanco)
		figura = Image(source='imagens/logo.png')
		
		box.add_widget(figura)
		box.add_widget(botoes)
		box.add_widget(textoF)
		box.add_widget(fechar)
		anim = Animation(size_hint=(.8,.8),duration=0.3,t='out_back')
		anim.start(pop)
		pop.open()

class Pronto(BoxLayout):
	pass

class Teste(Screen):
	def __init__(self,**kwargs):
		super(Teste,self).__init__(**kwargs)
	
	def addImagem(self,valor):#adc os widgets com o text contendo os nomes das imagens		
		global inicio
		global qtdimagens

		qtdimagens = valor
		inicio = time.time()#inicia a contagem de tempo
		cont=0

		result = random.sample(range(1,29), valor)#gera um vetor de tamanho valor(4,6,10) entre 1 e 28(quantidade de imagens na pasta)
		nova = result[:]#copia do vetor
		random.shuffle(result)#result foi embaralhado
		

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
		teste = Teste(name='teste')
		self.parent.add_widget(teste)

class MyLabel(Image):#redimensiona os textos

	text = StringProperty('')
	def on_text(self, *args):
		# Just get large texture:
		l = Label(text="Selecione a quantidade de imagens",color=(0,0,0,1),bold=True)#,outline_width=40,outline_color=(0.22,0.10,0.03))
		l.font_size = '50dp'  # something that'll give texture bigger than phone's screen size
		l.texture_update()
		# Set it to image, it'll be scaled to image size automatically:
		self.texture = l.texture

class Quiz(Screen):#tela do quiz
	def previous_screen(self, *args):
		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart)
	
	def restart(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart)
class Jogo(Screen):#Tela do jogo da memoria
	
	def __init__(self,**kwargs):
		super(Jogo,self).__init__(**kwargs)
	
	def addImagem(self,valor):#adc os widgets com o text contendo os nomes das imagens		
		global inicio
		global qtdimagens

		qtdimagens = valor
		inicio = time.time()#inicia a contagem de tempo
		cont=0

		result = random.sample(range(1,29), valor)#gera um vetor de tamanho valor(4,6,10) entre 1 e 28(quantidade de imagens na pasta)
		nova = result[:]#copia do vetor
		random.shuffle(result)#result foi embaralhado

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

	def fimdejogo(self,*args):
		# Espera o dismis do popup de imagem 
		global tempo,erro

		fim = time.time()
		box = BoxLayout(orientation = 'vertical',padding=10,spacing=10)
		botoes = BoxLayout(padding=10,spacing=10)

		pop = Popup(title='Fim de jogo',title_size='30sp',title_align='center', content = box,size_hint=(.1,.1),background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))

		pontuacao = Botao(text = "Pontos = "+str(pontos))
		tempo = ('{:.2f}'.format(fim-inicio))
		final = Botao(text = "Tempo = "+str(tempo)+"s")
		erros = Botao(text='Erros = '+str(erro))
		
		botoes.add_widget(pontuacao)
		botoes.add_widget(final)
		botoes.add_widget(erros)

		textoF = Inserenome()

		fechar = Botao(text = "Fechar popup",on_release = pop.dismiss,on_press = Inserenome.guardabanco)
		figura = Image(source='imagens/logo.png')
		
		box.add_widget(figura)
		box.add_widget(botoes)
		box.add_widget(textoF)
		box.add_widget(fechar)
		anim = Animation(size_hint=(.8,.8),duration=0.3,t='out_back')
		anim.start(pop)
		pop.open()

	def AcertoImg(self,text=[]):

		box = BoxLayout(orientation = 'vertical')#,padding=10,spacing=10)

		figura = Image(source=str(text))		
		box.add_widget(figura)
		
		pop = Popup(title=self.arquivos[text],title_font='DejaVuSans',separator_height='0dp',title_color=(1,1,1,1),title_size='30sp', content = box,size_hint=(.1,.1),title_align='center',background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))#,size=(100,100))

		anim = Animation(size_hint=(1,1),duration=0.2,t='out_back')
		anim.start(pop)
		
		pop.open()
		
		Clock.schedule_once(pop.dismiss, 1.5)

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
					Clock.schedule_once(self.fimdejogo, 1.4)			
			else:
				erro+=1

				for child in self.parent.children:
					if(child.source != 'imagens/pergunta.png' and child.source != 'acerto.jpeg' and child.text != 'acerto.jpeg'  ):
						child.source = 'imagens/pergunta.png'						
			
			contador=0
			texto=[]
			ident=[]

class Tarefa(BoxLayout):

	def __init__(self,text='',**kwargs):
		super().__init__(**kwargs)
		self.ids.label.text = text

class BoxLayoutCustom(BoxLayout):
	pass

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
		dump = c.execute("SELECT nome,pontos,erros,tempo from rank ORDER BY tempo ASC, erros ASC, pontos DESC")
		contador = 1
		for linha in dump.fetchall():
			if (contador % 2 == 0):
				cor = (0,0,0, .4)
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
		
		self.ids.action.text=''
		self.ids.action.cor=0,0,0,1

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

		
class Tarefa(BoxLayout):

	def __init__(self,text='',**kwargs):
		super().__init__(**kwargs)
		self.ids.label.text = text
class LabelBotao(Image):

	text = StringProperty('')
	
	def __init__(self , **kwargs):
		super(LabelBotao, self).__init__(**kwargs)

	def on_text(self, *args):
		# Just get large texture:
		l = Label(text=str(self.text),font_name='RobotoMono-Regular.ttf',color=(1,1,1,1))#,outline_width=40,outline_color=(0.22,0.10,0.03))
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

class BotaoRounded(ButtonBehavior,LabelBotao):

	branco = ListProperty([1,1,1,1])
	preto = ListProperty([0,0,0,1])
	
	def __init__(self, **kwargs):
		super(BotaoRounded, self).__init__(**kwargs)
	def on_press(self):
		self.color = self.preto 
	def on_release(self):
		self.color = self.branco

class Novo(App):

	icon = 'icone.png'
	title = 'Muhna'
		
	def build(self):
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