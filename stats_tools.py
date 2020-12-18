####################################################################################
# Funcoes estatisticas para a analise de Series Temporais.
# INPE, Sao Jose dos Campos, SP, Brasil - 18 de dezembro de 2020.
# Leonardo Sattler Cassara - leocassara@igeo.ufrj.br.
####################################################################################


#====================================================================================
#                                    IMPORTS
#------------------------------------------------------------------------------------
import numpy as np
from scipy.stats import moment


#====================================================================================
#                                DEFININDO FUNCOES
#------------------------------------------------------------------------------------


# Funcao para normalizar os dados (entre 0 e 1)
def norm(dados):
    dados_norm = []
    for item in dados:
        item_norm = (item - min(dados)) / (max(dados) - min(dados))
        dados_norm.append(item_norm)
    return dados_norm


# Funcao para calcular variancia
def variancia(dados):
    v = moment(dados, moment=2)
    return v


# Funcao para calcular skewness
def skewness(dados):
    n = len(dados)
    s1 = np.sqrt(n*(n-1)) / (n-2)
    s2 = moment(dados, moment=3) / (moment(dados, moment=2)**(3/2.))
    s = s1*s2
    return s


# Funcao para calcular kurtosis
def kurtosis(dados):
    n = len(dados)
    k1 = ((n-1)*(n+1)) / ((n-2)*(n-3))
    #k1 = (n*(n+1)) / ((n-1)*(n-2)*(n-3))
    k2 = moment(dados, moment=4) / (moment(dados, moment=2)**2)
    k3 = ((n-1)**2) / ((n-2)*(n-3))
    k = k1*k2 - 3*k3
    return k


# Funcao para calcular kurtosis (nao usada - definicao compativel com scikit learn)
def kurtosis2(dados):
    n = len(dados)
    #k1 = ((n-1)*(n+1)) / ((n-2)*(n-3))
    k1 = (n*(n+1)) / ((n-1)*(n-2)*(n-3))
    k2 = moment(dados, moment=4) / (moment(dados, moment=2)**2)
    k3 = ((n-1)**2) / ((n-2)*(n-3))
    k = k2 - 3
    return k


# Funcao para retornar primeiro momento
def moment_1(dados):
    return moment(dados, moment=1)


# Funcao para retornar segundo momento
def moment_2(dados):
    return moment(dados, moment=2)


# Funcao para retornar terceiro momento
def moment_3(dados):
    return moment(dados, moment=3)


# Funcao para retornar quarto momento
def moment_4(dados):
    return moment(dados, moment=4)


# Funcao para calcular alteracao relativa
def ar(x, x_ref):
    r = (x-x_ref)/x_ref
    #print('%.2f' %(100*r))
    #print('%.3f' %(100*r))
    return r
