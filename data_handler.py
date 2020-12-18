####################################################################################
# Programa que analisa os resultados presentes na pasta sdumont dete repositorio.
# INPE, Sao Jose dos Campos, SP, Brasil - 18 de dezembro de 2020.
# Leonardo Sattler Cassara - leocassara@igeo.ufrj.br.
####################################################################################


# ==================================================================================
#                             IMPORTS
# ----------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import stats_tools as stats
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


# ==================================================================================
# Parte I - a)
# ----------------------------------------------------------------------------------
# Importando arquivos

# icc)
out_icc_novec = np.genfromtxt('sdumont/ICC_2/icc_novec.out', skip_header=4, dtype='str')
out_icc_vec = np.genfromtxt('sdumont/ICC_2/icc_vec.out', skip_header=4, dtype='str')

# pgi)
out_pgi_novec = np.genfromtxt('sdumont/PGI_2/pgi_novec.out', skip_header=4, dtype='str')
out_pgi_vec = np.genfromtxt('sdumont/PGI_2/pgi_vec.out', skip_header=4, dtype='str')

# gcc)
out_gcc_novec = np.genfromtxt('sdumont/GCC_2/gcc_novec.out', skip_header=4, dtype='str')
out_gcc_vec = np.genfromtxt('sdumont/GCC_2/gcc_vec.out', skip_header=4, dtype='str')

# Nome dos arquivos de output
NAME = '2'

# Gerando datacube com dados de output relevantes 
data_cube = np.concatenate( [out_icc_novec[:,[1]], out_icc_vec[:,[1]], \
                             out_pgi_novec[:,[1]], out_pgi_vec[:,[1]], \
                             out_gcc_novec[:,[1]], out_gcc_vec[:,[1]]], axis=1 )
# Colunas do dataframe
compilations = ['ICC(novec)', 'ICC(vec)',\
                'PGI(novec)', 'PGI(vec)',\
                'GCC(novec)', 'GCC(vec)']

# Indices do dataframe
loop_names = out_icc_novec[:,0]

# Gerando dataframe a partir do datacube 
df = pd.DataFrame( data_cube, index = loop_names, columns = compilations )

# Convertendo os tipos de dados do dataframe
df = df.astype({'ICC(novec)':float, 'ICC(vec)':float, \
                'PGI(novec)':float, 'PGI(vec)':float, \
                'GCC(novec)':float, 'GCC(vec)':float})

# Printando os primeiros 4 valores da tabela
print('a) Planilha com resultados das execucoes:')
print(df.head(4))


# ==================================================================================
# Parte I - b)
# ----------------------------------------------------------------------------------
# Calculando o Speedup de cada loop

# icc)
icc_novec = df['ICC(novec)'].to_numpy(dtype='float')
icc_vec = df['ICC(vec)'].to_numpy(dtype='float')
icc_speedup = icc_novec/icc_vec
# Inserindo no dataframe
df.insert(2, 'Speedup-ICC', icc_speedup)

# pgi)
pgi_novec = df['PGI(novec)'].to_numpy(dtype='float')
pgi_vec = df['PGI(vec)'].to_numpy(dtype='float')
pgi_speedup = pgi_novec/pgi_vec
# Inserindo no dataframe
df.insert(5, 'Speedup-PGI', pgi_speedup)

# gcc)
gcc_novec = df['GCC(novec)'].to_numpy(dtype='float')
gcc_vec = df['GCC(vec)'].to_numpy(dtype='float')
gcc_speedup = gcc_novec/gcc_vec
# Inserindo no dataframe
df.insert(8, 'Speedup-GCC', gcc_speedup)

# Printando os primeiros 4 valores da tabela
print('\nb) Planilha apos calculo dos Speedups:')
print(df.head(4))


# ==================================================================================
# Parte I - c)
# ----------------------------------------------------------------------------------
# Calculando o speedup medio 

# icc)
icc_avg_speedup = np.mean(icc_speedup)

# pgi)
pgi_avg_speedup = np.mean(pgi_speedup)

# gcc)
gcc_avg_speedup = np.mean(gcc_speedup)

# Printando resultados
print('\nc) Speedup medio:')
print('{0:<15} {1:<15} {2:<15}'.format('ICC', 'PGI', 'GCC'))
print('{0:<15.4} {1:<15.4} {2:<15.4}'\
      .format(icc_avg_speedup, pgi_avg_speedup, gcc_avg_speedup))


# ==================================================================================
# Parte I - d)
# ----------------------------------------------------------------------------------
# Calculando o tempo total de cada execucao

# icc)
icc_total_novec = np.sum(icc_novec)
icc_total_vec = np.sum(icc_vec)

# pgi)
pgi_total_novec = np.sum(pgi_novec)
pgi_total_vec = np.sum(pgi_vec)

# gcc)
gcc_total_novec = np.sum(gcc_novec)
gcc_total_vec = np.sum(gcc_vec)

