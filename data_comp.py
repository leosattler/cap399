####################################################################################
# Programa que compara as saidas de data_handler.py.
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



# ==================================================================================
# 0) Importando planilhas com resultados a serem comparados
# ----------------------------------------------------------------------------------
# Resultado da Parte I
df1 = pd.read_excel('results1.xlsx', index_col=0)
# Resultado da Parte II
df2 = pd.read_excel('results2.xlsx', index_col=0)


# ==================================================================================
# I) Comparando speedups de cada compilador
# ----------------------------------------------------------------------------------
print('\nI) \n{0:<15} {1:<15} {2:<15}'.format('ICC', 'PGI', 'GCC'))
print('Speedup de df2 > df1 (1=sim, 0=nao)?')
print('{0:<15} {1:<15} {2:<15}'\
      .format(df2['Speedup-ICC'].mean() > df1['Speedup-ICC'].mean(), \
              df2['Speedup-PGI'].mean() > df1['Speedup-PGI'].mean(), \
              df2['Speedup-GCC'].mean() > df1['Speedup-GCC'].mean()))
print('Speedups df1:')
print('{0:<15.4} {1:<15.4} {2:<15.4}'\
      .format(df1['Speedup-ICC'].mean(), \
              df1['Speedup-PGI'].mean(), \
              df1['Speedup-GCC'].mean()))
print('Speedups df2:')
print('{0:<15.4} {1:<15.4} {2:<15.4}'\
      .format(df2['Speedup-ICC'].mean(), \
              df2['Speedup-PGI'].mean(), \
              df2['Speedup-GCC'].mean()))

print('{0:<15.4} {1:<15.4} {2:<15.4}'\
      .format(100*(stats.ar(df2['Speedup-ICC'].sum(),df1['Speedup-ICC'].sum())), \
              100*(stats.ar(df2['Speedup-PGI'].sum(),df1['Speedup-PGI'].sum())), \
              100*(stats.ar(df2['Speedup-GCC'].mean(),df1['Speedup-GCC'].mean()))))


# ==================================================================================
# II) Comparando tempo total de cada execucao
# ----------------------------------------------------------------------------------
print('\nII) \n{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15}'.\
      format('ICC(novec)', 'ICC(vec)', 'PGI(novec)', 'PGI(vec)', 'GCC(novec)', 'GCC(vec)'))
print('Tempos de execucao de df2 < df1 (1=sim, 0=nao)?')
print('{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15}'\
      .format(df2['ICC(novec)'].sum() < df1['ICC(novec)'].sum(), \
              df2['ICC(vec)'].sum() < df1['ICC(vec)'].sum(), \
              df2['PGI(novec)'].sum() < df1['PGI(novec)'].sum(), \
              df2['PGI(vec)'].sum() < df1['PGI(vec)'].sum(), \
              df2['GCC(novec)'].sum() < df1['GCC(novec)'].sum(), \
              df2['GCC(vec)'].sum() < df1['GCC(vec)'].sum()))
print('Tempos df1:')
print('{0:<15.4} {1:<15.4} {2:<15.4} {3:<15.4} {4:<15.4} {5:<15.4}'\
      .format(df1['ICC(novec)'].sum(), \
              df1['ICC(vec)'].sum(), \
              df1['PGI(novec)'].sum(), \
              df1['PGI(vec)'].sum(), \
              df1['GCC(novec)'].sum(), \
              df1['GCC(vec)'].sum()))
print('Tempos df2:')
print('{0:<15.4} {1:<15.4} {2:<15.4} {3:<15.4} {4:<15.4} {5:<15.4}'\
      .format(df2['ICC(novec)'].sum(), \
              df2['ICC(vec)'].sum(), \
              df2['PGI(novec)'].sum(), \
              df2['PGI(vec)'].sum(), \
              df2['GCC(novec)'].sum(), \
              df2['GCC(vec)'].sum()))
print('Alteracao relativa 100*(df2 - df1)/df1 (em %):')
print('{0:<15.4} {1:<15.4} {2:<15.4} {3:<15.4} {4:<15.4} {5:<15.4}'\
      .format(100*(stats.ar(df2['ICC(novec)'].sum(),df1['ICC(novec)'].sum())), \
              100*(stats.ar(df2['ICC(vec)'].sum(),df1['ICC(vec)'].sum())), \
              100*(stats.ar(df2['PGI(novec)'].sum(),df1['PGI(novec)'].sum())), \
              100*(stats.ar(df2['PGI(vec)'].sum(),df1['PGI(vec)'].sum())), \
              100*(stats.ar(df2['GCC(novec)'].sum(),df1['GCC(novec)'].sum())), \
              100*(stats.ar(df2['GCC(vec)'].sum(),df1['GCC(vec)'].sum()))))


