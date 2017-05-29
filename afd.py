# dicionário chave-valor que mapeia estados, caracteres e transições, 
# na forma
# AFD = {
#		 'S': {
#			   's': ['A']
#			  }, 
#		 'A': {
#			   'e': ['B']
#			  }
#		}

transicoes = {} 
transicoes['S'] = {}
simbolos = []

def leToken(linha):
	global transicoes, simbolos #tem que escrever global quando vc quer alterar os valores das variaveis globais

def leGR(linha):
	global transicoes, simbolos


def main():
	#abre o arquivo em modo de leitura
	with open("entrada.txt", "r") as arquivo:
		for linha in arquivo:
			#não precisa nem ter cuidado se é EOF, objetos do tipo FILE são iteráveis em python
			if(linha[0] != '<') 
				leToken(linha)
			else
				leGR(linha)




main()
