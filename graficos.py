import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sc

def gamma(l, a, l_0, g_0):
    return 2*g_0/(1+np.exp(a*(l-l_0)))

def L(l, a, l_0, g_0, A):
    return 2*A/(np.pi*gamma(l, a, l_0, g_0))/(1+4*((l-l_0)/gamma(l, a, l_0, g_0))**2)

def G(l, a, l_0, g_0, A):
    return A/gamma(l, a, l_0, g_0)*np.sqrt(4*np.log(2)/np.pi)*np.exp(-4*np.log(2)*((l-l_0)/gamma(l, a, l_0, g_0))**2)

def f_blaster(l, a, l_0, g_0, A, f):
    return f*L(l, a, l_0, g_0, A) + (1-f)*G(l, a, l_0, g_0, A)

dados_l = []
dados_y = []

arquivo = "teste"#"Amarelo_600.csv"
with open(arquivo, "r") as arq:
    dados = arq.readlines()
    for i in dados:
        linha = i.split("\t")
        dados_l.append(float(linha[0]))
        dados_y.append(float(linha[1]))

#parametros = sc.curve_fit(f_blaster, dados_l, dados_y)[0]
parametros = sc.curve_fit(G, dados_l, dados_y)[0]

a = parametros[0]
l_0 = parametros[1]
g_0 = parametros[2]
A = parametros[3]
#f = parametros[4]

#print(arquivo.rstrip(".csv"))

#f_dados = list(map(lambda x: f_blaster(x, a, l_0, g_0, A, f), dados_l))
#f_gamma = list(map(lambda x: gamma(x, a, l_0, g_0), dados_l))
f_L = list(map(lambda x: G(x, a, l_0, g_0, A), dados_l))

#plt.plot(dados_l, dados_y)
#plt.plot(f_dados, dados_y)
plt.plot(f_L, dados_y)

plt.show()