# @author Jefferson Coppini, Jonathan Rauber
# @since 05/2017
# @descr
# 	dicionário chave-valor que mapeia estados, caracteres e transições,
# 	na forma
# 	AFND = {
#		 	'S': {
#				  's': ['A']
#				 },
#	   		'A': {
#			   	  'e': ['B']
#			  	 }
#		 	'B': {}
#		   }
#
# T -> transicoes
# cont -> contador_de_estado, indica o estado que está sendo produzido
# A -> alfabeto da linguagem
from collections import deque

AFND = {}		#AFND
AFD = {}
cont = 1
A = []		#ALFABETO DA LINGUAGEM
E = []		#ESTADOS
i_linha = 1

#Função que lê TOKENS do arquivo de entrada
def leToken(linha):
	#tem que escrever global quando vc quer alterar os valores das variaveis globais
	global AFND, cont, A
	if linha[0] not in AFND['S']:
		AFND['S'][linha[0]] = []
		if linha[0] not in A:
			A.append(linha[0])
	AFND['S'][linha[0]].append(cont)

	i = 1
	while linha[i] != '\n':
		AFND[cont] = {}
		E.append(cont)
		if linha[i] not in A:
			A.append(linha[i])
		AFND[cont][linha[i]] = []
		AFND[cont][linha[i]].append(cont+1)
		cont += 1
		i += 1
	AFND[cont] = {}
	E.append(cont)
	cont += 1

#Lê o estado entre os símbolos "<" e ">"
def splitNT (linha):
	global i_linha
	NT = ""

	while linha[i_linha] != '>':
		NT = NT + linha[i_linha]
		i_linha += 1
	return NT

#Lê uma linha do arquivo de entrada com uma gramática regular
def leGR(linha):
	global AFND, cont, A, i_linha
	#split para pegar o nome do estado
	i_linha = 1
	estado = splitNT(linha)
	if estado not in AFND:
		AFND[cont] = {}
		E.append(estado)
	while linha[i_linha] != ':':
		i_linha += 1
	i_linha += 3 #pula o simbolo da atribuição ::=
	while linha[i_linha] != '\n':
		while linha[i_linha] == ' ' or linha[i_linha] == '|': #verifica espaços iniciais ::=______
			i_linha += 1
		term = linha[i_linha]
		if term not in A:
			A.append(term)
		i_linha += 1
		if linha[i_linha] == '<':
			i_linha += 1
			nao_term = splitNT(linha)
			i_linha += 1
		else:
			while linha[i_linha] == ' ':
				i_linha += 1
			nao_term = cont
			cont += 1
			if linha[i_linha] == '|':
				i_linha += 1
		if term not in AFND[estado]:
			AFND[estado][term] = []
		if nao_term not in AFND[estado][term]:
			AFND[estado][term].append(nao_term)
			if nao_term not in AFND:
				AFND[nao_term] = {}
				E.append(nao_term)


# def determiniza():
# 	global AFD
# 	estadosAFD = []
#
# 	#implementação em fila
# 	#funcionamento:
# 	#1. coloca as transições do estado inicial na fila e só copia todo estado inicial
# 	#2. a partir daí, cria os estados através de remoção da fila
# 	fila = deque()
# 	AFD['S'] = AFND['S'] #copia o estado inicial de AFND para AFD
# 	for i in A:
# 		if i in AFND['S'] and i not in fila and i not in estadosAFD:
# 			fila.append(AFND['S'][i]) #coloca TODAS as transições de S por i, juntas, na fila
# 	while len(fila) > 0: #enquanto tiver estados na fila
# 		estado = fila.popleft() #tira a posição mais a esquerda da fila
# 		estado = tuple(estado)
# 		estadosAFD.append(estado)
# 		AFD[estado] = {} #cria o novo estado no AFD
# 		for i in estado:
# 			for j in A:
# 				if j in AFND[i]:
# 					if j not in AFD[estado]:
# 						AFD[estado][j] = []
# 					for k in AFND[i][j]:
# 						if k not in AFD[estado][j]:
# 							AFD[estado][j].append(k)
# 		for i in AFD[estado]:
# 			if AFD[estado][i] not in fila and AFD[estado][i] not in estadosAFD:
# 				fila.append(AFD[estado][i])
#
# 	for i in AFD:
# 		for j in AFD[i]:
# 			for k in AFD[i][j]:
# 				print(k)
# 			print()


def main():
	#abre o arquivo em modo de leitura
	with open("entrada.txt", "r") as arquivo:
		for linha in arquivo:
			if (linha[len(linha)-1] != '\n'):
				linha = linha + '\n'
			if not AFND:
				AFND['S'] = {}
				E.append('S')
			#não precisa nem ter cuidado se é EOF, objetos do tipo FILE são iteráveis em python
			if(linha[0] != '<'):
				leToken(linha)
			else:
				leGR(linha)
	print("&", end=" | ")
	for i in A:
		print(i, end=" | ")
	print("")
	for i in E:
		print(i, end=" ")
		for j in A:
			if j in AFND[i]:
				for k in AFND[i][j]:
					print(k, end=" ")
				print("", end=" ")
			else:
				print("NAO", end=" ")
		print("")


main()
