import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.colored_header import colored_header

brazil_covid_df = pd.read_csv("brazil_covid19_cities.csv")
brazil_covid_region_df = pd.read_csv("brazil_covid19.csv")

brazil_covid_df["date"] = pd.to_datetime(brazil_covid_df["date"])
brazil_covid_region_df["date"] = pd.to_datetime(brazil_covid_region_df["date"]).dt.date

st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

# // Esconde o "Made with Streamlit"
hide_st_style = """
                <style>
                footer {visibility: hidden;}
                </style>"""

st.markdown(hide_st_style, unsafe_allow_html=True)

# Muda a cor do sidebar
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #FFD700;
        }
    </style>
    """, unsafe_allow_html=True)

with st.container():
    st.sidebar.header("Sistema Nexus")
    st.sidebar.image("rounded-logo.png", width=150)
    selected_chart = st.sidebar.radio("Filtros", ["Por Cidade e Estado", "Por Região", "Por Número de Óbitos"])

with st.container():
    colored_header(
        label="Dashboard da COVID-19 no Brasil 🏥",
        description="Análise acerca dos dados das planilhas que contêm informações do número de casos de COVID-19 no "
                    "Brasil, entre 2020 a 2021.",
        color_name="yellow-80"
    )

    texto_com_link = ("Clique [aqui](https://www.kaggle.com/datasets/unanimad/corona-virus-brazil?select"
                      "=brazil_covid19_cities.csv) para visitar o Dataset.")

    st.markdown(texto_com_link, unsafe_allow_html=True)

    st.divider()

if selected_chart == "Por Cidade e Estado":
    with st.container():
        toggle_ativar_brazil_covid_df = st.toggle('Mostrar Tabela', key = 'toggle1')

        if toggle_ativar_brazil_covid_df:
            filtered_brazil_covid_extra_df = dataframe_explorer(brazil_covid_df)
            st.dataframe(filtered_brazil_covid_extra_df, use_container_width=True)

        st.subheader("Filtrando por Estado e Cidade")
        selected_state = st.selectbox('Selecione o Estado', brazil_covid_df['state'].unique())
        selected_city = st.selectbox('Selecione a Cidade',
                                     brazil_covid_df[brazil_covid_df['state'] == selected_state]['name'].unique())

        filtered_region = brazil_covid_df[
            (brazil_covid_df['state'] == selected_state) & (brazil_covid_df['name'] == selected_city)]

        if st.button("Exibir Gráfico", key="botao1"):
            st.info(f'Mostrando os dados de {selected_city}, {selected_state}', icon="ℹ️")
            st.bar_chart(filtered_region[['date', 'cases']].set_index('date'), use_container_width=True)

        st.divider()


elif selected_chart == "Por Região":
    with st.container():
        toggle_ativar_brazil_covid_region_df = st.toggle("Mostrar Tabela", key = "toggle2")

        if toggle_ativar_brazil_covid_region_df:
            filtered_brazil_covid_region_extra_df = dataframe_explorer(brazil_covid_region_df)
            st.dataframe(filtered_brazil_covid_region_extra_df, use_container_width=True)

        st.subheader('Por Região')

        start_date = st.date_input('Data de Início',
                                   min_value=brazil_covid_region_df['date'].min(),
                                   max_value=brazil_covid_region_df['date'].max(),
                                   value=brazil_covid_region_df['date'].max())
        end_date = st.date_input('Data de Término',
                                 min_value=brazil_covid_region_df['date'].min(),
                                 max_value=brazil_covid_region_df['date'].max(),
                                 value=brazil_covid_region_df['date'].max())

        filtered_date = brazil_covid_region_df[
            (brazil_covid_region_df['date'] >= start_date) & (brazil_covid_region_df['date'] <= end_date)]

        cases_by_region = filtered_date.groupby('region')['cases'].last().reset_index()

        fig_pie = px.pie(cases_by_region, values='cases', names='region',
                         title='Distribuição de Casos por Região (2020 - 2021)',
                         labels={'cases': 'Quantidade de Casos', 'region': 'Região'})

        st.plotly_chart(fig_pie, use_container_width=True)

        st.divider()

elif selected_chart == "Por Número de Óbitos":

    with st.container():

        toggle_ativar_brazil_covid_region_df = st.toggle("Mostrar Tabela", key="toggle3")

        if toggle_ativar_brazil_covid_region_df:
            filtered_brazil_covid_region_extra_df = dataframe_explorer(brazil_covid_region_df)
            st.dataframe(filtered_brazil_covid_region_extra_df, use_container_width=True)

        deaths_by_region = brazil_covid_region_df.groupby('region')['deaths'].last().reset_index()

        fig = px.bar(deaths_by_region, x='region', y='deaths', title='Óbitos Totais por Região (2020 - 2021)',
                     labels={'deaths': 'Quantidade de Mortes', 'region': 'Região'})

        st.plotly_chart(fig, use_container_width=True)
