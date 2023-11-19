import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.colored_header import colored_header
from deep_translator import GoogleTranslator

def createMap(data, value_data, scale, map_filter):
    coordinates = {
        'AC': (-8.77, -70.55),
        'AL': (-9.71, -35.73),
        'AM': (-3.47, -62.21),
        'AP': (1.41, -51.77),
        'BA': (-12.96, -38.51),
        'CE': (-3.71, -38.54),
        'DF': (-15.78, -47.93),
        'ES': (-19.19, -40.34),
        'GO': (-16.64, -49.31),
        'MA': (-2.55, -44.30),
        'MG': (-18.10, -44.38),
        'MS': (-20.51, -54.54),
        'MT': (-12.64, -55.42),
        'PA': (-5.53, -52.29),
        'PB': (-7.06, -35.55),
        'PE': (-8.28, -35.07),
        'PI': (-8.28, -43.68),
        'PR': (-24.89, -51.55),
        'RJ': (-22.84, -43.15),
        'RN': (-5.79, -36.51),
        'RO': (-11.22, -62.80),
        'RR': (1.99, -61.33),
        'RS': (-30.01, -51.22),
        'SC': (-27.33, -49.44),
        'SE': (-10.95, -37.07),
        'SP': (-23.55, -46.64),
        'TO': (-10.25, -48.25)
    }

    tradutor = GoogleTranslator(source="en", target="pt")

    if map_filter == "Soma":

        data = data[["state", value_data]].groupby("state").sum().reset_index()

    elif map_filter == "Média":

        data = data[["state", value_data]].groupby("state").mean().reset_index()

    else:

        pass

    # Cria um gráfico template
    fig = go.Figure()

    text = tradutor.translate(value_data)

    # Pega o valor máximo do Series value_data ("deaths" ou "cases")
    max_value = data[value_data].max()

    # Percorre cada instância (linha) de DataFrameGroupBy
    for _, row in data.iterrows():
        state = row["state"]
        value = row[value_data]

        # Reduz a diferença de tamanho do maior valor em relação ao restante
        if value == max_value:


            if map_filter == "Soma":
                marker_size = value * (scale - scale / 3)
            else: 
                marker_size = value * (scale - scale / 1.09)
        else:
            marker_size = value * scale

        # Adiciona um novo gráfico (objeto Scattergeo) dentro do objeto Figure
        fig.add_trace(go.Scattergeo(
            name=state,
            locationmode="ISO-3",
            lat=[coordinates[state][0]],
            lon=[coordinates[state][1]],
            text=[f"{state}: {str(round(value,2)).replace('.', ',')} {text}"],
            mode="markers",
            marker={
                "size": marker_size,
                "opacity": 0.7,
                "reversescale": True,
                "autocolorscale": True,
                "symbol": "circle",
                "line": {
                    "width": 1,
                    "color": "rgb(102, 102, 102)"
                }
            }))

    # Atualiza o layout do gráfico template (Agora com o gráfico Scattergeo incluso)
    fig.update_layout(
        title=f"{text.capitalize()} de COVID-19 em Cada Estado",
        geo={
            "scope": "south america",
            "showland": True,
            "center": {
                "lon": -55,
                "lat": -12
            },
            "projection_scale": 4
        },
        width = 800,
        height = 800,
    )

    return fig


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
    selected_chart = st.sidebar.radio("Filtros",
                                      ["Por Cidade e Estado", "Por Região", "Por Número de Óbitos", "Visualizar Mapas"])

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
        toggle_ativar_brazil_covid_df = st.toggle('Mostrar Tabela', key='toggle1')

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
        toggle_ativar_brazil_covid_region_df = st.toggle("Mostrar Tabela", key="toggle2")

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

elif selected_chart == "Visualizar Mapas":

    with st.container():

        filtro = st.selectbox(label="Filtros", options=("Soma", "Média"))

        # Retorna um booleano
        if st.button("Exibir Gráficos", key="botao2"):

            if filtro == "Soma":
                map_graph_deaths = createMap(brazil_covid_df, "deaths", 0.000005, filtro)
                st.plotly_chart(map_graph_deaths)

                map_graph_cases = createMap(brazil_covid_df, "cases", 0.0000001, filtro)
                st.plotly_chart(map_graph_cases)

            else:
                map_graph_deaths = createMap(brazil_covid_df, "deaths", 0.35, filtro)
                st.plotly_chart(map_graph_deaths)

                map_graph_cases = createMap(brazil_covid_df, "cases", 0.01, filtro)
                st.plotly_chart(map_graph_cases)
