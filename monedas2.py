import streamlit as st
import pandas as pd
import altair as alt
from openpyxl import Workbook
import pip



n = 14

Activo = "USD-COP"

df = pd.read_excel("USD-COP.xlsx")

st.dataframe(df,hide_index=True)

