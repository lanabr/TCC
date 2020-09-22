import json as js
import shutil

class Resultado:
    def __init__(self):
        self.file = None

        self.trucoDescription = {}
        self.porcentagemDif   = 0.1
        self.codificacao      = [1, 2, 3, 4, 6, 7, 8, 12, 16, 24, 40, 42, 50, 52]
        self.ordem = ["4", "5", "6", "7", "10", "11", "12", "1", "2", "3", "7o", "7e", "1p", "1e"]
        self.pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/"

        # envido
        self.ganhouEnvido           = None
        self.maxEnvido              = 26
        self.cabecalhoMatProbEnvido = []
        self.matrizEnvidoVitoria    = [[]]
        self.matrizEnvidoDerrota    = [[]]

        # flor
        self.ganhouContraFlor     = None
        self.maxFlor              = 36
        self.cabecalhoMatProbFlor = []
        self.matrizFlorVitoria    = [[]]
        self.matrizFlorDerrota    = [[]]

        # truco
        self.ganhouTruco           = None
        self.maxTruco              = 73
        self.cabecalhoMatProbTruco = []
        self.matrizTrucoVitoria    = [[]]
        self.matrizTrucoDerrota    = [[]]

        # prox carta
        self.jogouCarta                   = False
        self.maxProxCarta                 = 11
        self.cabecalhoMatProbProximaCarta = []
        self.cabecalhoMatQtdCartas        = []
        self.matrizProximaCartaVitoria    = [[]]
        self.matrizProximaCartaDerrota    = [[]]
        self.matrizQtdCartas              = [[]]

    def main(self):
        self.file = open(self.pasta + "ganhos-truco-envido.txt", 'a+')

        self.trucoDescription = js.load(open(self.pasta + 'trucoDescription.json', 'r'))

        self.retiraResultados()
        if self.ganhouEnvido is not None:
            self.extraindoMatrizesEnvido()
            self.calculaEnvido()
            self.escrevendoMatrizesEnvido()
        if self.ganhouContraFlor is not None:
            self.extraindoMatrizesFlor()
            self.calculaFlor()
            self.escrevendoMatrizesFlor()
        if self.ganhouTruco is not None:
            self.extraindoMatrizesTruco()
            self.calculaTruco()
            self.escrevendoMatrizesTruco()
        if self.jogouCarta is not False:
            self.extraindoMatrizesProxCarta()
            self.calculaProxCarta()
            self.calculaQtdCarta()
            self.escrevendoMatrizesProxCarta()

    def retiraResultados(self):
        self.ganhouEnvido = self.trucoDescription["quemGanhouEnvido"]
        self.ganhouContraFlor = self.trucoDescription["quemGanhouFlor"]
        self.ganhouTruco = self.trucoDescription["quemGanhouTruco"]
        self.jogouCarta = self.trucoDescription["primeiraCartaRobo"] and self.trucoDescription["primeiraCartaHumano"]

    # prox carta
    def extraindoMatrizesProxCarta(self):
        vitoria   = open(self.pasta + 'matrizProximaCartaVitoria.txt', 'r')
        derrota   = open(self.pasta + 'matrizProximaCartaDerrota.txt', 'r')
        qtdCartas = open(self.pasta + 'matrizOrdemCartas.txt', 'r')
        matrizVit       = []
        matrizDer       = []
        matrizQtdCartas = []
        self.cabecalhoMatProbProximaCarta = vitoria.readline().split()
        self.cabecalhoMatQtdCartas        = qtdCartas.readline().split()

        for each in range(len(self.cabecalhoMatQtdCartas)):
            self.cabecalhoMatQtdCartas[each] = int(self.cabecalhoMatQtdCartas[each])

        cabecalho = derrota.readline()

        linhasVit = vitoria.readlines()
        linhasDer = derrota.readlines()
        linhasQtd = qtdCartas.readlines()

        for i in range(len(linhasVit)):
            matrizVit.append(linhasVit[i].split())

        for i in range(len(linhasDer)):
            matrizDer.append(linhasDer[i].split())

        for i in range(len(linhasQtd)):
            matrizQtdCartas.append(linhasQtd[i].split())

        for linha in range(len(matrizVit)):
            for coluna in range(len(matrizVit[linha])):
                matrizVit[linha][coluna] = int(matrizVit[linha][coluna])
                matrizDer[linha][coluna] = int(matrizDer[linha][coluna])

        for linha in range(len(matrizQtdCartas)):
            for coluna in range(len(matrizQtdCartas[linha])):
                matrizQtdCartas[linha][coluna] = int(matrizQtdCartas[linha][coluna])

        self.matrizProximaCartaVitoria = matrizVit
        self.matrizProximaCartaDerrota = matrizDer
        self.matrizQtdCartas           = matrizQtdCartas

        vitoria.close()
        derrota.close()
        qtdCartas.close()

    # prox carta
    def escrevendoMatrizesProxCarta(self):
        shutil.move(self.pasta + 'matrizProximaCartaVitoria.txt', self.pasta + 'antigos/' + 'matrizProximaCartaVitoria.txt')
        shutil.move(self.pasta + 'matrizProximaCartaDerrota.txt', self.pasta + 'antigos/' + 'matrizProximaCartaDerrota.txt')
        shutil.move(self.pasta + 'matrizOrdemCartas.txt', self.pasta + 'antigos/' + 'matrizOrdemCartas.txt')

        vitoria = open(self.pasta + 'matrizProximaCartaVitoria.txt', 'w')
        derrota = open(self.pasta + 'matrizProximaCartaDerrota.txt', 'w')
        qtdCartas = open(self.pasta + 'matrizOrdemCartas.txt', 'w')

        for elemento in self.cabecalhoMatProbProximaCarta:
            vitoria.write(str(elemento) + " ")
            derrota.write(str(elemento) + " ")

        for elemento in self.cabecalhoMatQtdCartas:
            qtdCartas.write(str(elemento) + " ")

        vitoria.write("\n")
        derrota.write("\n")
        qtdCartas.write("\n")

        for linha in self.matrizProximaCartaVitoria:
            for coluna in linha:
                vitoria.write(str(round(coluna)) + " ")
            vitoria.write("\n")

        for linha in self.matrizProximaCartaDerrota:
            for coluna in linha:
                derrota.write(str(round(coluna)) + " ")
            derrota.write("\n")

        for linha in self.matrizQtdCartas:
            for coluna in linha:
                qtdCartas.write(str(round(coluna)) + " ")
            qtdCartas.write("\n")

        vitoria.close()
        derrota.close()
        qtdCartas.close()

    # prox carta
    def calculaProxCarta(self):
        combRobo = []
        combHumano = []

        if self.trucoDescription['primeiraCartaRobo'] is None or self.trucoDescription['segundaCartaRobo'] is None or self.trucoDescription['terceiraCartaRobo'] is None:
            combRobo = self.defineCombMao(None)
        elif self.trucoDescription['primeiraCartaRobo'] is 0 or self.trucoDescription['segundaCartaRobo'] is 0 or self.trucoDescription['terceiraCartaRobo'] is 0:
            combRobo = self.defineCombMao(0)
        else:
            comb = self.combinacoesProxCarta(self.trucoDescription['primeiraCartaRobo'], self.trucoDescription['segundaCartaRobo'],
                                             self.trucoDescription['terceiraCartaRobo'], self.trucoDescription['cartaBaixaRobo'],
                                             self.trucoDescription['cartaMediaRobo'], self.trucoDescription['cartaAltaRobo'])
            combRobo.append(comb)

        if self.trucoDescription['primeiraCartaHumano'] is None or self.trucoDescription['segundaCartaHumano'] is None or self.trucoDescription['terceiraCartaHumano'] is None:
            combHumano = self.definePossiveisCombMao(None)
        elif self.trucoDescription['primeiraCartaHumano'] is 0 or self.trucoDescription['segundaCartaHumano'] is 0 or self.trucoDescription['terceiraCartaHumano'] is 0:
            combHumano = self.definePossiveisCombMao(0)
        else:
            comb = self.combinacoesProxCarta(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'],
                                             self.trucoDescription['terceiraCartaHumano'], self.trucoDescription['cartaBaixaHumano'],
                                             self.trucoDescription['cartaMediaHumano'], self.trucoDescription['cartaAltaHumano'])
            combHumano.append(comb)

        if len(combRobo) == 0 or len(combHumano) == 0:
            pass
        else:
            diferenca = self.maxProxCarta * self.porcentagemDif
            diferenca = round(diferenca / (len(combHumano) * len(combRobo)))

            ganhadorPrimeiraRodada = self.trucoDescription['ganhadorPrimeiraRodada']
            ganhadorSegundaRodada = self.trucoDescription['ganhadorSegundaRodada']
            ganhadorTerceiraRodada = self.trucoDescription['ganhadorTerceiraRodada']

            if ganhadorPrimeiraRodada is not None and ganhadorSegundaRodada is not None:
                if ganhadorPrimeiraRodada == 1 and ganhadorSegundaRodada == 1:
                    self.atualizaMatriz(1, diferenca, combRobo, combHumano)
                elif ganhadorPrimeiraRodada == 0 and ganhadorSegundaRodada == 1:
                    self.atualizaMatriz(1, diferenca, combRobo, combHumano)
                elif ganhadorPrimeiraRodada == 1 and ganhadorSegundaRodada == 0:
                    self.atualizaMatriz(1, diferenca, combRobo, combHumano)

                if ganhadorPrimeiraRodada == 2 and ganhadorSegundaRodada == 2:
                    self.atualizaMatriz(2, diferenca, combRobo, combHumano)
                elif ganhadorPrimeiraRodada == 0 and ganhadorSegundaRodada == 2:
                    self.atualizaMatriz(2, diferenca, combRobo, combHumano)
                elif ganhadorPrimeiraRodada == 2 and ganhadorSegundaRodada == 0:
                    self.atualizaMatriz(2, diferenca, combRobo, combHumano)

                if ganhadorTerceiraRodada is not None:
                    if ganhadorPrimeiraRodada == 1 and ganhadorTerceiraRodada == 1:
                        self.atualizaMatriz(1, diferenca, combRobo, combHumano)
                    elif ganhadorSegundaRodada == 1 and ganhadorTerceiraRodada == 1:
                        self.atualizaMatriz(1, diferenca, combRobo, combHumano)

                    if ganhadorPrimeiraRodada == 2 and ganhadorTerceiraRodada == 2:
                        self.atualizaMatriz(2, diferenca, combRobo, combHumano)
                    elif ganhadorSegundaRodada == 2 and ganhadorTerceiraRodada == 2:
                        self.atualizaMatriz(2, diferenca, combRobo, combHumano)

                    if ganhadorPrimeiraRodada == 0 and ganhadorSegundaRodada == 0 and ganhadorTerceiraRodada == 1:
                        self.atualizaMatriz(1, diferenca, combRobo, combHumano)
                    elif ganhadorPrimeiraRodada == 0 and ganhadorSegundaRodada == 0 and ganhadorTerceiraRodada == 2:
                        self.atualizaMatriz(2, diferenca, combRobo, combHumano)
                    elif ganhadorPrimeiraRodada == 1 and ganhadorSegundaRodada == 1 and ganhadorTerceiraRodada == 0:
                        self.atualizaMatriz(1, diferenca, combRobo, combHumano)
                    elif ganhadorPrimeiraRodada == 2 and ganhadorSegundaRodada == 1 and ganhadorTerceiraRodada == 0:
                        self.atualizaMatriz(2, diferenca, combRobo, combHumano)

    # prox carta
    def atualizaMatriz(self, ganhador, diferenca, combRobo, combHumano):
        if ganhador == 1:
            for j in range(len(combRobo)):
                for i in range(len(combHumano)):
                    self.matrizProximaCartaVitoria[self.cabecalhoMatProbProximaCarta.index(combRobo[j])][self.cabecalhoMatProbProximaCarta.index(combHumano[i])] += diferenca
                    self.matrizProximaCartaDerrota[self.cabecalhoMatProbProximaCarta.index(combHumano[i])][self.cabecalhoMatProbProximaCarta.index(combRobo[j])] += diferenca
        elif ganhador == 2:
            for j in range(len(combRobo)):
                for i in range(len(combHumano)):
                    self.matrizProximaCartaVitoria[self.cabecalhoMatProbProximaCarta.index(combHumano[i])][self.cabecalhoMatProbProximaCarta.index(combRobo[j])] += diferenca
                    self.matrizProximaCartaDerrota[self.cabecalhoMatProbProximaCarta.index(combRobo[j])][self.cabecalhoMatProbProximaCarta.index(combHumano[i])] += diferenca

    # prox carta
    def combinacoesProxCarta(self, primeiraCarta, segundaCarta, terceiraCarta, cartaBaixa, cartaMedia, cartaAlta):
        carta1 = ""
        carta2 = ""
        carta3 = ""
        comb = None

        if primeiraCarta == cartaBaixa: carta1 = "b"
        elif primeiraCarta == cartaMedia: carta1 = "m"
        elif primeiraCarta == cartaAlta: carta1 = "a"

        if segundaCarta == cartaBaixa: carta2 = "b"
        elif segundaCarta == cartaMedia: carta2 = "m"
        elif segundaCarta == cartaAlta: carta2 = "a"

        if terceiraCarta == cartaBaixa: carta3 = "b"
        elif terceiraCarta == cartaMedia: carta3 = "m"
        elif terceiraCarta == cartaAlta: carta3 = "a"

        if carta1 not in carta2 and carta1 not in carta3 and carta2 not in carta3: # todas diferentes
            comb = carta1 + carta2 + carta3
        if carta1 == carta2 and carta2 == carta3: # todas iguais
            if carta1 == "b": comb = "bma" # se começou achando que é baixa, só cresce
            if carta1 == "m": comb = "mab" # se começou com média, cresce e depois baixa
            if carta1 == "a": comb = "amb" # se começou com alta, só baixa
        if carta1 == carta2 and carta1 not in carta3 and carta2 not in carta3: # se as duas primeiras forem iguais, confia sempre na primeira
            if carta1 == "b": # bbm -> bma, bba -> bma
                comb = "bma"
            if carta1 == "m":
                if carta3 == "b": # mmb -> mab
                    comb = "mab"
                if carta3 == "a": # mma -> mba
                    comb = "mba"
            if carta1 == "a": # aab -> amb, aam -> amb
                comb = "amb"
        if carta1 == carta3 and carta1 not in carta2 and carta3 not in carta2: # se a primeira e a ultima forem iguais
            if carta1 == "b": # bmb -> bam, bab -> bam
                comb = "bam"
            if carta1 == "m":
                if carta2 == "b": # mbm -> mba
                    comb = "mba"
                if carta2 == "a": # mam -> mab
                    comb = "mab"
            if carta1 == "a": # aba -> abm, ama -> abm
                comb = "abm"
        if carta2 == carta3 and carta2 not in carta1 and carta3 not in carta1: # se a segunda e a ultima forem iguais
            if carta2 == "b": # mbb -> abm, abb -> abm
                comb = "abm"
            if carta2 == "m":
                if carta1 == "b": # bmm -> bma
                    comb = "bma"
                if carta1 == "a": # amm -> amb
                    comb = "amb"
            if carta2 == "a": # baa -> bam, maa -> bam
                comb = "bam"

        return comb

    # prox carta
    def defineCombMao(self, qual):
        primeiraCartaRobo = self.trucoDescription['primeiraCartaRobo']
        segundaCartaRobo = self.trucoDescription['segundaCartaRobo']
        terceiraCartaRobo = self.trucoDescription['terceiraCartaRobo']

        combRobo = []

        if primeiraCartaRobo == qual and segundaCartaRobo == qual and terceiraCartaRobo == qual:
            pass
        elif primeiraCartaRobo != qual and segundaCartaRobo == qual and terceiraCartaRobo == qual:
            for comb in self.cabecalhoMatProbProximaCarta:
                if comb[0] == self.nivelCartaJogada(primeiraCartaRobo, self.trucoDescription['primeiraCartaRobo'], self.trucoDescription['segundaCartaRobo'], self.trucoDescription['terceiraCartaRobo']):
                    combRobo.append(comb)
        elif primeiraCartaRobo != qual and segundaCartaRobo != qual and terceiraCartaRobo == qual:
            niveis = ["b", "m", "a"]
            nivelCarta1 = self.nivelCartaJogada(primeiraCartaRobo, self.trucoDescription['cartaBaixaRobo'], self.trucoDescription['cartaMediaRobo'], self.trucoDescription['cartaAltaRobo'])
            nivelCarta2 = self.nivelCartaJogada(segundaCartaRobo, self.trucoDescription['cartaBaixaRobo'], self.trucoDescription['cartaMediaRobo'], self.trucoDescription['cartaAltaRobo'])

            if nivelCarta1 == nivelCarta2:
                if nivelCarta1 == "b": nivelCarta2 = "m"
                if nivelCarta1 == "a": nivelCarta2 = "m"
                if nivelCarta1 == "m":
                    if self.cabecalhoMatQtdCartas.index(primeiraCartaRobo) > len(self.cabecalhoMatQtdCartas) / 2:
                        nivelCarta2 = "a"
                    else:
                        nivelCarta2 = "b"

            niveis.remove(nivelCarta1)
            niveis.remove(nivelCarta2)
            combRobo.append(nivelCarta1 + nivelCarta2 + niveis[0])

        return combRobo

    # prox carta
    def definePossiveisCombMao(self, qual):
        primeiraCartaHumano = self.trucoDescription['primeiraCartaHumano']
        segundaCartaHumano = self.trucoDescription['segundaCartaHumano']
        terceiraCartaHumano = self.trucoDescription['terceiraCartaHumano']

        combHumano = []

        if primeiraCartaHumano == qual and segundaCartaHumano == qual and terceiraCartaHumano == qual:
            pass
        elif primeiraCartaHumano != qual and segundaCartaHumano == qual and terceiraCartaHumano == qual:
            nivelCarta = self.analisaNivelCarta(primeiraCartaHumano)  # analisa qual carta foi jogada
            listaCartasRestantes = self.analisaCartasRestantes(nivelCarta)  # ve quais cartas sobraram

            combHumano.append(nivelCarta + listaCartasRestantes[0] + listaCartasRestantes[1])
            combHumano.append(nivelCarta + listaCartasRestantes[1] + listaCartasRestantes[0])
        elif primeiraCartaHumano != qual and segundaCartaHumano != qual and terceiraCartaHumano == qual:
            niveis = ["b", "m", "a"]
            nivelCarta1 = self.analisaNivelCarta(primeiraCartaHumano)
            nivelCarta2 = self.analisaNivelCarta(segundaCartaHumano)

            if nivelCarta1 == nivelCarta2:
                carta1 = self.cabecalhoMatQtdCartas.index(primeiraCartaHumano)
                carta2 = self.cabecalhoMatQtdCartas.index(segundaCartaHumano)

                if carta1 > carta2:
                    if niveis.index(nivelCarta1) + 1 >= len(niveis):
                        nivelCarta2 = niveis[niveis.index(nivelCarta2) - 1]
                    else:
                        nivelCarta1 = niveis[niveis.index(nivelCarta1) + 1]
                else:
                    if niveis.index(nivelCarta2) + 1 >= len(niveis):
                        nivelCarta1 = niveis[niveis.index(nivelCarta1) - 1]
                    else:
                        nivelCarta2 = niveis[niveis.index(nivelCarta2) + 1]

            niveis.remove(nivelCarta1)
            niveis.remove(nivelCarta2)

            combHumano.append(nivelCarta1 + nivelCarta2 + niveis[0])

        return combHumano

    # prox carta
    def nivelCartaJogada(self, carta, cartaBaixaRobo, cartaMediaRobo, cartaAltaRobo):
        if carta == cartaBaixaRobo:
            return "b"
        elif carta == cartaMediaRobo:
            return "m"
        elif carta == cartaAltaRobo:
            return "a"

    # prox carta
    def analisaCartasRestantes(self, carta):
        if carta == "b":
            return ["m", "a"]
        elif carta == "m":
            return ["b", "a"]
        elif carta == "a":
            return ["b", "m"]

    # prox carta
    def analisaNivelCarta(self, carta):
        qtdB = self.matrizQtdCartas[0][self.cabecalhoMatQtdCartas.index(carta)]
        qtdM = self.matrizQtdCartas[1][self.cabecalhoMatQtdCartas.index(carta)]
        qtdA = self.matrizQtdCartas[2][self.cabecalhoMatQtdCartas.index(carta)]

        if qtdB >= qtdM and qtdB >= qtdA:
            return "b"
        elif qtdM >= qtdB and qtdM >= qtdA:
            return "m"
        elif qtdA >= qtdB and qtdA >= qtdM:
            return "a"

    # prox carta
    def calculaQtdCarta(self):
        b = 0
        m = 1
        a = 2

        self.matrizQtdCartas[b][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaBaixaRobo'])] += 1
        self.matrizQtdCartas[m][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaMediaRobo'])] += 1
        self.matrizQtdCartas[a][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaAltaRobo'])] += 1

        if self.trucoDescription['cartaBaixaHumano'] is not None and self.trucoDescription['cartaBaixaHumano'] is not 0:
            self.matrizQtdCartas[b][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaBaixaHumano'])] += 1
        if self.trucoDescription['cartaMediaHumano'] is not None and self.trucoDescription['cartaMediaHumano'] is not 0:
            self.matrizQtdCartas[m][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaMediaHumano'])] += 1
        if self.trucoDescription['cartaAltaHumano'] is not None and self.trucoDescription['cartaAltaHumano'] is not 0:
            self.matrizQtdCartas[a][self.cabecalhoMatQtdCartas.index(self.trucoDescription['cartaAltaHumano'])] += 1

    # truco
    def extraindoMatrizesTruco(self):
        vitoria   = open(self.pasta + 'matrizTrucoVitoria.txt', 'r')
        derrota   = open(self.pasta + 'matrizTrucoDerrota.txt', 'r')
        matrizVit = []
        matrizDer = []
        self.cabecalhoMatProbTruco = vitoria.readline().split()
        cabecalho = derrota.readline()

        linhasVit = vitoria.readlines()
        linhasDer = derrota.readlines()

        for i in range(len(linhasVit)):
            matrizVit.append(linhasVit[i].split())

        for i in range(len(linhasDer)):
            matrizDer.append(linhasDer[i].split())

        for linha in range(len(matrizVit)):
            for coluna in range(len(matrizVit[linha])):
                matrizVit[linha][coluna] = int(matrizVit[linha][coluna])
                matrizDer[linha][coluna] = int(matrizDer[linha][coluna])

        self.matrizTrucoVitoria = matrizVit
        self.matrizTrucoDerrota = matrizDer

        vitoria.close()
        derrota.close()

    # truco
    def escrevendoMatrizesTruco(self):
        shutil.move(self.pasta + 'matrizTrucoVitoria.txt', self.pasta + 'antigos/' + 'matrizTrucoVitoria.txt')
        shutil.move(self.pasta + 'matrizTrucoDerrota.txt', self.pasta + 'antigos/' + 'matrizTrucoDerrota.txt')

        vitoria = open(self.pasta + 'matrizTrucoVitoria.txt', 'w')
        derrota = open(self.pasta + 'matrizTrucoDerrota.txt', 'w')

        for elemento in self.cabecalhoMatProbTruco:
            vitoria.write(str(elemento) + " ")
            derrota.write(str(elemento) + " ")

        vitoria.write("\n")
        derrota.write("\n")

        for linha in self.matrizTrucoVitoria:
            for coluna in linha:
                vitoria.write(str(round(coluna)) + " ")
            vitoria.write("\n")

        for linha in self.matrizTrucoDerrota:
            for coluna in linha:
                derrota.write(str(round(coluna)) + " ")
            derrota.write("\n")

        vitoria.close()
        derrota.close()

    # truco
    def calculaTruco(self):
        pontosRobo = str(self.trucoDescription['cartaBaixaRobo']) + str(self.trucoDescription['cartaMediaRobo']) + str(self.trucoDescription['cartaAltaRobo'])
        diferenca = self.maxTruco * self.porcentagemDif
        pontosHumano = []

        if self.trucoDescription['cartaBaixaHumano'] is None or self.trucoDescription['cartaMediaHumano'] is None or self.trucoDescription['cartaAltaHumano'] is None:
            pontosHumano = self.definePossiveisCombTruco(None)
        elif self.trucoDescription['cartaBaixaHumano'] is 0 or self.trucoDescription['cartaMediaHumano'] is 0 or self.trucoDescription['cartaAltaHumano'] is 0:
            pontosHumano = self.definePossiveisCombTruco(0)
        else:
            pontosHumano.append(str(self.trucoDescription['cartaBaixaHumano']) + str(self.trucoDescription['cartaMediaHumano']) + str(self.trucoDescription['cartaAltaHumano']))

        diferenca = round(diferenca / len(pontosHumano))

        if self.ganhouTruco == 1:
            self.file.write("ganhou truco na partida " + self.trucoDescription['idPartida'] + "\n")
            for i in range(len(pontosHumano)):
                self.matrizTrucoVitoria[self.cabecalhoMatProbTruco.index(pontosRobo)][self.cabecalhoMatProbTruco.index(pontosHumano[i])] += diferenca
                self.matrizTrucoDerrota[self.cabecalhoMatProbTruco.index(pontosHumano[i])][self.cabecalhoMatProbTruco.index(pontosRobo)] += diferenca
        else:
            self.file.write("perdeu truco na partida " + self.trucoDescription['idPartida'] + "\n")
            for i in range(len(pontosHumano)):
                self.matrizTrucoVitoria[self.cabecalhoMatProbTruco.index(pontosHumano[i])][self.cabecalhoMatProbTruco.index(pontosRobo)] += diferenca
                self.matrizTrucoDerrota[self.cabecalhoMatProbTruco.index(pontosRobo)][self.cabecalhoMatProbTruco.index(pontosHumano[i])] += diferenca

    # truco
    def definePossiveisCombTruco(self, qual):
        primeiraCartaHumano = self.trucoDescription['primeiraCartaHumano']
        segundaCartaHumano = self.trucoDescription['segundaCartaHumano']
        terceiraCartaHumano = self.trucoDescription['terceiraCartaHumano']

        possiveisCombTruco = []
        if primeiraCartaHumano is qual and segundaCartaHumano is qual and terceiraCartaHumano is qual:
            possiveisCombTruco = self.cabecalhoMatProbTruco.copy()
        elif primeiraCartaHumano is not qual and segundaCartaHumano is qual and terceiraCartaHumano is qual:
            for segundaCarta in range(0, len(self.codificacao)):
                for terceiraCarta in range(segundaCarta, len(self.codificacao)):
                    if self.validadeComb(primeiraCartaHumano, self.codificacao[segundaCarta], self.codificacao[terceiraCarta]):
                        possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, self.codificacao[segundaCarta], self.codificacao[terceiraCarta]))
        elif primeiraCartaHumano is not qual and segundaCartaHumano is not qual and terceiraCartaHumano is qual:
            for terceiraCarta in range(0, len(self.codificacao)):
                if self.validadeComb(primeiraCartaHumano, segundaCartaHumano, self.codificacao[terceiraCarta]):
                    possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, segundaCartaHumano, self.codificacao[terceiraCarta]))
        elif primeiraCartaHumano is not qual and segundaCartaHumano is not qual and terceiraCartaHumano is not qual:
            possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, segundaCartaHumano, terceiraCartaHumano))

        return possiveisCombTruco

    # truco
    def validadeComb(self, carta1, carta2, carta3):
        repUnica = [40, 42, 50, 52]

        if carta1 == 4 and carta2 == 4:
            if carta3 == 4:
                return False
            else:
                return True
        elif carta1 == 12 and carta2 == 12:
            if carta3 == 12:
                return False
            else:
                return True
        elif carta1 in repUnica or carta2 in repUnica or carta3 in repUnica:
            if (carta1 == carta2 and (carta1 in repUnica or carta2 in repUnica)) or (carta2 == carta3 and (
                    carta3 in repUnica or carta2 in repUnica)) or (carta1 == carta3 and (carta1 in repUnica or carta3 in repUnica)):
                return False
            else:
                return True
        else:
            return True

    # truco
    def arrumaCombinacao(self, carta1, carta2, carta3):
        if carta1 <= carta2 <= carta3:
            return str(carta1) + str(carta2) + str(carta3)
        elif carta1 <= carta3 <= carta2:
            return str(carta1) + str(carta3) + str(carta2)
        elif carta2 <= carta1 <= carta3:
            return str(carta2) + str(carta1) + str(carta3)
        elif carta2 <= carta3 <= carta1:
            return str(carta2) + str(carta3) + str(carta1)
        elif carta3 <= carta1 <= carta2:
            return str(carta3) + str(carta1) + str(carta2)
        elif carta3 <= carta2 <= carta1:
            return str(carta3) + str(carta2) + str(carta1)

    # flor
    def extraindoMatrizesFlor(self):
        vitoria = open(self.pasta + 'matrizContraFlorVitoria.txt', 'r')
        derrota = open(self.pasta + 'matrizContraFlorDerrota.txt', 'r')
        matrizVit = []
        matrizDer = []
        self.cabecalhoMatProbFlor = vitoria.readline().split()
        cabecalho = derrota.readline()

        linhasVit = vitoria.readlines()
        linhasDer = derrota.readlines()

        for i in range(len(linhasVit)):
            matrizVit.append(linhasVit[i].split())

        for i in range(len(linhasDer)):
            matrizDer.append(linhasDer[i].split())

        for linha in range(len(matrizVit)):
            for coluna in range(len(matrizVit[linha])):
                matrizVit[linha][coluna] = int(matrizVit[linha][coluna])
                matrizDer[linha][coluna] = int(matrizDer[linha][coluna])

        self.matrizFlorVitoria = matrizVit
        self.matrizFlorDerrota = matrizDer

        vitoria.close()
        derrota.close()

    # flor
    def escrevendoMatrizesFlor(self):
        shutil.move(self.pasta + 'matrizContraFlorVitoria.txt', self.pasta + 'antigos/' + 'matrizContraFlorVitoria.txt')
        shutil.move(self.pasta + 'matrizContraFlorDerrota.txt', self.pasta + 'antigos/' + 'matrizContraFlorDerrota.txt')

        vitoria = open(self.pasta + 'matrizContraFlorVitoria.txt', 'w')
        derrota = open(self.pasta + 'matrizContraFlorDerrota.txt', 'w')

        for elemento in self.cabecalhoMatProbFlor:
            vitoria.write(str(elemento) + " ")
            derrota.write(str(elemento) + " ")

        vitoria.write("\n")
        derrota.write("\n")

        for linha in self.matrizFlorVitoria:
            for coluna in linha:
                vitoria.write(str(round(coluna)) + " ")
            vitoria.write("\n")

        for linha in self.matrizFlorDerrota:
            for coluna in linha:
                derrota.write(str(round(coluna)) + " ")
            derrota.write("\n")

        vitoria.close()
        derrota.close()

    # flor
    def calculaFlor(self):
        pontosRobo = self.trucoDescription['pontosFlorRobo']
        pontosHumano = self.trucoDescription['pontosFlorHumano']

        if pontosRobo < 20 or pontosHumano < 20:
            return

        combRobo = self.defineCombFlor()
        combHumano = []
        diferenca = round(self.maxFlor * self.porcentagemDif)

        if self.trucoDescription['primeiraCartaHumano'] is None or self.trucoDescription['segundaCartaHumano'] is None or self.trucoDescription['terceiraCartaHumano'] is None:
            combHumano = self.definePossiveisCombFlor(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, None)
        elif self.trucoDescription['primeiraCartaHumano'] is 0 or self.trucoDescription['segundaCartaHumano'] is 0 or self.trucoDescription['terceiraCartaHumano'] is 0:
            combHumano = self.definePossiveisCombFlor(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, 0)
        else:
            combHumano = self.definePossiveisCombFlor(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, 0)

        if len(combHumano) > 1:
            diferenca = round(diferenca / len(combHumano))

        if self.ganhouContraFlor == 1:
            for comb in combHumano:
                self.matrizFlorVitoria[self.cabecalhoMatProbFlor.index(combRobo)][self.cabecalhoMatProbFlor.index(comb)] += diferenca
                self.matrizFlorDerrota[self.cabecalhoMatProbFlor.index(comb)][self.cabecalhoMatProbFlor.index(combRobo)] += diferenca
        else:
            for comb in combHumano:
                self.matrizFlorVitoria[self.cabecalhoMatProbFlor.index(comb)][self.cabecalhoMatProbFlor.index(combRobo)] += diferenca
                self.matrizFlorDerrota[self.cabecalhoMatProbFlor.index(combRobo)][self.cabecalhoMatProbFlor.index(comb)] += diferenca

    # flor
    def defineCombFlor(self):
        carta1 = self.ordem[self.codificacao.index(self.trucoDescription['cartaBaixaRobo'])]
        carta2 = self.ordem[self.codificacao.index(self.trucoDescription['cartaMediaRobo'])]
        carta3 = self.ordem[self.codificacao.index(self.trucoDescription['cartaAltaRobo'])]

        naipes = ["o", "e", "p"]

        if carta1[-1] in naipes: carta1 = int(carta1[:-1])
        if int(carta1) >= 10:
            carta1 = 0
        else:
            carta1 = int(carta1)

        if carta2[-1] in naipes: carta2 = int(carta2[:-1])
        if int(carta2) >= 10:
            carta2 = 0
        else:
            carta2 = int(carta2)

        if carta3[-1] in naipes: carta3 = int(carta3[:-1])
        if int(carta3) >= 10:
            carta3 = 0
        else:
            carta3 = int(carta3)

        return self.arrumaCombinacaoFlor(carta1, carta2, carta3)

    # flor
    def avaliaCartaFlor(self, valorCarta):
        if valorCarta >= 10: return 0
        else:                return valorCarta

    # flor
    def arrumaCombinacaoFlor(self, carta1, carta2, carta3):
        if carta1 <= carta2 <= carta3:
            return str(carta1) + str(carta2) + str(carta3)
        elif carta1 <= carta3 <= carta2:
            return str(carta1) + str(carta3) + str(carta2)
        elif carta2 <= carta1 <= carta3:
            return str(carta2) + str(carta1) + str(carta3)
        elif carta2 <= carta3 <= carta1:
            return str(carta2) + str(carta3) + str(carta1)
        elif carta3 <= carta1 <= carta2:
            return str(carta3) + str(carta1) + str(carta2)
        elif carta3 <= carta2 <= carta1:
            return str(carta3) + str(carta2) + str(carta1)

    # flor
    def definePossiveisCombFlor(self, primeiraCarta, segundaCarta, terceiraCarta, pontosHumano, qual):
        possiveisCombFlor = []

        if primeiraCarta != qual and segundaCarta == qual and terceiraCarta == qual:
            primeiraCarta = self.ordem[self.codificacao.index(primeiraCarta)]
            naipes = ["o", "e", "p"]

            if primeiraCarta[-1] in naipes: primeiraCarta = int(primeiraCarta[:-1])
            if int(primeiraCarta) >= 10: primeiraCarta = 0
            else: primeiraCarta = int(primeiraCarta)

            for numeroUmComb in range(0, 8):
                for numeroDoisComb in range(numeroUmComb, 8):
                    if (numeroUmComb != numeroDoisComb) and (numeroDoisComb != primeiraCarta) and (numeroUmComb != primeiraCarta):
                        if numeroUmComb + numeroDoisComb + primeiraCarta + 20 == pontosHumano:
                             possiveisCombFlor.append(self.arrumaCombinacaoFlor(numeroUmComb, numeroDoisComb, primeiraCarta))
                    elif primeiraCarta == 0 and (numeroUmComb == 0 or numeroDoisComb == 0):
                        if numeroUmComb + numeroDoisComb + primeiraCarta + 20 == pontosHumano:
                            possiveisCombFlor.append(self.arrumaCombinacaoFlor(numeroUmComb, numeroDoisComb, primeiraCarta))
        elif primeiraCarta != qual and segundaCarta != qual and terceiraCarta == qual:
            primeiraCarta = self.ordem[self.codificacao.index(primeiraCarta)]
            segundaCarta = self.ordem[self.codificacao.index(segundaCarta)]
            naipes = ["o", "e", "p"]

            if primeiraCarta[-1] in naipes: primeiraCarta = int(primeiraCarta[:-1])
            if int(primeiraCarta) >= 10: primeiraCarta = 0
            else: primeiraCarta = int(primeiraCarta)

            if segundaCarta[-1] in naipes: segundaCarta = int(segundaCarta[:-1])
            if int(segundaCarta) >= 10: segundaCarta = 0
            else: segundaCarta = int(segundaCarta)

            for numeroUmComb in range(0, 8):
                if (numeroUmComb != primeiraCarta) and (numeroUmComb != segundaCarta):
                    if numeroUmComb + primeiraCarta + segundaCarta + 20 == pontosHumano:
                        possiveisCombFlor.append(self.arrumaCombinacaoFlor(numeroUmComb, primeiraCarta, segundaCarta))
                elif primeiraCarta == 0 and segundaCarta == 0 and numeroUmComb == 0:
                    if numeroUmComb + primeiraCarta + segundaCarta + 20 == pontosHumano:
                        possiveisCombFlor.append(self.arrumaCombinacaoFlor(numeroUmComb, primeiraCarta, segundaCarta))
        elif primeiraCarta != qual and segundaCarta != qual and terceiraCarta != qual:
            primeiraCarta = self.ordem[self.codificacao.index(primeiraCarta)]
            segundaCarta = self.ordem[self.codificacao.index(segundaCarta)]
            terceiraCarta = self.ordem[self.codificacao.index(terceiraCarta)]
            naipes = ["o", "e", "p"]

            if primeiraCarta[-1] in naipes: primeiraCarta = int(primeiraCarta[:-1])
            if int(primeiraCarta) >= 10:
                primeiraCarta = 0
            else:
                primeiraCarta = int(primeiraCarta)

            if segundaCarta[-1] in naipes: segundaCarta = int(segundaCarta[:-1])
            if int(segundaCarta) >= 10:
                segundaCarta = 0
            else:
                segundaCarta = int(segundaCarta)

            if terceiraCarta[-1] in naipes: terceiraCarta = int(terceiraCarta[:-1])
            if int(terceiraCarta) >= 10:
                terceiraCarta = 0
            else:
                terceiraCarta = int(terceiraCarta)

            possiveisCombFlor.append(self.arrumaCombinacaoFlor(primeiraCarta, segundaCarta, terceiraCarta))

        possiveisCombFlor = set(possiveisCombFlor).copy()

        return possiveisCombFlor

    # envido
    def extraindoMatrizesEnvido(self):
        vitoria   = open(self.pasta + 'matrizEnvidoVitoria.txt', 'r')
        derrota   = open(self.pasta + 'matrizEnvidoDerrota.txt', 'r')
        matrizVit = []
        matrizDer = []
        self.cabecalhoMatProbEnvido = vitoria.readline().split()
        cabecalho = derrota.readline()

        linhasVit = vitoria.readlines()
        linhasDer = derrota.readlines()

        for i in range(len(linhasVit)):
            matrizVit.append(linhasVit[i].split())

        for i in range(len(linhasDer)):
            matrizDer.append(linhasDer[i].split())

        for linha in range(len(matrizVit)):
            for coluna in range(len(matrizVit[linha])):
                matrizVit[linha][coluna] = int(matrizVit[linha][coluna])
                matrizDer[linha][coluna] = int(matrizDer[linha][coluna])

        self.matrizEnvidoVitoria = matrizVit
        self.matrizEnvidoDerrota = matrizDer

        vitoria.close()
        derrota.close()

    # envido
    def escrevendoMatrizesEnvido(self):
        shutil.move(self.pasta + 'matrizEnvidoVitoria.txt', self.pasta + 'antigos/' + 'matrizEnvidoVitoria.txt')
        shutil.move(self.pasta + 'matrizEnvidoDerrota.txt', self.pasta + 'antigos/' + 'matrizEnvidoDerrota.txt')

        vitoria = open(self.pasta + 'matrizEnvidoVitoria.txt', 'w')
        derrota = open(self.pasta + 'matrizEnvidoDerrota.txt', 'w')

        for elemento in self.cabecalhoMatProbEnvido:
            vitoria.write(str(elemento) + " ")
            derrota.write(str(elemento) + " ")

        vitoria.write("\n")
        derrota.write("\n")

        for linha in self.matrizEnvidoVitoria:
            for coluna in linha:
                vitoria.write(str(round(coluna)) + " ")
            vitoria.write("\n")

        for linha in self.matrizEnvidoDerrota:
            for coluna in linha:
                derrota.write(str(round(coluna)) + " ")
            derrota.write("\n")

        vitoria.close()
        derrota.close()

    # envido
    def calculaEnvido(self):
        pontosRobo = self.trucoDescription['pontosEnvidoRobo']
        pontosHumano = self.trucoDescription['pontosEnvidoHumano']

        if pontosRobo < 20 or pontosHumano < 20:
            return

        combRobo = self.defineCombEnvido(pontosRobo)
        combHumano = []
        diferenca = round(self.maxEnvido * self.porcentagemDif)
        if self.trucoDescription['primeiraCartaHumano'] is None or self.trucoDescription['segundaCartaHumano'] is None or self.trucoDescription['terceiraCartaHumano'] is None:
            combHumano = self.definePossiveisCombEnvido(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, None)
        elif self.trucoDescription['primeiraCartaHumano'] is 0 or self.trucoDescription['segundaCartaHumano'] is 0 or self.trucoDescription['terceiraCartaHumano'] is 0:
            combHumano = self.definePossiveisCombEnvido(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, 0)
        else:
            combHumano = self.definePossiveisCombEnvido(self.trucoDescription['primeiraCartaHumano'], self.trucoDescription['segundaCartaHumano'], self.trucoDescription['terceiraCartaHumano'], pontosHumano, 0)

        if len(combHumano) > 1:
            diferenca = round(diferenca / len(combHumano))

        if self.ganhouEnvido == 1:
            self.file.write("ganhou envido na partida " + self.trucoDescription['idPartida'] + "\n")
            for comb in combHumano:
                self.matrizEnvidoVitoria[self.cabecalhoMatProbEnvido.index(combRobo)][self.cabecalhoMatProbEnvido.index(comb)] += diferenca
                self.matrizEnvidoDerrota[self.cabecalhoMatProbEnvido.index(comb)][self.cabecalhoMatProbEnvido.index(combRobo)] += diferenca
        else:
            self.file.write("perdeu envido na partida " + self.trucoDescription['idPartida'] + "\n")
            for comb in combHumano:
                self.matrizEnvidoVitoria[self.cabecalhoMatProbEnvido.index(comb)][self.cabecalhoMatProbEnvido.index(combRobo)] += diferenca
                self.matrizEnvidoDerrota[self.cabecalhoMatProbEnvido.index(combRobo)][self.cabecalhoMatProbEnvido.index(comb)] += diferenca

    # envido
    def achaCartasEnvido(self, primeiraCarta, segundaCarta, terceiraCarta, pontosEnvido):
        carta1 = 0
        carta2 = 0

        cartaBaixa = self.ordem[self.codificacao.index(primeiraCarta)]
        cartaMedia = self.ordem[self.codificacao.index(segundaCarta)]
        cartaAlta = self.ordem[self.codificacao.index(terceiraCarta)]

        naipes = ["o", "e", "p"]

        if cartaBaixa[-1] in naipes: cartaBaixa = int(cartaBaixa[:-1])
        if int(cartaBaixa) >= 10: cartaBaixa = 0
        else: cartaBaixa = int(cartaBaixa)

        if cartaMedia[-1] in naipes: cartaMedia = int(cartaMedia[:-1])
        if int(cartaMedia) >= 10: cartaMedia = 0
        else: cartaMedia = int(cartaMedia)

        if cartaAlta[-1] in naipes: cartaAlta = int(cartaAlta[:-1])
        if int(cartaAlta) >= 10: cartaAlta = 0
        else: cartaAlta = int(cartaAlta)

        if cartaBaixa + cartaMedia + 20 == pontosEnvido:
            carta1 = cartaBaixa
            carta2 = cartaMedia
        elif cartaBaixa + cartaAlta + 20 == pontosEnvido:
            carta1 = cartaBaixa
            carta2 = cartaAlta
        elif cartaMedia + cartaAlta + 20 == pontosEnvido:
            carta1 = cartaMedia
            carta2 = cartaAlta

        return carta1, carta2

    # envido
    def defineCombEnvido(self, pontosRobo):
        carta1, carta2 = self.achaCartasEnvido(self.trucoDescription['cartaBaixaRobo'], self.trucoDescription['cartaMediaRobo'], self.trucoDescription['cartaAltaRobo'], pontosRobo)

        carta1 = self.avaliaCartaEnvido(carta1)
        carta2 = self.avaliaCartaEnvido(carta2)

        return self.arrumaCombinacaoEnvido(carta1, carta2)

    # envido
    def arrumaCombinacaoEnvido(self, carta1, carta2):
        if carta1 > carta2:
            return str(carta2) + str(carta1)
        elif carta1 <= carta2:
            return str(carta1) + str(carta2)

    # envido
    def avaliaCartaEnvido(self, valorCarta):
        if valorCarta >= 10: return 0
        else:                return valorCarta

    # envido
    def auxArrumaCartasParaPossiveisCombHumano(self, primeiraCarta, segundaCarta, terceiraCarta, qual):
        carta1 = -1
        carta2 = -1
        carta3 = -1

        if primeiraCarta != qual: carta1 = self.ordem[self.codificacao.index(primeiraCarta)]
        if segundaCarta != qual: carta2 = self.ordem[self.codificacao.index(segundaCarta)]
        if terceiraCarta != qual: carta3 = self.ordem[self.codificacao.index(terceiraCarta)]

        naipes = ["o", "e", "p"]

        if carta1 != -1:
            if carta1[-1] in naipes: carta1 = int(carta1[:-1])
        if int(carta1) >= 10: carta1 = 0
        else: carta1 = int(carta1)

        if carta2 != -1:
            if carta2[-1] in naipes: carta2 = int(carta2[:-1])
        if int(carta2) >= 10: carta2 = 0
        else: carta2 = int(carta2)

        if carta3 != -1:
            if carta3[-1] in naipes: carta3 = int(carta3[:-1])
        if int(carta3) >= 10: carta3 = 0
        else: carta3 = int(carta3)

        return carta1, carta2, carta3

    # envido
    def auxQuandoTemUmaCartaEnvido(self, carta1, pontosHumano):
        possiveisCombEnvido = []

        for carta2 in range(0, 8):
            if carta2 != carta1 and carta1 + carta2 + 20 == pontosHumano:
                possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1, carta2))
            elif carta1 == 0 and carta2 == 0 and carta1 + carta2 + 20 == pontosHumano:
                possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1, carta2))

        return possiveisCombEnvido

    # envido
    def definePossiveisCombEnvido(self, primeiraCarta, segundaCarta, terceiraCarta, pontosHumano, qual):
        possiveisCombEnvido = []

        carta1, carta2, carta3 = self.auxArrumaCartasParaPossiveisCombHumano(primeiraCarta, segundaCarta, terceiraCarta, qual)

        carta1Envido = 0
        carta2Envido = 0

        if carta1 != -1 and carta2 != -1 and carta3 != -1:
            if carta1 + carta2 + 20 == pontosHumano:
                carta1Envido = carta1
                carta2Envido = carta2
            elif carta1 + carta3 + 20 == pontosHumano:
                carta1Envido = carta1
                carta2Envido = carta3
            elif carta2 + carta3 + 20 == pontosHumano:
                carta1Envido = carta2
                carta2Envido = carta3
            possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1Envido, carta2Envido))

        elif carta1 == -1 and carta2 == -1 and carta3 == -1:
            for carta1Envido in range(0, 8):
                for carta2Envido in range(carta1Envido, 8):
                    if (carta1Envido != carta2Envido) and carta1Envido + carta2Envido + 20 == pontosHumano:
                        possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1Envido, carta2Envido))
                    elif carta1Envido == 0 and carta2Envido == 0 and carta1Envido + carta2Envido + 20 == pontosHumano:
                            possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1Envido, carta2Envido))

        elif carta1 != -1 and carta2 == -1 and carta3 == -1:
            possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta1, pontosHumano)
        elif carta1 == -1 and carta2 != -1 and carta3 == -1:
            possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta2, pontosHumano)
        elif carta1 == -1 and carta2 == -1 and carta3 != -1:
            possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta3, pontosHumano)

        elif carta1 != -1 and carta2 != -1 and carta3 == -1:
            if carta1 + carta2 + 20 == pontosHumano:
                possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1, carta2))
            else:
                possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta1, pontosHumano) + self.auxQuandoTemUmaCartaEnvido(carta2, pontosHumano)
        elif carta1 != -1 and carta2 == -1 and carta3 != -1:
            if carta1 + carta2 + 20 == pontosHumano:
                possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta1, carta3))
            else:
                possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta1, pontosHumano) + self.auxQuandoTemUmaCartaEnvido(carta3, pontosHumano)
        elif carta1 == -1 and carta2 != -1 and carta3 != -1:
            if carta1 + carta2 + 20 == pontosHumano:
                possiveisCombEnvido.append(self.arrumaCombinacaoEnvido(carta2, carta3))
            else:
                possiveisCombEnvido = self.auxQuandoTemUmaCartaEnvido(carta2, pontosHumano) + self.auxQuandoTemUmaCartaEnvido(carta3, pontosHumano)

        return possiveisCombEnvido

if __name__ == "__main__":
    r = Resultado()
    r.main()
