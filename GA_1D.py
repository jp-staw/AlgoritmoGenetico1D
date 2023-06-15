from contextlib import suppress
from random import choice, choices, randint, random
from numpy import sin, exp, log, linspace, cos, e, tanh
from math import isnan, exp
import matplotlib.pyplot as plt
import latexify

#nohup python GA_TESTE.py &         -> comando para carregar o codigo no cluster

class Codigo_genetico:
    def __init__(self, genoma:list, min_max:str):
        self.genoma = genoma
        self.um_cent = int(len(genoma)*0.01)
        if min_max == 'min':
            self.min_max = min
        elif min_max == 'max':
            self.min_max = max
        self.lista_de_genoma = []
        self.repet = 100
        self.tamanho = len(genoma)
        self.prob_ind = [i + 1 for i in range(self.tamanho)]
        self.sum_prob = sum(self.prob_ind)
        self.pesos = [(self.tamanho-i)/self.sum_prob for i in range(self.tamanho)]

    def f(self, x):
        with suppress(ValueError, ZeroDivisionError, RuntimeWarning):
            return abs(x/sin(x))

    def cross(self, par_selec:list):
        return (par_selec[0]+par_selec[1])/2

    def mutacao(self, genoma:list):
        for _ in range(self.um_cent):
            ind = choice(genoma)
            genoma[genoma.index(ind)] += 0.01*((-1)**randint(1,2))
        return genoma

    def selecao_par(self, genoma:list):
        return choices(population= genoma, weights= self.pesos, k= 2)

    def desempenho(self, genoma:list):
        resultado = list(map(self.f, genoma))
        ordem_res = []
        conter = 0
        for valor in resultado:
            if valor is None:
                valor = float("nan")
            melhores_pontos = self.min_max(resultado[conter:])
            if isnan(melhores_pontos) is True:
                conter += 1
                melhores_pontos = self.min_max(resultado[conter:])
            ordem_res.append(resultado.index(melhores_pontos))
            resultado[resultado.index(melhores_pontos)] = float("nan")
        return ordem_res

    def elitismo(self, genoma:list, desenp:list):
        return [genoma[desenp[i]] for i in range(5*self.um_cent)]

    def evolucao_temporal(self):
        with open('resultados da GA.txt', 'w') as arq:
            genoma = self.genoma
            for geracoes in range(self.repet):
                desenp = self.desempenho(genoma)
                nova_geracao = self.elitismo(genoma, desenp)
                for _ in range(int(self.tamanho * 0.95)):
                    pais = self.selecao_par(genoma)
                    filhos = self.cross(pais)
                    nova_geracao.append(filhos)
                genoma = self.mutacao(nova_geracao)
                arq.write(f'{genoma[0]}    {self.f(genoma[0])}\n')
                self.lista_de_genoma.append(genoma)
        return [genoma[i] for i in self.desempenho(genoma)]

# implementar o Numba ( DEPOIS DE TERMINAR O CODIGO :D )

if __name__ == '__main__':
    with open("arquivo de parametros.txt", 'r') as parametros:
        variaveis = parametros.readlines()
        a = int(variaveis[0])
        b = int(variaveis[1])
        min_max = variaveis[2]
    chute = Codigo_genetico([randint(a,b)+random() for _ in range(200)], min_max)
    array_final = chute.evolucao_temporal()
    plt.plot(chute.lista_de_genoma,'.')
    @latexify.expression
    def funcao(x):
        return abs(x)/abs(sin(x))

    plt.title(f"$f(x) = {funcao}$")
    plt.grid()
    plt.xlabel("Gerações")
    plt.ylabel("Valor individual dos genomas")
    plt.show()
