import json as js
import sys
import random as rd


class ContraFlor:
    def __init__(self):
        self.pontosFlor = 0             # meus pontos de flor
        self.combinacaoFlor = None      # minha combinação de flor
        self.possiveisCombFlor = []   # possiveis combinações de flor do adversario
        self.ordem = []                 # ordem das cartas (menor para maior)
        self.codificacao = []           # codificação das cartas

        self.trucoDescription = {}      # classe trucoDescription
        self.pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/"

        self.probLimiteGanhoFlor = 0    # probabilidade minima de ganho do flor

        self.cabecalhoMatProbFlor = []  # cabeçalho das matrizes de markov
        self.matrizFlorVitoria = [[]]   # matriz de probabilidades de vitoria
        self.matrizFlorDerrota = [[]]   # matriz de probabilidades de derrota

    def main(self):
        """
        Método inicial que é chamado de fora da classe e executa as operações
        """
        self.trucoDescription = js.load(open(self.pasta + 'trucoDescription.json', 'r'))
        self.probLimiteGanhoFlor = float(sys.argv[2])
        self.pontosFlor = self.trucoDescription['pontosFlorRobo']
        self.ordem = ["4", "5", "6", "7", "10", "11", "12", "1", "2", "3", "7o", "7e", "1p", "1e"]
        self.codificacao = [1, 2, 3, 4, 6, 7, 8, 12, 16, 24, 40, 42, 50, 52]

        self.extraindoMatrizes()
        self.defineCombFlor()
        self.chamaContraFlor()

    def extraindoMatrizes(self):
        """
        Método que extrai dos arquivos as matrizes de vitória e derrota e coloca nas variáveis da classe
        """
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

        self.matrizFlorVitoria = matrizVit
        self.matrizFlorDerrota = matrizDer

        vitoria.close()
        derrota.close()

    def definePossiveisCombFlor(self, primeiraCarta):
        """
        Método que encontra as possíveis combinações de cartas/pontos do adversário
        :param primeiraCarta: primeira carta do humano, a partir dela são encontradas as combinações
        """
        if primeiraCarta is not None:
            primeiraCarta = self.ordem[self.codificacao.index(primeiraCarta)]
            naipes = ["o", "e", "p"]

            if primeiraCarta[-1] in naipes: primeiraCarta = int(primeiraCarta[:-1])
            if int(primeiraCarta) >= 10: primeiraCarta = 0
            else: primeiraCarta = int(primeiraCarta)

            for numeroUmComb in range(0, 8):
                for numeroDoisComb in range(numeroUmComb, 8):
                    if (numeroUmComb != numeroDoisComb) and (numeroDoisComb != primeiraCarta) and (numeroUmComb != primeiraCarta):
                        self.possiveisCombFlor.append(self.arrumaCombinacao(numeroUmComb, numeroDoisComb, primeiraCarta))
                    elif primeiraCarta == 0 or numeroUmComb == 0 or numeroDoisComb == 0:
                        self.possiveisCombFlor.append(self.arrumaCombinacao(numeroUmComb, numeroDoisComb, primeiraCarta))

            self.possiveisCombFlor = set(self.possiveisCombFlor).copy()
        elif primeiraCarta is None:
            self.possiveisCombFlor = self.cabecalhoMatProbFlor.copy()

    def defineCombFlor(self):
        carta1 = self.ordem[self.codificacao.index(self.trucoDescription['cartaBaixaRobo'])]
        carta2 = self.ordem[self.codificacao.index(self.trucoDescription['cartaMediaRobo'])]
        carta3 = self.ordem[self.codificacao.index(self.trucoDescription['cartaAltaRobo'])]

        naipes = ["o", "e", "p"]

        if carta1[-1] in naipes: carta1 = int(carta1[:-1])
        if int(carta1) >= 10: carta1 = 0
        else: carta1 = int(carta1)

        if carta2[-1] in naipes: carta2 = int(carta2[:-1])
        if int(carta2) >= 10: carta2 = 0
        else: carta2 = int(carta2)

        if carta3[-1] in naipes: carta3 = int(carta3[:-1])
        if int(carta3) >= 10: carta3 = 0
        else: carta3 = int(carta3)

        self.combinacaoFlor = self.arrumaCombinacao(carta1, carta2, carta3)

    def avaliaCarta(self, valorCarta):
        """
        Método que avalia o valor da carta
        :param valorCarta: número da carta
        :return: valor de carta, se for menor do que 10, e 0 se for igual ou maior do que 10
        """
        if valorCarta >= 10: return 0
        else:                return valorCarta

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

    def markovFlor(self):
        """
        Método que executa todas as operações
        :return: falso se não tem pontos de flor, se não alcançou o mínimo ou se os calculos
                 não forem positivos para a questão, e true se os resultados derem positivo.
        """
        if self.pontosFlor < 20: return False

        primeiraCarta = self.trucoDescription['primeiraCartaHumano']

        self.definePossiveisCombFlor(primeiraCarta)

        ganhosPossiveisFlor = 0
        perdasPossiveisFlor = 0
        listaVitoriaDerrota = []

        # contabiliza derrotas e vitorias
        for comb in self.possiveisCombFlor:
            ganhosPossiveisFlor += int(self.matrizFlorVitoria[self.cabecalhoMatProbFlor.index(self.combinacaoFlor)][self.cabecalhoMatProbFlor.index(comb)])
            perdasPossiveisFlor += int(self.matrizFlorDerrota[self.cabecalhoMatProbFlor.index(self.combinacaoFlor)][self.cabecalhoMatProbFlor.index(comb)])

        if ganhosPossiveisFlor == 0 and perdasPossiveisFlor == 0:
            ganhosPossiveisFlor = 1
            perdasPossiveisFlor = 1

        # calcula porcentagem
        porcentagemGanhos = ganhosPossiveisFlor / (ganhosPossiveisFlor + perdasPossiveisFlor)
        porcentagemPerdas = perdasPossiveisFlor / (ganhosPossiveisFlor + perdasPossiveisFlor)

        porcentagemGanhos = round(porcentagemGanhos, 1)
        porcentagemPerdas = round(porcentagemPerdas, 1)

        if self.probLimiteGanhoFlor < porcentagemGanhos < self.probLimiteGanhoFlor + 0.2:
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

    def chamaContraFlor(self):
        """
        Método que verifica o resultado das operações. Só esse método pode usar a função print()
        """
        if self.markovFlor():
            print("true")
        else:
            print("false")

if __name__ == "__main__":
    f = ContraFlor()
    f.main()
