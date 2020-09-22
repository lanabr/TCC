import json as js
import sys
import random as rd
import math


class Envido:
    def __init__(self):
        self.pontosEnvido          = 0      # meus pontos de envido
        self.combinacaoEnvido      = None   # minha combinação de envido
        self.possiveisCombEnvido   = []     # possiveis combinações de envido do adversario

        self.ordem                 = []     # ordem das cartas (menor para maior)
        self.codificacao           = []     # codificação das cartas

        self.trucoDescription = {}          # classe trucoDescription
        self.pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/"

        self.probLimiteGanhoEnvido = 0      # probabilidade minima de ganho do envido

        self.cabecalhoMatProbEnvido = []    # cabeçalho das matrizes de markov
        self.matrizEnvidoVitoria    = [[]]  # matriz de probabilidades de vitoria
        self.matrizEnvidoDerrota    = [[]]  # matriz de probabilidades de derrota

    def main(self):
        """
        Método inicial que é chamado de fora da classe e executa as operações
        """
        self.trucoDescription = js.load(open(self.pasta + 'trucoDescription.json', 'r'))
        self.probLimiteGanhoEnvido = float(sys.argv[2])
        self.pontosEnvido = self.trucoDescription['pontosEnvidoRobo']
        self.ordem = ["4", "5", "6", "7", "10", "11", "12", "1", "2", "3", "7o", "7e", "1p", "1e"]
        self.codificacao = [1, 2, 3, 4, 6, 7, 8, 12, 16, 24, 40, 42, 50, 52]

        self.extraindoMatrizes()
        self.defineMinhaCombEnvido()
        self.chamaEnvido()

    def extraindoMatrizes(self):
        """
        Método que extrai dos arquivos as matrizes de vitória e derrota e coloca nas variáveis da classe
        """
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

        self.matrizEnvidoVitoria = matrizVit
        self.matrizEnvidoDerrota = matrizDer

        vitoria.close()
        derrota.close()

    def definePossiveisCombEnvido(self, primeiraCarta):
        """
        Método que encontra as possíveis combinações de cartas/pontos do adversário
        :param primeiraCarta: primeira carta do humano, a partir dela são encontradas as combinações
        """
        if primeiraCarta is not None:
            for numeroComb in range(0, 8):
                if numeroComb != primeiraCarta:
                    self.possiveisCombEnvido.append(self.arrumaCombinacao(primeiraCarta, numeroComb))
                if numeroComb == 0 and primeiraCarta == 0:
                    self.possiveisCombEnvido.append(self.arrumaCombinacao(primeiraCarta, numeroComb))

        elif primeiraCarta is None:
            self.possiveisCombEnvido = self.cabecalhoMatProbEnvido.copy()

    def ajustaPrimeiraCartaHumano(self, primeiraCarta):
        """
        Método que
        :param primeiraCarta:
        :return:
        """
        if primeiraCarta is not None:
            primeiraCarta = self.ordem[self.codificacao.index(primeiraCarta)]
            naipes = ["o", "e", "p"]

            if primeiraCarta[-1] in naipes: primeiraCarta = int(primeiraCarta[:-1])
            if int(primeiraCarta) >= 10: primeiraCarta = 0
            else: primeiraCarta = int(primeiraCarta)

            return primeiraCarta

    def defineMinhaCombEnvido(self):
        """
        Método que analisa quais cartas tem naipes iguais e define pontos e combinação dessas cartas.
        """
        carta1 = 0
        carta2 = 0

        cartaBaixa = self.ordem[self.codificacao.index(self.trucoDescription['cartaBaixaRobo'])]
        cartaMedia = self.ordem[self.codificacao.index(self.trucoDescription['cartaMediaRobo'])]
        cartaAlta = self.ordem[self.codificacao.index(self.trucoDescription['cartaAltaRobo'])]

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

        if cartaBaixa + cartaMedia + 20 == self.pontosEnvido:
            carta1 = cartaBaixa
            carta2 = cartaMedia
        elif cartaBaixa + cartaAlta + 20 == self.pontosEnvido:
            carta1 = cartaBaixa
            carta2 = cartaAlta
        elif cartaMedia + cartaAlta + 20 == self.pontosEnvido:
            carta1 = cartaMedia
            carta2 = cartaAlta

        carta1 = self.avaliaCarta(carta1)
        carta2 = self.avaliaCarta(carta2)

        self.combinacaoEnvido = self.arrumaCombinacao(carta1, carta2)

    def arrumaCombinacao(self, carta1, carta2):
        """
        Método que arruma a combinação de acordo com a ordem das cartas
        :param carta1: primeira carta
        :param carta2: segunda carta
        :return: combinação na ordem certa
        """
        if carta1 > carta2:
            return str(carta2) + str(carta1)
        elif carta1 <= carta2:
            return str(carta1) + str(carta2)

    def avaliaCarta(self, valorCarta):
        """
        Método que avalia o valor da carta
        :param valorCarta: número da carta
        :return: valor de carta, se for menor do que 10, e 0 se for igual ou maior do que 10
        """
        if valorCarta >= 10: return 0
        else:                return valorCarta

    def markovEnvido(self):
        """
        Método que executa todas as operações
        :return: falso se não tem pontos de envido, se não alcançou o mínimo ou se os calculos
                 não forem positivos para a questão, e true se os resultados derem positivo.
        """
        if self.pontosEnvido < 20: return False

        primeiraCarta = self.ajustaPrimeiraCartaHumano(self.trucoDescription['primeiraCartaHumano'])

        self.definePossiveisCombEnvido(primeiraCarta)

        ganhosPossiveisEnvido = 0
        perdasPossiveisEnvido = 0
        listaVitoriaDerrota   = []

        # contabiliza derrotas e vitorias
        for comb in self.possiveisCombEnvido:
            ganhosPossiveisEnvido += int(self.matrizEnvidoVitoria[self.cabecalhoMatProbEnvido.index(self.combinacaoEnvido)][self.cabecalhoMatProbEnvido.index(comb)])
            perdasPossiveisEnvido += int(self.matrizEnvidoDerrota[self.cabecalhoMatProbEnvido.index(self.combinacaoEnvido)][self.cabecalhoMatProbEnvido.index(comb)])

        if ganhosPossiveisEnvido == 0 and perdasPossiveisEnvido == 0:
            ganhosPossiveisEnvido = 1
            perdasPossiveisEnvido = 1

        # calcula porcentagem
        porcentagemGanhos = ganhosPossiveisEnvido / (ganhosPossiveisEnvido + perdasPossiveisEnvido)
        porcentagemPerdas = perdasPossiveisEnvido / (ganhosPossiveisEnvido + perdasPossiveisEnvido)

        porcentagemGanhos = round(porcentagemGanhos, 1)
        porcentagemPerdas = round(porcentagemPerdas, 1)

        if primeiraCarta is not None and primeiraCarta > 5:
            if porcentagemGanhos - 0.2 > 0:
                porcentagemGanhos -= 0.2
                porcentagemPerdas += 0.2

        if self.probLimiteGanhoEnvido < porcentagemGanhos:
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
        if escolheJogo == "G": return True
        else: return False

    def chamaEnvido(self):
        """
        Método que verifica o resultado das operações. Só esse método pode usar a função print()
        """
        if self.markovEnvido(): print("true")
        else:                   print("false")

if __name__ == "__main__":
    e = Envido()
    e.main()
