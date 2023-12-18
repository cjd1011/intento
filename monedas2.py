import streamlit as st
import pandas as pd
import altair as alt
from openpyxl import Workbook
import pip


n = 14

Activo = "USD-COP"

Base_Historica = pd.read_excel("USD-COP.xlsx")

Base_Historica['Var'] = Base_Historica["Precio Cierre"].diff()

ordenar_df = ['fecha','Precio Cierre']

Base_Historica1 = Base_Historica[ordenar_df]

datosgov = pd.read_csv('https://www.datos.gov.co/api/views/dit9-nnvp/rows.csv?accessType=DOWNLOAD&bom=true&format=true.csv')

datosgov.to_excel('datosgov.xlsx',index= False)

datosgov['FECHA'] = pd.to_datetime(datosgov['FECHA'], format='%d/%m/%Y') #ordenar formato

datosgov.rename({'TRM':'Precio Cierre','FECHA':'fecha'}, axis=1,inplace=True) #cambios los nombres de las columnas

concatenacion = pd.concat([Base_Historica1,datosgov], ignore_index=True) #El ignore_index me sirve para que se resetee el index y no se me dañe desde el iloc

concatenacion['Nemotecnico'] = "USD/COP"

ordenar_concatenacion = ['Nemotecnico','fecha','Precio Cierre']

df = concatenacion[ordenar_concatenacion]

df['Var'] = df["Precio Cierre"].diff()

df['M. Ganancias'] = 0 # se crea la columna de M. Ganancias y se vuelve 0

df.loc[df['Var']<0,['M. Ganancias']] = 0  #Si var es menor a 0 entonces que me deje un 0
df.loc[df['Var']>0,['M. Ganancias']] = df['Var'] #si var es mayor a 0 entonces que me deje var

df['M. Perdidas'] = 0 #columna de perdidas

df.loc[df['Var']<0,['M. Perdidas']] = df['Var'] #Si var es menor a 0 entonces var sino 0
df.loc[df['Var']>0,['M. Perdidas']] = 0 # si var es mayor a 0 entonces 0

df['M. Perdidas'] = df['M. Perdidas'].abs() # valor absoluto en perdidas

EMA_M_GANANCIAS = df['M. Ganancias'].rolling(n).mean()
EMA_M_PERDIDAS = df['M. Perdidas'].rolling(n).mean()

rs = EMA_M_GANANCIAS/EMA_M_PERDIDAS

df['RSI'] = 100-(100/(1+rs))

df['SMA14'] = df['Precio Cierre'].rolling(14).mean()
df['SMA50'] = df['Precio Cierre'].rolling(50).mean()
df['SMA200'] = df['Precio Cierre'].rolling(200).mean()

df['EMA14'] = df['Precio Cierre'].ewm(span = 14,adjust = False).mean()
df['EMA50'] = df['Precio Cierre'].ewm(span = 50,adjust = False).mean()
df['EMA200'] = df['Precio Cierre'].ewm(span = 200,adjust = False).mean()

elegir_columnas = ['Nemotecnico','fecha','Precio Cierre','RSI','EMA14','EMA50','EMA200']

df1 = df[elegir_columnas].sort_values(by=['fecha'], ascending=False)

#df1.sort_values(by=['fecha'], ascending=True)

#df['Cap. Bursatil'] = df['Precio Cierre']*df['No. Acciones']

#df.to_excel(Activo+" DONE"+".xlsx",index = False,sheet_name = "RESULTADO")

st.title('Análisis del :blue[USD/COP] :bar_chart:')

#st.divider()

st.subheader('Realizado por: Camilo Diaz:briefcase:')

#st.divider()

#st.slider("This is a slider", df['fecha'])

st.dataframe(df1,hide_index=True)
