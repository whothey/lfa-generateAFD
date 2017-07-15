# @author Jefferson Coppini, Jonathan Rauber
from estado import *
from transicoes import *

AFND = []
ALFABETO = []
CONT_ESTADO = 0
I_LINHA = 0
ESTADOS = []

#Lê o estado entre os símbolos "<" e ">"
def splitNT (linha):
	global i_linha
	NT = ""

	while linha[i_linha] != '>':
		NT = NT + linha[i_linha]
		i_linha += 1
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
		if linha[0] not in ALFABETO:
			ALFABETO.append(linha[0])
		i += 1

	estad = estado()
	estad.rotulo = CONT_ESTADO
	estad.final = True
	CONT_ESTADO += 1
	AFND.append(estad)

def leGR(linha):
	global AFND, CONT_ESTADO, ALFABETO, I_LINHA, ESTADOS
	I_LINHA = 1
	flag = 0
	flag2 = 0
	estado = splitNT(linha)


	if estado == 'S':#Estado inicial da gramatica
		while linha[I_LINHA] != '\n':
			while linha[I_LINHA] == '>' or linha[I_LINHA] == ' ' or linha[I_LINHA] == ':' or linha[I_LINHA] == '='  or linha[I_LINHA] == '|':
				I_LINHA += 1
			term = linha[I_LINHA]
			I_LINHA += 1

			if term not in ALFABETO:
				ALFABETO.append(term)

			if linha[I_LINHA] == '<':
				nao_term = splitNT(linha)
				I_LINHA += 1
				for i in ESTADOS:
					if i.rotuloGr == nao_term:
						fla2 = 1
				if flag2 == 1:
						est = estado()
						est.rotulo = nao_term
						trans = transicoes()
						trans.rotulo = term
						trans.transicoes.append(nao_term)
						est.transicoes.append(trans)
						AFND.append(est)
						ESTADOS.append(nao_term)

			if estado == 'S':
				existeTransicaoPeloTerminal(term, 0)
			else
				existeTransicaoPeloTerminal(term, est.rotulo)



def existeTransicaoPeloTerminal(term, estado):
	for i in AFND[estado].transicoes:
		if i.rotulo == term
			i.transicoes.append(CONT_ESTADO)
			flag = 1

	if flag == 0: #linha[0] nao esta no estado inicial
		transic = transicoes()
		transic.rotulo = term
		transic.transicoes.append(CONT_ESTADO)
		AFND[estado].transicoes.append(transic)


			"""
				AFND[n].transicoes[n].transicoes

				AFND -> [0, 1, 2, 3]
				1 -> rotulo=1, transicoes=[a, b, c]
				a -> rotulo=a, transicoes[2, 3]
			"""

def printAFND():

	for i in AFND:
		print(i.rotulo, end = " ")
		for j in i.transicoes:
			print(j.transicoes, end = " ")
		print()

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
				AFND.append(est)
				CONT_ESTADO +=1

			if(linha[0] != '<'):
				leToken(linha)
			else:
				leGR(linha)
		printAFND()
main()