# Printando resultados
print('\nd) Tempo total das execucoes em segundos:')
print('{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15}'\
      .format('ICC(novec)', 'ICC(vec)', 'PGI(novec)', 'PGI(vec)', 'GCC(novec)', 'GCC(vec)'))
print('{0:<15.3} {1:<15.3} {2:<15.3} {3:<15.3} {4:<15.3} {5:<15.3}'\
      .format(icc_total_novec, icc_total_vec, pgi_total_novec, pgi_total_vec, gcc_total_novec, gcc_total_vec))


# ==================================================================================
# Parte I - e)
# ----------------------------------------------------------------------------------
# Descobrindo loops vetorizados e nao vetorizados com limiar de speedup=1.5

# icc)
icc_vec_loops = df['Speedup-ICC'] > 1.15
icc_vec_Nloops = icc_vec_loops.sum()
icc_novec_loops = df['Speedup-ICC'] < 1.15 
icc_novec_Nloops = icc_novec_loops.sum()

# pgi)
pgi_vec_loops = df['Speedup-PGI'] > 1.15
pgi_vec_Nloops = pgi_vec_loops.sum()
pgi_novec_loops = df['Speedup-PGI'] < 1.15 
pgi_novec_Nloops = pgi_novec_loops.sum()

# gcc)
gcc_vec_loops = df['Speedup-GCC'] > 1.15
gcc_vec_Nloops = gcc_vec_loops.sum()
gcc_novec_loops = df['Speedup-GCC'] < 1.15 
gcc_novec_Nloops = gcc_novec_loops.sum()

# Printando resultados
print('\ne) Numero de loops vetorizados (yes) e nao vetorizados (no) por compilador:')
print('{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15}'\
      .format('ICC (no)','ICC (yes)','PGI (no)','PGI (yes)','GCC (no)','GCC (yes)'))
print('{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15}'\
      .format(icc_novec_Nloops, icc_vec_Nloops, pgi_novec_Nloops, pgi_vec_Nloops, gcc_novec_Nloops, gcc_vec_Nloops))


# ==================================================================================
# Parte I - f)
# ----------------------------------------------------------------------------------
# Descobrindo loops que nao foram vetorizados por nenhum compilador
unvectorized = df.index[icc_novec_loops & pgi_novec_loops & gcc_novec_loops]

print('\nf) Loops nao vetorizados por nenhum compilador (%i):' \
      %(len(unvectorized)))
print(unvectorized)


# ==================================================================================
#                         Output 1 -  Planilha
# ----------------------------------------------------------------------------------
df.to_excel('results'+NAME+'.xlsx')


# ==================================================================================
#                         Output 2 - Histograma 
# ----------------------------------------------------------------------------------
# Histograma do item I.a) 

# Parametros do histograma
# Numero de bins
nbins = 25
# Tamanho do bin
binsize = .8
'''
# Limite de 'distancia da media' de uma amostra,
# onde distancia = limit * std(amostras),
# para considera-la no histograma (atualmente desativado)
limit = np.inf

# Amostras icc
icc_v = icc_vec[np.logical_and(icc_vec > icc_vec.mean() - limit * icc_vec.std(), \
icc_vec <= icc_vec.mean() + limit * icc_vec.std())]
icc_n = icc_novec[np.logical_and(icc_novec > icc_novec.mean() - limit * icc_novec.std(), \
icc_novec <= icc_novec.mean() + limit * icc_novec.std())]

# Amostras pgi
pgi_v = pgi_vec[np.logical_and(pgi_vec > pgi_vec.mean() - limit * pgi_vec.std(), \
pgi_vec <= pgi_vec.mean() + limit * pgi_vec.std())]
pgi_n = pgi_novec[np.logical_and(pgi_novec > pgi_novec.mean() - limit * pgi_novec.std(), \
pgi_novec <= pgi_novec.mean() + limit * pgi_novec.std())]

# Amostras gcc
gcc_v = gcc_vec[np.logical_and(gcc_vec > gcc_vec.mean() - limit * gcc_vec.std(), \
gcc_vec <= gcc_vec.mean() + limit * gcc_vec.std())]
gcc_n = gcc_novec[np.logical_and(gcc_novec > gcc_novec.mean() - limit * gcc_novec.std(), \
gcc_novec <= gcc_novec.mean() + limit * gcc_novec.std())]
'''

# Definindo bins
xbins = np.histogram(icc_vec, bins=nbins)[1] # plt.hist(icc_vec, bins=nbins, rwidth=binsize)[1]
# plt.close('all')

# Gerando figura
plt.figure(figsize=(16,5))

