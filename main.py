# @author Jefferson Coppini, Jonathan Rauber
from estado import *
from transicoes import *

AFND = []
ALFABETO = []
CONT_ESTADO = 0
I_LINHA = 0
ESTADOS = []
AFD = []

#Lê o estado entre os símbolos "<" e ">"
def splitNT (linha):
	global I_LINHA
	NT = ""

	while linha[I_LINHA] != '>':
		NT = NT + linha[I_LINHA]
		I_LINHA += 1
	return NT

def leToken(linha):
	global AFND, ALFABETO, CONT_ESTADO
	flag = 0
	for i in AFND[0].transicoes:
		if i.rotulo == linha[0]:#linha[0] esta no estado inicial
			i.transicoes.append(CONT_ESTADO)
			flag = 1

	if flag == 0: #linha[0] nao esta no estado inicial
		transic = transicoes()
		transic.rotulo = linha[0]
		transic.transicoes.append(CONT_ESTADO)
		AFND[0].transicoes.append(transic)

	if linha[0] not in ALFABETO:
		ALFABETO.append(linha[0])

	i = 1

	while linha[i] != '\n':
		estad = estado()
		estad.rotulo = CONT_ESTADO
		CONT_ESTADO += 1
		trans = transicoes()
		trans.rotulo = linha[i]
		trans.transicoes.append(CONT_ESTADO)
		estad.transicoes.append(trans)
		AFND.append(estad)
		if linha[i] not in ALFABETO:
			ALFABETO.append(linha[i])
		i += 1

	estad = estado()
	estad.rotulo = CONT_ESTADO
	estad.final = True
	CONT_ESTADO += 1
	AFND.append(estad)
	
def NaoTerm(estad,term,nao_term):
	global AFND, CONT_ESTADO, ALFABETO, ESTADOS
	flag = 0
	have_nao_term = False
	cont = 0
	rot = 0
	for i in ESTADOS:
		if i.rotuloGr == estad:
			break
		cont += 1
	
	for i in ESTADOS:
		if i.rotuloGr == nao_term:
			have_nao_term = True
			rot = i.rotulo
		
	
	for i in ESTADOS[cont].transicoes:
		if i.rotulo == term:
			flag = 1
			if have_nao_term == True:
				if rot not in i.transicoes:
					i.transicoes.append(rot)
			else:
				i.transicoes.append(CONT_ESTADO)
				est = estado()
				est.rotulo = CONT_ESTADO
				est.rotuloGr = nao_term
				CONT_ESTADO += 1
				ESTADOS.append(est)
				AFND.append(est)
			break
	
	if flag == 0:
		transi = transicoes()
		transi.rotulo = term
		if have_nao_term == True:
			transi.transicoes.append(rot)
		else:
			transi.transicoes.append(CONT_ESTADO)
			est = estado()
			est.rotulo = CONT_ESTADO
			est.rotuloGr = nao_term
			CONT_ESTADO += 1
			ESTADOS.append(est)
			AFND.append(est)
		ESTADOS[cont].transicoes.append(transi)

def Term(estad, term):
	global AFND, CONT_ESTADO, ALFABETO, ESTADOS	
	have_est_erro = False
	cont = 0
	rot = 0
	flag = 0
	
	for i in ESTADOS:
		if i.rotuloGr == estad:
			break
		cont += 1
	
	for i in ESTADOS:
		if i.rotuloGr == 'X':
			rot = i.rotulo

	for i in ESTADOS[cont].transicoes:
		if i.rotulo == term:
			flag = 1
			if rot not in i.transicoes:
				i.transicoes.append(rot)
	
	if flag == 0:
		transi = transicoes()
		transi.rotulo = term
		transi.transicoes.append(rot)
		ESTADOS[cont].transicoes.append(transi)

def inicializaEST():
	global ESTADOS, AFND
	while ESTADOS:
		ESTADOS.pop(0)
	ESTADOS.append(AFND[0])
	ESTADOS.append(AFND[1])
	
