# dicionário chave-valor que mapeia estados, caracteres e transições, 
# na forma
# AFD = {
#		 'S': {
#			   's': ['A']
#			  }, 
#		 'A': {
#			   'e': ['B']
#			  }
#		 'B': {}
#		}
#
# T -> transicoes
# cont -> contador_de_estado, indica o estado que está sendo produzido
# A -> alfabeto da linguagem


T = {}
cont = 1
A = []
E = []
i_linha = 1

def leToken(linha):
	#tem que escrever global quando vc quer alterar os valores das variaveis globais
	global T, cont, A 
	if linha[0] not in T['S']:
		T['S'][linha[0]] = []
		if linha[0] not in A:
			A.append(linha[0])
	T['S'][linha[0]].append(cont)

	i = 1
	while linha[i] != '\n':
		T[cont] = {}
		E.append(cont)
		if linha[i] not in A:
			A.append(linha[i])
		T[cont][linha[i]] = []
		T[cont][linha[i]].append(cont+1)
		cont += 1
		i += 1 
	T[cont] = {}
	E.append(cont)
	cont += 1


def splitNT (linha):
	global i_linha
	NT = ""

	while linha[i_linha] != '>':
		NT = NT + linha[i_linha]
		i_linha += 1
	return NT

def leGR(linha):
	global T, cont, A, i_linha
	#split para pegar o nome do estado
	i_linha = 1
	estado = splitNT(linha)
	if estado not in T:
		T[estado] = {}
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
		if term not in T[estado]:
			T[estado][term] = []
		if nao_term not in T[estado][term]:
			T[estado][term].append(nao_term)
			if nao_term not in T:
				T[nao_term] = {}
				E.append(nao_term)




def main():
	#abre o arquivo em modo de leitura
	with open("entrada.txt", "r") as arquivo:
		for linha in arquivo:
			if (linha[len(linha)-1] != '\n'):
				linha = linha + '\n'
			if not T:
				T['S'] = {}
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
			if j in T[i]:
				for k in T[i][j]:
					print(k, end=" ")
				print("", end=" ")
			else:
				print("NAO", end=" ")
		print("")

main()
