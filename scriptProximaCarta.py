import json as js
import sys
import random as rd


class ProximaCarta:
    def __init__(self):
        self.combCartas = []                      #minhas combinações de cartas

        self.primeiraCartaRobo   = None           # primeira carta jogada pelo robo
        self.segundaCartaRobo    = None           # segunda carta jogada pelo robo
        self.terceiraCartaRobo   = None           # terceira carta jogada pelo robo
        self.cartaAltaRobo       = None           # carta alta do robo
        self.cartaMediaRobo      = None           # carta media do robo
        self.cartaBaixaRobo      = None           # carta alta do robo
        self.primeiraCartaHumano = None           # primeira carta jogada pelo humano
        self.segundaCartaHumano  = None           # segunda carta jogada pelo humano
        self.terceiraCartaHumano = None           # terceira carta jogada pelo humano

        self.possiveisCombCartas = []             # possiveis combinações de cartas do adversário

        self.pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/"
        self.trucoDescription = {}                # classe trucoDescription
        self.rodada           = 0                 # rodada atual
        self.qualCarta        = 0                 # qual carta eu tenho que jogar, 1, 2 ou 3
        self.quemMao          = 0                 # quem é a mão da rodada

        self.ordem       = []                     # ordem das cartas (menor para maior)
        self.codificacao = []                     # codificação das cartas

        self.cabecalhoMatProbProximaCarta = []    # cabeçalho das matrizes de markov
        self.cabecalhoMatQtdCartas        = []    # cabeçalho da matriz de quantidades
        self.matrizProximaCartaVitoria    = [[]]  # matriz de probabilidades de vitoria
        self.matrizProximaCartaDerrota    = [[]]  # matriz de probabilidades de derrota
        self.matrizQtdCartas              = [[]]  # matriz de quantidades das cartas

    def main(self):
        """
        Método inicial que é chamado de fora da classe e executa as operações
        """
        self.trucoDescription = js.load(open(self.pasta + 'trucoDescription.json', 'r'))
        self.rodada  = int(sys.argv[1])
        self.qualCarta = float(sys.argv[2])
        self.quemMao = self.trucoDescription['jogadorMao']
        self.codificacao = [1, 2, 3, 4, 6, 7, 8, 12, 16, 24, 40, 42, 50, 52]

        self.extraindoMatrizes()
        self.defineCartas()
        self.defineCombMao()
        self.jogaProximaCarta()

    def extraindoMatrizes(self):
        """
        Método que extrai dos arquivos as matrizes de vitória e derrota e coloca nas variáveis da classe
        """
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

        self.matrizProximaCartaVitoria = matrizVit
        self.matrizProximaCartaDerrota = matrizDer
        self.matrizQtdCartas           = matrizQtdCartas

        vitoria.close()
        derrota.close()
        qtdCartas.close()

    def definePossiveisCombMao(self):
        """
        Método que verifica as cartas já jogadas pelo oponente e a partir delas gera as combinações.
        """
        if self.primeiraCartaHumano is None and self.segundaCartaHumano is None and self.terceiraCartaHumano is None:
            self.possiveisCombCartas = self.cabecalhoMatProbProximaCarta.copy()
        elif self.primeiraCartaHumano is not None and self.segundaCartaHumano is None and self.terceiraCartaHumano is None:
            nivelCarta = self.analisaNivelCarta(self.primeiraCartaHumano) #analisa qual carta foi jogada
            listaCartasRestantes = self.analisaCartasRestantes(nivelCarta)  #ve quais cartas sobraram

            self.possiveisCombCartas.append(nivelCarta + listaCartasRestantes[0] + listaCartasRestantes[1])
            self.possiveisCombCartas.append(nivelCarta + listaCartasRestantes[1] + listaCartasRestantes[0])
        elif self.primeiraCartaHumano is not None and self.segundaCartaHumano is not None and self.terceiraCartaHumano is None:
            niveis = ["b", "m", "a"]
            nivelCarta1 = self.analisaNivelCarta(self.primeiraCartaHumano)
            nivelCarta2 = self.analisaNivelCarta(self.segundaCartaHumano)

            if nivelCarta1 == nivelCarta2:
                carta1 = self.cabecalhoMatQtdCartas.index(self.primeiraCartaHumano)
                carta2 = self.cabecalhoMatQtdCartas.index(self.segundaCartaHumano)

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

            self.possiveisCombCartas.append(nivelCarta1 + nivelCarta2 + niveis[0])

    def analisaNivelCarta(self, carta):
        """
        Método que analisa o nível da carta, se é baixa, média ou alta, de acordo com a quantidade de vezes que
        ela foi baixa, média ou alta.
        :param carta: carta a ser analisada
        :return: b se é baixa, m se é media e a se é alta
        """
        qtdB = self.matrizQtdCartas[0][self.cabecalhoMatQtdCartas.index(carta)]
        qtdM = self.matrizQtdCartas[1][self.cabecalhoMatQtdCartas.index(carta)]
        qtdA = self.matrizQtdCartas[2][self.cabecalhoMatQtdCartas.index(carta)]

        if qtdB >= qtdM and qtdB >= qtdA:
            return "b"
        elif qtdM >= qtdB and qtdM >= qtdA:
            return "m"
        elif qtdA >= qtdB and qtdA >= qtdM:
            return "a"

    def analisaCartasRestantes(self, carta):
        """
        Método que analisa quais serão as cartas restantes na combinação.
        :param carta: carta a ser analisada
        :return: lista com as cartas restantes
        """
        if carta == "b":
            return ["m", "a"]
        elif carta == "m":
            return ["b", "a"]
        elif carta == "a":
            return ["b", "m"]

    def defineCartas(self):
        """
        Método que define as variáveis de cartas.
        """
        self.primeiraCartaRobo   = self.trucoDescription['primeiraCartaRobo']
        self.segundaCartaRobo    = self.trucoDescription['segundaCartaRobo']
        self.cartaAltaRobo       = self.trucoDescription['cartaAltaRobo']
        self.cartaMediaRobo      = self.trucoDescription['cartaMediaRobo']
        self.cartaBaixaRobo      = self.trucoDescription['cartaBaixaRobo']
        self.primeiraCartaHumano = self.trucoDescription['primeiraCartaHumano']
        self.segundaCartaHumano  = self.trucoDescription['segundaCartaHumano']
        self.terceiraCartaHumano = self.trucoDescription['terceiraCartaHumano']

    def defineCombMao(self):
        """
        Método que define a variável de combinação da classe
        """
        if self.qualCarta == 0.1 and self.rodada == 1:
            self.combCartas = self.cabecalhoMatProbProximaCarta.copy()
        elif self.qualCarta == 0.2 and self.rodada == 2:
            for comb in self.cabecalhoMatProbProximaCarta:
                if comb[0] == self.nivelCartaJogada(self.primeiraCartaRobo):
                    self.combCartas.append(comb)

    def nivelCartaJogada(self, carta):
        """
        Método que analisa o nível da carta já jogada
        :param carta: carta a ser analisada
        :return: b se é baixa, m se é média e a se é alta
        """
        if carta == self.cartaBaixaRobo:
            return "b"
        elif carta == self.cartaMediaRobo:
            return "m"
        elif carta == self.cartaAltaRobo:
            return "a"

    def analisaQualCartaNaoFoiJogada(self):
        """
        Método que qual carta do oponente ainda não foi jogada, baixa, média ou alta.
        :return: carta ainda não jogada
        """
        if self.primeiraCartaRobo == self.cartaBaixaRobo:
            if self.segundaCartaRobo == self.cartaMediaRobo:
                return self.cartaAltaRobo
            elif self.segundaCartaRobo == self.cartaAltaRobo:
                return self.cartaMediaRobo
        elif self.primeiraCartaRobo == self.cartaMediaRobo:
            if self.segundaCartaRobo == self.cartaBaixaRobo:
                return self.cartaAltaRobo
            elif self.segundaCartaRobo == self.cartaAltaRobo:
                return self.cartaBaixaRobo
        elif self.primeiraCartaRobo == self.cartaAltaRobo:
            if self.segundaCartaRobo == self.cartaBaixaRobo:
                return self.cartaMediaRobo
            elif self.segundaCartaRobo == self.cartaMediaRobo:
                return self.cartaBaixaRobo

    def markovProximaCarta(self):
        """
        Método que executa todas as operações
        :return: falso se não tem pontos de flor, se não alcançou o mínimo ou se os calculos
                 não forem positivos para a questão, e true se os resultados derem positivo.
        """
        # se for a terceira carta a ser jogada, joga a que sobrou
        if self.rodada == 3:
            return self.analisaQualCartaNaoFoiJogada()

        self.definePossiveisCombMao()

        ganhosPossiveisProxCarta = []
        perdasPossiveisProxCarta = []
        listaBMA = []

        # contabiliza derrotas e vitorias
        for minhaComb in self.combCartas:
            ganhos = 0
            perdas = 0
            for comb in self.possiveisCombCartas:
                ganhos += int(self.matrizProximaCartaVitoria[self.cabecalhoMatProbProximaCarta.index(minhaComb)][self.cabecalhoMatProbProximaCarta.index(comb)])
                perdas += int(self.matrizProximaCartaDerrota[self.cabecalhoMatProbProximaCarta.index(minhaComb)][self.cabecalhoMatProbProximaCarta.index(comb)])
            ganhosPossiveisProxCarta.append(ganhos)
            perdasPossiveisProxCarta.append(perdas)

        porcentagemBaixa = 0
        porcentagemMedia = 0
        porcentagemAlta = 0

        # calcula porcentagens de acordo com qual carta tem que jogar
        if self.qualCarta == 0.1:
            primeiraBaixa = 0
            primeiraMedia = 0
            primeiraAlta  = 0

            for comb in self.combCartas:
                if comb[0] == "b":
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        primeiraBaixa += ganho
                elif comb[0] == "m":
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        primeiraMedia += ganho
                elif comb[0] == "a":
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        primeiraAlta += ganho

            if primeiraBaixa == 0 and primeiraMedia == 0 and primeiraAlta == 0:
                primeiraBaixa = 1
                primeiraMedia = 1
                primeiraAlta = 1

            porcentagemBaixa = round(primeiraBaixa / (primeiraBaixa + primeiraMedia + primeiraAlta), 1)
            porcentagemMedia = round(primeiraMedia / (primeiraBaixa + primeiraMedia + primeiraAlta), 1)
            porcentagemAlta = round(primeiraAlta / (primeiraBaixa + primeiraMedia + primeiraAlta), 1)
        elif self.qualCarta == 0.2:
            segundaBaixa = 0
            segundaMedia = 0
            segundaAlta = 0

            for comb in self.combCartas:
                if comb[1] == "b" and comb[1] not in self.nivelCartaJogada(self.primeiraCartaRobo):
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        segundaBaixa += ganho
                elif comb[1] == "m" and comb[1] not in self.nivelCartaJogada(self.primeiraCartaRobo):
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        segundaMedia += ganho
                elif comb[1] == "a" and comb[1] not in self.nivelCartaJogada(self.primeiraCartaRobo):
                    ganho = ganhosPossiveisProxCarta[self.combCartas.index(comb)]
                    perda = perdasPossiveisProxCarta[self.combCartas.index(comb)]

                    porcentagemGanho = round(ganho / (ganho + perda), 1)
                    porcentagemPerda = round(perda / (ganho + perda), 1)

                    if porcentagemGanho > porcentagemPerda:
                        segundaAlta += ganho

            if segundaBaixa == 0 and segundaMedia == 0 and segundaAlta == 0:
                jogada = self.nivelCartaJogada(self.primeiraCartaRobo)
                if "b" not in jogada:
                    segundaBaixa = 1
                if "m" not in jogada:
                    segundaMedia = 1
                if "a" not in jogada:
                    segundaAlta = 1

            porcentagemBaixa = round(segundaBaixa / (segundaBaixa + segundaMedia + segundaAlta), 1)
            porcentagemMedia = round(segundaMedia / (segundaBaixa + segundaMedia + segundaAlta), 1)
            porcentagemAlta = round(segundaAlta / (segundaBaixa + segundaMedia + segundaAlta), 1)

        # insere na lista para randomizar
        for i in range(int(porcentagemBaixa * 10)):
            listaBMA.append("B")

        for i in range(int(porcentagemMedia * 10)):
            listaBMA.append("M")

        for i in range(int(porcentagemAlta * 10)):
            listaBMA.append("A")

        # escolhe randomico da lista
        escolheJogo = rd.choice(listaBMA)

        # retorna a carta que escolheu
        if escolheJogo == "B":
            return self.cartaBaixaRobo
        elif escolheJogo == "M":
            return self.cartaMediaRobo
        elif escolheJogo == "A":
            return self.cartaAltaRobo

    def jogaProximaCarta(self):
        """
        Método que verifica o resultado das operações. Só esse método pode usar a função print()
        """
        resultado = self.markovProximaCarta()
        print(resultado)


if __name__ == "__main__":
    p = ProximaCarta()
    p.main()