def leGR(linha):
	global AFND, CONT_ESTADO, ALFABETO, I_LINHA, ESTADOS
	I_LINHA = 1
	
	std = splitNT(linha)
	if std == 'S':
		inicializaEST()
	
	flag = 0
	for i in ESTADOS:
		if i.rotuloGr == std:
			flag = 1
	
	if flag == 0:
		est = estado()
		est.rotulo = CONT_ESTADO
		est.rotuloGr = std
		CONT_ESTADO += 1
		ESTADOS.append(est)
		AFND.append(est)
		

	while linha[I_LINHA] != '\n':
		while linha[I_LINHA] == '>' or linha[I_LINHA] == ' ' or linha[I_LINHA] == ':' or linha[I_LINHA] == '='  or linha[I_LINHA] == '|':
			I_LINHA += 1
		if linha[I_LINHA] == '\n':
			break
		term = linha[I_LINHA]
		if term not in ALFABETO:
			ALFABETO.append(term)
		I_LINHA += 1

		if term not in ALFABETO:
			ALFABETO.append(term)

		if linha[I_LINHA] == '<':
			I_LINHA += 1
			nao_term = splitNT(linha)
			I_LINHA += 1
			NaoTerm(std,term,nao_term)
			
		else:
			if term == 'ε':
				for i in ESTADOS:
					if i.rotuloGr == std:
						i.final = True
			Term(std,term)
		
		

def printAFND():

	for i in AFND:
		print(i.rotulo, end = " ")
		for j in i.transicoes:
			print(j.transicoes, end = " ")
		print()

def printAFD():

	for i in AFD:
		print(i.rotulo, end = " ")
		for j in i.transicoes:
			if j.trans != -1:
				print(j.trans, end = " ")
		print()
	

def determinizar():
	global  AFND, AFD, CONT_ESTADO
	CONTADOR = 0
	fila = []
	fila_aux = []
	lista = []
	lista.append(AFND[0].rotulo)
	fila.append(lista)
	fila_aux.append(lista)
	while fila:
		est = estado()
		est.rotulo = CONTADOR
		CONTADOR += 1
		for j in ALFABETO:
			cont = 0
			trans = transicoes()
			trans.rotulo = j
			for i in fila[0]:
				if AFND[i].final == True:
					est.final = True
				if AFND[i].inicial == True:
					est.inicial = True
				for k in AFND[i].transicoes:
					if k.rotulo == j:
						for l in k.transicoes:
							if l not in trans.transicoes: 
								trans.transicoes.append(l)
								trans.transicoes.sort()
			if trans.transicoes not in fila_aux:
				if trans.transicoes:
					fila.append(trans.transicoes)
					fila_aux.append(trans.transicoes)
			for c in fila_aux:
				if c == trans.transicoes:
					trans.trans = cont
				cont += 1
			est.transicoes.append(trans)
		AFD.append(est)
		fila.pop(0)	

def alcancaveis():
	global AFD
	change = True
	
	for i in AFD:
		if i.rotulo not in i.alcancaveis:
			i.alcancaveis.append(i.rotulo)
		for j in i.transicoes:
			if j.trans not in i.alcancaveis:
				if j.trans != -1:
					i.alcancaveis.append(j.trans) 
	while change:
		change = False
		for i in AFD:
			for j in i.alcancaveis:
				for k in AFD[j].alcancaveis:
					if k not in i.alcancaveis:
						i.alcancaveis.append(k)
						i.alcancaveis.sort()
						change = True
			 
def mortos():
	global AFD
	mortos = []
	alcancaveis()
	
	for i in AFD:
		have_final = False
		for j in i.alcancaveis:
			if AFD[j].final == True:
				have_final = True
		if have_final == False:
			mortos.append(i.rotulo)
			for k in AFD:
				cont = 0
				for j in k.transicoes:
					if j.trans == i.rotulo:
						j.trans = -1
	for i in mortos:
		cont = 0
		for j in AFD:
			if i == j.rotulo:
				AFD.pop(cont)
			cont += 1
						
def main():
	global CONT_ESTADO, AFND, ESTADOS
	#abre o arquivo em modo de leitura
	with open("entrada.txt", "r") as arquivo:
		for linha in arquivo:
			if (linha[len(linha)-1] != '\n'):
				linha = linha + '\n'
			if not AFND:
				est = estado()
				est.rotulo = CONT_ESTADO
				est.inicial = True
				est.rotuloGr = 'S'
				AFND.append(est)
				CONT_ESTADO +=1
				est = estado()
				est.rotulo = CONT_ESTADO
				est.final = True
				est.rotuloGr = 'X'
				AFND.append(est)
				CONT_ESTADO +=1
			if(linha[0] != '<'):
				leToken(linha)
			else:
				leGR(linha)
		printAFND()
		determinizar()
		printAFD()
		mortos()
		printAFD()
main()
