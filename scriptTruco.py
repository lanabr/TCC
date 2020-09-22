import json as js
import sys
import random as rd


class Truco:
    def __init__(self):
        self.combCartasTruco = 0           # combinação das minhas cartas

        self.possiveisCombTruco = []       # possiveis combinações de cartas do adversário

        self.trucoDescription = {}         # classe trucoDescription
        self.rodada           = 0          # rodada atual
        self.pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/"

        self.probLimiteGanhoTruco = 0      # probabilidade minima de ganho do truco

        self.ordem       = []              # ordem das cartas (menor para maior)
        self.codificacao = []              # codificação das cartas

        self.cabecalhoMatProbTruco = []    # cabeçalho das matrizes de markov
        self.matrizTrucoVitoria    = [[]]  # matriz de probabilidades de vitoria
        self.matrizTrucoDerrota    = [[]]  # matriz de probabilidades de derrota

    def main(self):
        """
        Método inicial que é chamado de fora da classe e executa as operações
        """
        self.trucoDescription = js.load(open(self.pasta + 'trucoDescription.json', 'r'))
        self.rodada = int(sys.argv[1])
        self.probLimiteGanhoTruco = float(sys.argv[2])
        self.codificacao = [1, 2, 3, 4, 6, 7, 8, 12, 16, 24, 40, 42, 50, 52]

        self.extraindoMatrizes()
        self.defineCombTruco()
        self.chamaTruco()

    def extraindoMatrizes(self):
        """
        Método que extrai dos arquivos as matrizes de vitória e derrota e coloca nas variáveis da classe
        """
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

        self.matrizTrucoVitoria = matrizVit
        self.matrizTrucoDerrota = matrizDer

        vitoria.close()
        derrota.close()

    def definePossiveisCombTruco(self):
        """
        Método que verifica as cartas já jogadas pelo oponente e a partir delas gera as combinações.
        """
        primeiraCartaHumano = self.trucoDescription['primeiraCartaHumano']
        segundaCartaHumano = self.trucoDescription['segundaCartaHumano']
        terceiraCartaHumano = self.trucoDescription['terceiraCartaHumano']

        if primeiraCartaHumano is None and segundaCartaHumano is None and terceiraCartaHumano is None:
            self.possiveisCombTruco = self.cabecalhoMatProbTruco.copy()
        elif primeiraCartaHumano is not None and segundaCartaHumano is None and terceiraCartaHumano is None:
            for segundaCarta in range(0, len(self.codificacao)):
                for terceiraCarta in range(segundaCarta, len(self.codificacao)):
                    if self.validadeComb(primeiraCartaHumano, self.codificacao[segundaCarta], self.codificacao[terceiraCarta]):
                        self.possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, self.codificacao[segundaCarta], self.codificacao[terceiraCarta]))
        elif primeiraCartaHumano is not None and segundaCartaHumano is not None and terceiraCartaHumano is None:
            for terceiraCarta in range(0, len(self.codificacao)):
                if self.validadeComb(primeiraCartaHumano, segundaCartaHumano, self.codificacao[terceiraCarta]):
                    self.possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, segundaCartaHumano, self.codificacao[terceiraCarta]))
        elif primeiraCartaHumano is not None and segundaCartaHumano is not None and terceiraCartaHumano is not None:
            self.possiveisCombTruco.append(self.arrumaCombinacao(primeiraCartaHumano, segundaCartaHumano, terceiraCartaHumano))

    def analisaMinhaCombTruco(self):
        """
        Método que verifica se eu tenho as 4 cartas diferentes na minha combinação. Se eu tenho, remove
        as possíveis combinações do oponente que tem a carta que eu tenho
        """
        if "40" in self.combCartasTruco:
            self.removeMinhaCombTruco("40")
        if "42" in self.combCartasTruco:
            self.removeMinhaCombTruco("42")
        if "50" in self.combCartasTruco:
            self.removeMinhaCombTruco("50")
        if "52" in self.combCartasTruco:
            self.removeMinhaCombTruco("52")

    def removeMinhaCombTruco(self, carta):
        """
        Método que remove da lista de possíveis combinações todas as que tiverem a carta recebida.
        :param carta: carta para fazer a remoção.
        """
        for combinacao in self.possiveisCombTruco:
            if carta in combinacao:
                self.possiveisCombTruco.remove(combinacao)

    def defineCombTruco(self):
        """
        Método que define a variável de combinação da classe.
        """
        primeiraCarta = self.trucoDescription['cartaBaixaRobo']
        segundaCarta  = self.trucoDescription['cartaMediaRobo']
        terceiraCarta = self.trucoDescription['cartaAltaRobo']

        self.combCartasTruco = self.arrumaCombinacao(primeiraCarta, segundaCarta, terceiraCarta)

    def arrumaCombinacao(self, carta1, carta2, carta3):
        """
        Método que arruma a combinação de acordo com a ordem das cartas
        :param carta1: primeira carta
        :param carta2: segunda carta
        :param carta3: terceira carta
        :return: combinação na ordem certa
        """

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

    def validadeComb(self, carta1, carta2, carta3):
        """
        Método que analisa a validade da combinação.
        :param carta1: primeira carta
        :param carta2: segunda carta
        :param carta3: terceira carta
        :return: True se é válida, False se não é válida.
        """
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

    def markovTruco(self):
        """
        Método que executa todas as operações
        :return: falso se não tem pontos de truco, se não alcançou o mínimo ou se os calculos
                 não forem positivos para a questão, e true se os resultados derem positivo.
        """

        if self.trucoDescription['ganhadorPrimeiraRodada'] == 2 and self.trucoDescription['ganhadorSegundaRodada'] == 2:
            return False
        elif self.trucoDescription['ganhadorPrimeiraRodada'] == 0 and self.trucoDescription['ganhadorSegundaRodada'] == 2:
            return False
        elif self.trucoDescription['ganhadorPrimeiraRodada'] == 2 and self.trucoDescription['ganhadorSegundaRodada'] == 0:
            return False

        self.definePossiveisCombTruco()
        self.analisaMinhaCombTruco()

        ganhosPossiveisTruco = 0
        perdasPossiveisTruco = 0
        listaVitoriaDerrota  = []

        # contabiliza derrotas e vitorias
        for comb in self.possiveisCombTruco:
            ganhosPossiveisTruco += int(self.matrizTrucoVitoria[self.cabecalhoMatProbTruco.index(self.combCartasTruco)][self.cabecalhoMatProbTruco.index(comb)])
            perdasPossiveisTruco += int(self.matrizTrucoDerrota[self.cabecalhoMatProbTruco.index(self.combCartasTruco)][self.cabecalhoMatProbTruco.index(comb)])

        if ganhosPossiveisTruco == 0 and perdasPossiveisTruco == 0:
            ganhosPossiveisTruco = 1
            perdasPossiveisTruco = 1

        # calcula porcentagem
        porcentagemGanhos = ganhosPossiveisTruco / (ganhosPossiveisTruco + perdasPossiveisTruco)
        porcentagemPerdas = perdasPossiveisTruco / (ganhosPossiveisTruco + perdasPossiveisTruco)

        porcentagemGanhos = round(porcentagemGanhos, 1)
        porcentagemPerdas = round(porcentagemPerdas, 1)

        if self.probLimiteGanhoTruco < porcentagemGanhos:
            pass
        else:
            return False

        # insere na lista para randomizar
        for i in range(int(porcentagemGanhos * 10)):
            listaVitoriaDerrota.append("G")

        for i in range(int(porcentagemPerdas * 10)):
            listaVitoriaDerrota.append("P")

        # escolhe randomico da lista
        escolheJogo = rd.choice(listaVitoriaDerrota)

        # se escolheu G retorna true, se não false
        if escolheJogo == "G":
            return True
        else:
            return False

    def chamaTruco(self):
        if self.markovTruco(): print("true")
        else:                  print("false")

if __name__ == "__main__":
    t = Truco()
    t.main()