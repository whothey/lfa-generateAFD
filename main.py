# @author Jefferson Coppini, Jonathan Rauber e Ricardo Muller
from estado import *
from transicoes import *
import csv
import os
from prettytable import PrettyTable

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

#Recebe como parametro uma linha da entrada referente a um token
#converte esse token em estados no AF
def leToken(linha):
	global AFND, ALFABETO, CONT_ESTADO
	flag = 0
	for i in AFND[0].transicoes:
		if i.rotulo == linha[0]:
			i.transicoes.append(CONT_ESTADO)
			flag = 1

	if flag == 0:
		transic = transicoes()
		transic.rotulo = linha[0]
		transic.transicoes.append(CONT_ESTADO)
		AFND[0].transicoes.append(transic)

	if linha[0] not in ALFABETO and linha[0] != 'ε':
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
		if linha[i] not in ALFABETO and linha[0] != 'ε':
			ALFABETO.append(linha[i])
		i += 1

	estad = estado()
	estad.rotulo = CONT_ESTADO
	estad.final = True
	CONT_ESTADO += 1
	AFND.append(estad)

#Recebe como parametro o estado, o terminal e o nao terminal da producao
#Cria o estado ou a transicao no AF caso necessário
#Caso em que a produção contem um terminal e um não terminal ex: a<A>
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

#Recebe como parametro o estado e o terminal da producao
#Cria a transicao no AF caso necessário
#Caso em que a produção contem apenas o terminal ex: ε
def Term(estad, term):
	global AFND, CONT_ESTADO, ALFABETO, ESTADOS

	cont = 0
	flag = 0
	for i in ESTADOS:
		if i.rotuloGr == estad:
			break
		cont += 1

	for i in ESTADOS[cont].transicoes:
		if i.rotulo == term:
			flag = 1
			i.transicoes.append(CONT_ESTADO)

	if flag == 0:
		transi = transicoes()
		transi.rotulo = term
		transi.transicoes.append(CONT_ESTADO)
		ESTADOS[cont].transicoes.append(transi)
	est = estado()
	est.final = True
	est.rotulo = CONT_ESTADO
	CONT_ESTADO += 1
	ESTADOS.append(est)
	AFND.append(est)

#Inicializa o vetor de estados, para controle na criação de estados com mesmo nome em gramaticas diferentes
def inicializaEST():
	global ESTADOS, AFND
	while ESTADOS:
		ESTADOS.pop(0)
	ESTADOS.append(AFND[0])

#Recebe como parametro uma linha da entrada referente a um Estado e suas produçoes
#converte essa linha em estados no AFD
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
		if term not in ALFABETO and term != 'ε':
			ALFABETO.append(term)
		I_LINHA += 1

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


#Imprime na tela automato nao deterministico
def printIdentAFND():
	header = ['δ'] + ALFABETO
	t = PrettyTable(header)
	for i in AFND:
		linha = []
		if i.final:
			linha = ['*' + str(i.rotulo)]
		else:
			linha = [i.rotulo]
		for k in ALFABETO:
			flag = 0
			for j in i.transicoes:
				if j.rotulo == k:
					linha = linha + [j.transicoes]
					flag = 1
			if flag == 0:
				linha = linha + ['X']
		t.add_row(linha)
	print(t)


#Imprime na tela automato deterministico
def printIdentAFD(comErro = False):
	header = ['δ'] + ALFABETO
	if comErro:
		header = header + ['x']
	t = PrettyTable(header)
	for i in AFD:
		if i.final:
			linha = ['*' + str(i.rotulo)]
		else:
			linha = [i.rotulo]
		for j in i.transicoes:
			if j.trans != -1:
				linha = linha + [j.trans]
			else:
				linha = linha + ['X']
		t.add_row(linha)
	print(t)


#função que determiniza o AFND
#cria o AFD
#Costroi o AFD a partir do estado inicial
#Por ser construído a partir de seu estado inicial a função elimina os estados inalcançaveis
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
		print()
		print("=======================")
		print()
		print("Determinização: ")
		printIdentAFD()
		print("\nFILA\n")
		print(fila)
		print()
		input("Tecle 'Enter' para continuar...")
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

#adiciona ao atributo alcancaveis de cada estado, os estados que podem ser alcançaveis a partir dele mesmo
#utilizado para verificação dos estados mortos
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

#Exclui do AFD o estado que não chega a algum estado final
#verifica em cada estado o vetor de alcancaveis, se nenhum deles for final o estado é eliminado
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

#insere estado de erro após automato ser minimizado
def insereEstErro():
	global AFD

	est = estado()
	est.rotulo = len(AFD)
	est.rotuloGr = 'X'
	est.final = True
	AFD.append(est)
	for k in ALFABETO:
		trans = transicoes()
		trans.trans = est.rotulo
		est.transicoes.append(trans)

	for i in AFD:
		for j in i.transicoes:
			if j.trans == -1:
				j.trans = est.rotulo
	for i in AFD:
		trans = transicoes()
		trans.trans = est.rotulo
		i.transicoes.append(trans)

#gera arquivo csv do AFD
def gerarCSV():
	global AFD

	alf = []
	alf.append("Estado")

	for i in ALFABETO:
		alf.append(i)

	f = open('AFD.csv','w')
	writer = csv.writer(f)

	writer.writerow(alf)
	for i in AFD:
		linha = []
		linha.append(i.rotulo)
		for j in i.transicoes:
			linha.append(j.trans)
		writer.writerow(linha)

def main():
	global CONT_ESTADO, AFND, ESTADOS

	os.system('clear')

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
			if(linha[0] != '<'):
				leToken(linha)
			else:
				leGR(linha)
		print("Autômato Finito Não Determinístico: \n")
		printIdentAFND()
		input("Tecle 'Enter' para continuar...")
		determinizar()
		print()
		print("=======================")
		print()
		print("Autômato Finito Determinístico:")
		printIdentAFD()
		input("Tecle 'Enter' para continuar...")
		mortos()
		insereEstErro()
		print()
		print("=======================")
		print()
		print("AFD Minimizado: ")
		printIdentAFD(comErro = True)
		gerarCSV()

main()
