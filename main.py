#!/usr/bin/python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image
from kivy.properties import StringProperty,NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.popup import Popup
from random import randint
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
import time
import random
import json

#Variaveis globais

tempo = 0
qtdimagens = 0
contador = 0
texto = []
pontos = 0
inicio = 0
fim = 0
flag = 0
ident = []
image = []
''' 
	*lembrar
	*	nao se esquecer que compila em python 2 (VM-buildozer)
	*	setxkbmap br = teclado em pt-br kivy (VM-buildozer)
	*	acerto.jpeg eh usado apenas como marcacao de acerto, nao eh uma imagem
	*
	*Fazer
	*	Adc cronometro 
	*	sql lite local
	*	therad kivy
	* 
'''
class Gerenciador(ScreenManager):
	pass  

class Menu(Screen):
	pass

class Quiz(Screen):
	def previous_screen(self, *args):
		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart)
	
	def restart(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart)
class Jogo(Screen):
	
	def __init__(self,tarefas=[],**kwargs):
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
			self.ids.gridlayout.add_widget(ImagemBloco(text=str(texto)))#adc a imagem no gridlayot

			texto = "imagens/"+str(selecionadoT)+'.jpg'
			self.ids.gridlayout.add_widget(ImagemBloco(text=str(texto)))

			cont+=2

	def previous_screen(self, *args):
		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart)
	
	def restart(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart)
	
	def previous_screen_limpa(self, *args):
		global fim
		global inicio
		global tempo
		global pontos,qtdimagens

		self.manager.transition.direction = 'right'
		self.manager.current = 'menu'
		self.manager.transition.bind(on_complete=self.restart_limpa)

		pontos = 0
		qtdimagens = 0
		inicio = 0
		fim=0

	def restart_limpa(self,  *args):
		self.manager.transition.direction = 'left'
		self.manager.transition.unbind(on_complete=self.restart_limpa)
		self.limpatela()
		global contador
		global texto
		contador = 0
		texto = []

	def limpatela(self,*args):#botao recomecar, limpa a tela e cria uma nova tela		
		self.parent.remove_widget(self)
		jogo = Jogo(name='jogo')
		self.parent.add_widget(jogo)

class ImagemBloco(BoxLayout):
	#lendo o json com os nomes dos anime/plantas
	conteudo = open('arquivo.json').read()
	arquivos = json.loads(conteudo)

	def __init__(self,text='',**kwargs):
		super(ImagemBloco,self).__init__(**kwargs)
		global flag
		global fim
		self.ids.button.text = text
		self.id = str(flag)
		self.text = text
		flag+=1
		
	def FimdeJogo(self,*args):
		# Espera o dismis do popup de imagem 
		global tempo
		fim = time.time()
		box = BoxLayout(orientation = 'vertical',padding=10,spacing=10)
		botoes = BoxLayout(padding=10,spacing=10)

		pop = Popup(title='Fim de jogo',title_size='30sp',title_align='center', content = box,size_hint=(.1,.1),background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))

		pontuacao = Botao(text = "Pontos = "+str(pontos))
		tempo = ('{:.2f}s'.format(fim-inicio))
		final = Botao(text = "Tempo = "+str(tempo))
		
		botoes.add_widget(pontuacao)
		botoes.add_widget(final)
		fechar = Botao(text = "Fechar popup",on_release = pop.dismiss)
		figura = Image(source='imagens/logo.png')
		
		box.add_widget(figura)
		box.add_widget(botoes)
		box.add_widget(fechar)
		anim = Animation(size_hint=(.8,.8),duration=0.1,t='out_back')
		anim.start(pop)
		pop.open()

	def AcertoImg(self,text=[]):

		box = BoxLayout(orientation = 'vertical')#,padding=10,spacing=10)
		figura = Image(source=str(text))		
		box.add_widget(figura)
		pop = Popup(title=self.arquivos[text],title_color=(1,1,1,1),title_size='30sp', content = box,size_hint=(.1,.1),title_align='center',background = 'imagens/fundo.png', background_color=(0,0,0,.8),separator_color=(0,0,0,0))#,size=(100,100))

		anim = Animation(size_hint=(.8,.8),duration=0.1,t='out_back')
		anim.start(pop)
		pop.open()
		Clock.schedule_once(pop.dismiss, 1.5)

	def troca(self,text=[]):#troca as imagens do botao

		global contador
		global texto
		global ident

		if(contador<2 and text != 'acerto.jpeg'):
			contador+=1
			texto.append(str(text))
			ident.append(self.id)
			if(self.ids.button.source and self.ids.button.text != 'acerto.jpeg'):
				self.ids.button.source = self.ids.button.text
				self.ids.button.canvas.ask_update()

		Clock.schedule_once(self.conta, 1)#chama a funcao 1s a frente

	def conta(self,text=[]):#verifica se as imagens sao iguais e altera para acerto.png, se nao ele volta para pergunta.png

		global contador
		global texto
		global ident
		global pontos
		global qtdimagens
		global fim
		
		if(contador == 2):
			if( (texto[0] == texto[1]) and (ident[0] != ident[1]) ):
				self.AcertoImg(texto[0])
				for child in self.parent.children:
					if(child.text == texto[0] and child.text != 'acerto.jpeg' ):	
						for child1 in child.children:
							child1.source = child1.text
							child1.text = 'acerto.jpeg'
				pontos+=1;
				if(pontos == qtdimagens):
					fim = time.time()
					Clock.schedule_once(self.FimdeJogo, 2)			
			else:
				for child in self.parent.children:
					for child1 in child.children:
						if(child1.source != 'imagens/pergunta.png' and child1.source != 'acerto.jpeg' and child1.text != 'acerto.jpeg'  ):
							child1.source = 'imagens/pergunta.png'						
			
			contador=0
			texto=[]
			ident=[]
		
	
class ImageButton(ButtonBehavior, Image): 
	def __init__(self, **kwargs):
		super(ImageButton, self).__init__(**kwargs)

class Botao(ButtonBehavior,Label): 
	cor = ListProperty([0.1,0.5,0.7,1])
	cor2 = ListProperty([0.1,0.1,0.1,1])
	def __init__(self, **kwargs):
		super(Botao, self).__init__(**kwargs)
	def on_press(self,*args):
		self.cor,self.cor2 = self.cor2,self.cor 

class Novo(App):
	icon = 'icone.png'
	title = 'Muhna'
		
	def build(self):
		#carrega as imagens para o vetor
		#o que esta atrasando a inicializacao, mas esta deixando 'mais jogavel'
		global image
		
		for i in range(1,29):
			image.append(Image(source='imagens/'+str(i)+'.jpg'))
		print(image)		
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