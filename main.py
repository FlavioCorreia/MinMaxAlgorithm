from random import randint
aleatorio = randint(0,1) #VER QUEM COMEÇA PRIMEIRO

def imprime(tabuleiro):
    for i in range(9):
        if (i+1)%3 == 0:
            print("",tabuleiro[i])
        else:
            print("",tabuleiro[i],"|",end="")

    print("---------------------------------------------------------------")
        
def verifica(tabuleiro):#OLHA SE ALGUEM VENCEU
    for i in range(3):  #LINHAS
        if '_' != tabuleiro[3*i] == tabuleiro[3*i+1] == tabuleiro[3*i+2]:
            return tabuleiro[3*i]
    for i in range(3):  #COLUNAS
        if '_' != tabuleiro[i] == tabuleiro[3+i] == tabuleiro[6+i]:
            return tabuleiro[i]
    if '_' != tabuleiro[0] == tabuleiro[4] == tabuleiro[8]: #DIAGONAL 1
        return tabuleiro[0]
    if '_' != tabuleiro[2] == tabuleiro[4] == tabuleiro[6]: #DIAGONAL 2
        return tabuleiro[2]
    return ''

def preenchido(tabuleiro):#OLHA SE O TABULEIRO FOI PREENCHIDO TOTALMENTE
    for i in range(9):
        if tabuleiro[i] == '_':
            return False
    return True

def valorarArvore(arvRel,tabuleiro):
    if arvRel[tabuleiro][1] == []:          #SE NAO TIVER VALOR
        valores = []                        #LISTA QUE RECEBERÁ O VALOR DOS FILHOS
        for tabFilho in arvTab[tabuleiro]:
            valores += [valorarArvore(arvRel,tabFilho)]
            
        if arvRel[tabuleiro][2] % 2 == 0:   #SE ALTURA PAR, ENTAO NO É DE MAXIMIZACAO    
            melhor = max(valores)
            arvRel[tabuleiro][1] = melhor   #ATUALIZO AQUELE TABULEIRO

        else:                               #SE ALTURA IMPAR, ENTAO NO É DE MINIMIZACAO
            melhor = min(valores)
            arvRel[tabuleiro][1] = melhor   #ATUALIZO AQUELE TABULEIRO

        return melhor                       #RETORNO AO PAI

    else:                                   #SE NAO É VAZIO ENTAO TEM VALOR
        return arvRel[tabuleiro][1]         #RETORNO O VALOR DAQUELE NÓ
    
    

def criaComb(arvRel, tabuleiro, simbolo, jogador, maquina, altura):
    possibilidades = []
    for i in range(9):
        if tabuleiro[i] == '_':
            tAux = tabuleiro[:i] + simbolo + tabuleiro[i+1:] #TROCO O _ PELO SIMBOLO
            possibilidades += [tAux]
            ganhou = verifica(tAux) #OLHO SE ALGUEM GANHOU
            if ganhou == maquina:   #MAQUINHA GANHOU
                if aleatorio == 0:  #MAQUINA EH MIN
                    arvRel[tAux] = [tabuleiro, -1, altura+1]
                else:               #MAQUINA EH MAX
                    arvRel[tAux] = [tabuleiro, 1, altura+1]
                #subindo(arvRel, tAux, -1)
                
            elif ganhou == jogador: #JOGADOR GANHOU
                if aleatorio == 0:  #JOGADOR EH MAX
                    arvRel[tAux] = [tabuleiro, 1, altura+1]
                else:               #JOGADOR EH MIN
                    arvRel[tAux] = [tabuleiro, -1, altura+1]
                #subindo(arvRel, tAux, 1)            
                
            elif preenchido(tAux):  #OLHO SE O TABULEIRO FOI PREENCHIDO MAS NINGUEM GANHOU
                arvRel[tAux] = [tabuleiro, 0, altura+1]
                #subindo(arvRel, tAux, 0)
                
            else:                   #SEGUE O JOGO
                arvRel[tAux] = [tabuleiro,[], altura+1]
                
    return possibilidades

    