# ==================================================================================
# III) Investigando se novos loops foram vetorizados e comparando numeros totais
# ----------------------------------------------------------------------------------
# icc)
# df1
icc_vec_loops1 = df1['Speedup-ICC'] > 1.15
icc_vec_Nloops1 = icc_vec_loops1.sum()
icc_novec_loops1 = df1['Speedup-ICC'] < 1.15 
icc_novec_Nloops1 = icc_novec_loops1.sum()
# df2
icc_vec_loops2 = df2['Speedup-ICC'] > 1.15
icc_vec_Nloops2 = icc_vec_loops2.sum()
icc_novec_loops2 = df2['Speedup-ICC'] < 1.15 
icc_novec_Nloops2 = icc_novec_loops2.sum()
# Existe algum loop que df1 NAO vetorizou mas df2 vetorizou?
icc_2over1 = icc_novec_loops1 & icc_vec_loops2
# Existe algum loop que df1 vetorizou mas df1 NAO vetorizou?
icc_1over2 = icc_vec_loops1 & icc_novec_loops2

# pgi)
pgi_vec_loops1 = df1['Speedup-PGI'] > 1.15
pgi_vec_Nloops1 = pgi_vec_loops1.sum()
pgi_novec_loops1 = df1['Speedup-PGI'] < 1.15 
pgi_novec_Nloops1 = pgi_novec_loops1.sum()
pgi_vec_loops2 = df2['Speedup-PGI'] > 1.15
pgi_vec_Nloops2 = pgi_vec_loops2.sum()
pgi_novec_loops2 = df2['Speedup-PGI'] < 1.15 
pgi_novec_Nloops2 = pgi_novec_loops2.sum()
pgi_2over1 = pgi_novec_loops1 & pgi_vec_loops2
pgi_1over2 = pgi_vec_loops1 & pgi_novec_loops2

# gcc)
gcc_vec_loops1 = df1['Speedup-GCC'] > 1.15
gcc_vec_Nloops1 = gcc_vec_loops1.sum()
gcc_novec_loops1 = df1['Speedup-GCC'] < 1.15
gcc_novec_Nloops1 = gcc_novec_loops1.sum()
gcc_vec_loops2 = df2['Speedup-GCC'] > 1.15
gcc_vec_Nloops2 = gcc_vec_loops2.sum()
gcc_novec_loops2 = df2['Speedup-GCC'] < 1.15
gcc_novec_Nloops2 = gcc_novec_loops2.sum()
gcc_2over1 = gcc_novec_loops1 & gcc_vec_loops2
gcc_1over2 = gcc_novec_loops1 & gcc_vec_loops2

# Totais
total_v_df1 = len(icc_novec_loops1)-(icc_novec_loops1 & pgi_novec_loops1 & gcc_novec_loops1).sum()
total_v_df2 = len(icc_novec_loops2)-(icc_novec_loops2 & pgi_novec_loops2 & gcc_novec_loops2).sum()

print('\nIII) \n{0:<15} {1:<15} {2:<15}'.format('ICC', 'PGI', 'GCC'))
print('df2 vetorizou algum loop nao vetorizado por df1 (1=sim, 0=nao)?')
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_2over1.sum()>0, pgi_2over1.sum()>0, gcc_2over1.sum()>0))
print('df1 vetorizou algum loop nao vetorizado por df2 (1=sim, 0=nao)?')
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_1over2.sum()>0, pgi_1over2.sum()>0, gcc_1over2.sum()>0))
print('Numero de loops vetorizados df1 (total=%i):' \
      %(total_v_df1))
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_vec_Nloops1, pgi_vec_Nloops1, gcc_vec_Nloops1))
print('Numero de loops vetorizados df2 (total=%i):' \
      %(total_v_df2))
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_vec_Nloops2, pgi_vec_Nloops2, gcc_vec_Nloops2))
print('Numero de loops nao vetorizados df1 (por nenhum=%i):' \
      %((icc_novec_loops1 & pgi_novec_loops1 & gcc_novec_loops1).sum()))
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_novec_Nloops1, pgi_novec_Nloops1, gcc_novec_Nloops1))
print('Numero de loops nao vetorizados df2 (por nenhum=%i):' \
      %((icc_novec_loops2 & pgi_novec_loops2 & gcc_novec_loops2).sum()))
print('{0:<15} {1:<15} {2:<15}'\
      .format(icc_novec_Nloops2, pgi_novec_Nloops2, gcc_novec_Nloops2))


# ==================================================================================
# IV) Investigando loops nao vetorizados
# ----------------------------------------------------------------------------------
unvectorized1 = df1.index[icc_novec_loops1 & pgi_novec_loops1 & gcc_novec_loops1]
unvectorized2 = df2.index[icc_novec_loops2 & pgi_novec_loops2 & gcc_novec_loops2]
unvectorizedAll = df1.index[icc_novec_loops1 & pgi_novec_loops1 & gcc_novec_loops1 & \
                            icc_novec_loops2 & pgi_novec_loops2 & gcc_novec_loops2]

print('\nIV) \nLoops nao vetorizados por nenhum compilador em df1 (%i):' \
      %(len(unvectorized1)))
print(unvectorized1)
print('Loops nao vetorizados por nenhum compilador em df2 (%i):' \
      %(len(unvectorized2)))
print(unvectorized2)
print('Loops nao vetorizados por nenhum compilador em ambos os casos (%i):' \
      %(len(unvectorizedAll)))
print(unvectorizedAll)