# icc)
plt.subplot(1,3,1)
icc_labn = '\n mean: %.3f \n median: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(icc_novec.mean(), np.median(icc_novec), icc_novec.std(), stats.skewness(icc_novec), stats.kurtosis(icc_novec))
icc_labv = '\n mean: %.3f \n median: %.3f  \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(icc_vec.mean(), np.median(icc_vec), icc_vec.std(), stats.skewness(icc_vec), stats.kurtosis(icc_vec))
'''
icc_labn = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(icc_n.mean(), icc_n.std(), stats.skewness(icc_n), stats.kurtosis(icc_n))
icc_labv = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(icc_v.mean(), icc_v.std(), stats.skewness(icc_v), stats.kurtosis(icc_v))
'''
plt.title('ICC', size=17)
plt.hist([icc_novec,icc_vec], bins=nbins, rwidth=binsize, align='mid', \
         color = ["tab:orange", "tab:blue"], \
         label = ["Novec: " + icc_labn, "\nVec: " + icc_labv])
plt.xlabel('Time [s]', size=15)
plt.tick_params(labelsize=14)
plt.legend(fontsize=13)

# pgi)
plt.subplot(1,3,2)
pgi_labn = '\n mean: %.3f \n median: %.3f  \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(pgi_novec.mean(), np.median(pgi_novec), pgi_novec.std(), stats.skewness(pgi_novec), stats.kurtosis(pgi_novec))
pgi_labv = '\n mean: %.3f \n median: %.3f  \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(pgi_vec.mean(), np.median(pgi_vec), pgi_vec.std(), stats.skewness(pgi_vec), stats.kurtosis(pgi_vec))
'''
pgi_labn = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(pgi_n.mean(), pgi_n.std(), stats.skewness(pgi_n), stats.kurtosis(pgi_n))
pgi_labv = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(pgi_v.mean(), pgi_v.std(), stats.skewness(pgi_v), stats.kurtosis(pgi_v))
'''
plt.title('PGI', size=17)
plt.hist([pgi_novec,pgi_vec], bins=nbins, rwidth=binsize, align='mid', \
         color = ["tab:orange", "tab:blue"], \
         label = ["Novec:" + pgi_labn, "\nVec: " + pgi_labv])
plt.xlabel('Time [s]', size=15)
plt.tick_params(labelsize=14)
plt.legend(fontsize=13)

# gcc)
plt.subplot(1,3,3)
gcc_labn = '\n mean: %.3f \n median: %.3f  \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(gcc_novec.mean(), np.median(gcc_novec), gcc_novec.std(), stats.skewness(gcc_novec), stats.kurtosis(gcc_novec))
gcc_labv = '\n mean: %.3f \n median: %.3f  \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
           %(gcc_vec.mean(), np.median(gcc_vec), gcc_vec.std(), stats.skewness(gcc_vec), stats.kurtosis(gcc_vec))
'''
gcc_labn = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(gcc_n.mean(), gcc_n.std(), stats.skewness(gcc_n), stats.kurtosis(gcc_n))
gcc_labv = '\n mean: %.3f \n std: %.3f \n skew: %.3f \n kurt: %.3f ' \
%(gcc_v.mean(), gcc_v.std(), stats.skewness(gcc_v), stats.kurtosis(gcc_v))
'''
plt.title('GCC', size=17)
plt.hist([gcc_novec,gcc_vec], bins=nbins, rwidth=binsize, align='mid', \
         color = ["tab:orange", "tab:blue"], \
         label = ["Novec:" + gcc_labn, "\nVec: " + gcc_labv])
plt.xlabel('Time [s]', size=15)
plt.tick_params(labelsize=14)
plt.legend(fontsize=13)

plt.savefig('stats'+NAME+'.jpg', dpi=500, bbox_inches='tight') 
plt.show()


# ==================================================================================
#   Output 3 - Diagrama de Venn (somente valores; figura feita em TikZ)
# ----------------------------------------------------------------------------------
# Diagrama do item I.e) 

# ICC intersecao PGI intersecao GCC 
a = (icc_vec_loops & pgi_vec_loops & gcc_vec_loops).sum()
# ICC intersecao PGI - GCC
b = (icc_vec_loops & pgi_vec_loops & gcc_novec_loops).sum()
# PGI intersecao GCC - ICC
c = (icc_novec_loops & pgi_vec_loops & gcc_vec_loops).sum()
# ICC intersecao GCC - PGI
d = (icc_vec_loops & pgi_novec_loops & gcc_vec_loops).sum()
# ICC - PGI - GCC
e = (icc_vec_loops & pgi_novec_loops & gcc_novec_loops).sum()
# PGI - ICC - GCC
f = (icc_novec_loops & pgi_vec_loops & gcc_novec_loops).sum()
# GCC - ICC - PGI
g = (icc_novec_loops & pgi_novec_loops & gcc_vec_loops).sum()


# ==================================================================================
#  Output 4 - Tabela formatada em LaTeX com nomes dos loops nao vetorizados
# ----------------------------------------------------------------------------------
# Criando tabela do item I.f) (COMENTADO POIS TABELA JA FOI ADICIONADA AO MANUSCRITO)
'''
for i, v in enumerate(unvectorized):
    if (i+1)%9==0:
        print(v+' \\'+'\\')
    else:
        print(v + ' & ',end='')
'''