def criaArvore(arvTab, arvRel, tabuleiro, simbAtual, jogador, maquina, altura = 0): #TABULEIROS, RELACOES, S. ATUAL, S. JOG., S. MAQ.
    arvTab[tabuleiro] = criaComb(arvRel, tabuleiro, simbAtual, jogador, maquina, altura) #CRIAR COMBINACOES POSSIVEIS DO TABULEIRO
    for tabFilho in arvTab[tabuleiro]: #CONTINUAR A ARVORE NOS FILHOS QUE NAO SAO FOLHAS
        if arvRel[tabFilho][1] == []:
            if simbAtual == 'O':
                criaArvore(arvTab, arvRel, tabFilho, 'X', jogador, maquina, altura+1)
            else:
                criaArvore(arvTab, arvRel, tabFilho, 'O', jogador, maquina, altura+1)

arvTab = {} #CONTEM OS TABULEIROS           [TABULEIROS FILHOS]
arvRel = {} #CONTEM OS RELACIONAMENTOS      [TABULEIRO PAI, VALOR TABULEIRO, MAX/MIN] 
arvRel["_________"] = [[], [], 1]

print("Escolha: X | O")
jogador = input()   #JOGADOR ESCOLHE
while jogador != 'X' and jogador != 'O':
    jogador = input()

maquina = 'X'       #MAQUINA PEGA OQ SOBRAR
if jogador == 'X':
    maquina = 'O'

print("MAQUINA =",maquina,"| JOGADOR =",jogador)
print("CRIANDO ARVORE")
if aleatorio == 0: #ESCOLHER ALEATORIAMENTE QUEM COMECA
    criaArvore(arvTab, arvRel, "_________", jogador, jogador, maquina)
    print("O JOGADOR COMEÇA")
else:
    criaArvore(arvTab, arvRel, "_________", maquina, jogador, maquina)
    print("A MÁQUINA COMEÇA")

valorarArvore(arvRel,"_________") #ATRIBUO OS VALORES DOS NÓS NAO FOLHA

def maquinaJoga(tabuleiro):
    escolhas = []    
    for tb in arvTab[tabuleiro]: #OLHOS NOS FILHOS  DIRETOS DE TABULEIRO
        if escolhas == []:      #PEGO O PRIMEIRO SE ESTIVER VAZIO
            escolhas += [tb]

        elif aleatorio == 0:  #MAQUINA EH MIN
            if arvRel[escolhas[0]][1] > arvRel[tb][1]:      #SE OQ TENHO FOR MAIOR, ATUALIZO A LISTA COM O NOVO MENOR
                escolhas = [] 
                escolhas += [tb]
                
            elif arvRel[escolhas[0]][1] == arvRel[tb][1]:   #SE TIVER MESMO VALOR, ADICIONA NA LISTA
                escolhas += [tb]
                 
        else:               #MAQUINA EH MAX
            if arvRel[escolhas[0]][1] < arvRel[tb][1]:      #SE OQ TENHO FOR MENOR, ATUALIZO A LISTA COM O NOVO MAIOR
                escolhas = [] 
                escolhas += [tb]
                
            elif arvRel[escolhas[0]][1] == arvRel[tb][1]:   #SE TIVER MESMO VALOR, ADICIONA NA LISTA
                escolhas += [tb]
            
        
    tabuleiroEscolhido = escolhas[randint(0,len(escolhas)-1)] #ESCOLHO UM ALEATORIAMENTE ENTRE AS MELHORES ESCOLHAS
    return tabuleiroEscolhido

while True:
    print("---------------------------------------------------------------")
    print(" 0 | 1 | 2\n 3 | 4 | 5\n 6 | 7 | 8")
    print("---------------------------------------------------------------")
    tabuleiro = "_________" #TABULEIRO COMECA VAZIO
    alternaJogadorMaquina = aleatorio #VAR. RESP. POR ALTERNAR OS JOGADORES
    
    while verifica(tabuleiro) == '' and preenchido(tabuleiro) == False:
        imprime(tabuleiro)
        if alternaJogadorMaquina == 0:  #JOGADOR
            alternaJogadorMaquina = 1
            print("Escolha sua casa jogador:",end=" ")
            casa = int(input())
            tabuleiro = tabuleiro[:casa] + jogador + tabuleiro[casa+1:]
        else:                           #MAQUINA
            alternaJogadorMaquina = 0
            tabuleiro = maquinaJoga(tabuleiro)
    imprime(tabuleiro)
    
    if verifica(tabuleiro) != '':        
        print("(",verifica(tabuleiro),") GANHOU")
    else:
        print("- - - - EMPATOU - - - -")
    print("###############################################################")


































    
