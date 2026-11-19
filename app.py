import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium





# Configuración inicial de la página
st.set_page_config(
    page_title="Comparativa Epidemiológica: COVID-19 vs A(H1N1)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def load_data():
    return pd.read_csv("casos_COVID_por_Entidad.csv")
df = load_data()

@st.cache_data
def load_data_activos():
    return pd.read_csv("casos_covid_activos.csv")
df2 = load_data_activos()



#ENCABEZADO
st.markdown(
    "<span style='background-color: #2563eb; color: white; padding: 4px 10px;"
    " border-radius: 9999px; font-size: 11px; font-weight:"
    " bold;'>ANÁLISIS EPIDEMIOLÓGICO NACIONAL</span>",
    unsafe_allow_html=True,
)

st.title("Comparativa Epidemiológica: COVID-19 vs A(H1N1) en México")



#DESCRIPCION
st.markdown("---")
col_info_1, col_info_2 = st.columns(2)

with col_info_1:
    st.markdown("#### COVID-19")
    st.write(
        "Enfermedad respiratoria aguda causada por el virus SARS-CoV-2."
    )
    st.markdown("##### Síntomas:")
    st.write(
        "Fiebre, tos, dolor de garganta, congestión o secreción nasal, "
        "dolor de cabeza, dolor muscular o corporal, fatiga o cansancio."
    )
    st.markdown("##### Método de Propagación:")
    st.write(
        "Se propaga principalmente de persona a persona a través de gotitas "
        "que se expulsan cuando una persona infectada tose, estornuda, "
        "habla o respira. También puede contraerse al tocar superficies "
        "u objetos contaminados y luego llevarse las manos a la cara, la nariz o la boca."
    )

with col_info_2:
    st.markdown("#### A(H1N1)")
    st.write(
        "Infección respiratoria viral aguda provocada por una cepa del virus de la "
        "influenza A."
    )
    st.markdown("##### Síntomas:")
    st.write(
        "Fiebre alta, tos intensa y persistente, dolor de garganta, carraspera, "
        "dolores musculares, dolor en articulaciones, dolor de cabeza, fatiga extrema, "
        "debilidad general, escalofríos, sudoración, congestión o escurrimiento nasal."
    )
    st.markdown("##### Método de Propagación:")
    st.write(
        "Se propaga a través de gotitas de saliva que se expulsan al toser, "
        "estornudar o hablar; o bien, al tocar superficies contaminadas con "
        "el virus y luego llevarse las manos a la boca, la nariz o los ojos."
    )

st.markdown("---")



#PESTAÑAS
tab_general, tab_covid, tab_h1n1 = st.tabs(
    ["Vista General", "COVID-19", "H1N1"]
)

# PESTAÑA:VISTA GENERAL
with tab_general:
    st.markdown("### Vista General - Análisis Global")
    ano_general = st.radio(
        "Selecciona el periodo temporal:",
        [
            "Suma de Casos",
            "1° Año",
            "2° Año",
            "3° Año",
        ],  
        index=0,
        horizontal=True,
        key="radio_general",
    )

    if ano_general == "Suma de Casos":
        df_mapa_gen_covid = (
            df.groupby(["ENTIDAD_RES", "ENTIDAD_FEDERATIVA", "LATITUD", "LONGITUD"])["CASOS"]
            .sum()
            .reset_index()
        )
    else:
        mapa_anos = {
            "1° Año": 2020,
            "2° Año": 2021,
            "3° Año": 2022
        }
        anio_objetivo = mapa_anos[ano_general]
        df_mapa_gen_covid = df[df["AÑO"] == anio_objetivo].copy()

    col_mapa_covid, col_mapa_h1n1 = st.columns(2)

    with col_mapa_covid:
        st.markdown("#### Mapa COVID-19")
        fig_gen_covid = px.scatter_map(
            df_mapa_gen_covid,
            lat="LATITUD",
            lon="LONGITUD",
            size="CASOS",
            color="CASOS",
            color_continuous_scale="Plasma", 
            hover_name="ENTIDAD_FEDERATIVA",
            zoom=3,
            center={"lat": 23.6345, "lon": -102.5528},
            height=450,
        )
        fig_gen_covid.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_gen_covid, use_container_width=True)

    with col_mapa_h1n1:
        st.markdown("#### Mapa Influenza A(H1N1)")
        st.info("Espacio para el mapa de A(H1N1).")



    #  LÍNEA TEMPORAL_VISTA GENERAL 
st.markdown("#### Linea Temporal COVID-19 VS A(H1N1) ")
st.info("Espacio para la linea temporal de COVID-19 vs A(H1N1).")

     #  ENTIDADES MAS AFECTADAS_VISTA GENERAL 
st.markdown("#### Linea Temporal COVID-19 VS A(H1N1) ")
st.info("Espacio para graficos de las entidades mas afectadas de COVID-19 vs A(H1N1).")


# PESTAÑA: COVID-19 
with tab_covid:
    st.markdown("### Análisis de COVID-19")

    ano_covid = st.radio(
        "Selecciona el periodo temporal:",
        ["Suma de Casos", "1° Año", "2° Año", "3° Año"],
        horizontal=True,
        key="radio_covid"
    )

    if ano_covid == "Suma de Casos":
        df_mapa = (
            df.groupby(
                ["ENTIDAD_RES", "ENTIDAD_FEDERATIVA",
                 "LATITUD", "LONGITUD"]
            )["CASOS"]
            .sum()
            .reset_index()
        )
    else:
        mapa_anos = {
            "1° Año": 2020,
            "2° Año": 2021,
            "3° Año": 2022
        }
        anio_objetivo = mapa_anos[ano_covid]
        df_mapa = df[df["AÑO"] == anio_objetivo].copy()

    st.markdown("#### Mapa de Casos de COVID-19 por Entidad Federativa")
    fig = px.scatter_map(
        df_mapa,
        lat="LATITUD",
        lon="LONGITUD",
        size="CASOS",
        color="CASOS",
        color_continuous_scale="Plasma", 
        hover_name="ENTIDAD_FEDERATIVA",
        zoom=4,
        center={"lat": 23.6345, "lon": -102.5528},
        height=500,
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    #LÍNEA TEMPORAL
    st.markdown("#### Línea Temporal de Casos Activos")
    df_linea = df2.copy()
    if "FECHA_SINTOMAS" in df_linea.columns:
        df_linea["FECHA_SINTOMAS"] = pd.to_datetime(df_linea["FECHA_SINTOMAS"])
        
        if ano_covid != "Suma de Casos":
            anio_objetivo = mapa_anos[ano_covid]
            df_linea = df_linea[df_linea["FECHA_SINTOMAS"].dt.year == anio_objetivo]

        df_linea_agrupado = (
            df_linea.groupby("FECHA_SINTOMAS")["CASOS_ACTIVOS_ESTIMADOS_14D"]
            .sum()
            .reset_index()
            .sort_values("FECHA_SINTOMAS")
        )

        fig_linea = px.line(
            df_linea_agrupado,
            x="FECHA_SINTOMAS",
            y="CASOS_ACTIVOS_ESTIMADOS_14D",
            labels={"FECHA_SINTOMAS": "Fecha de Síntomas", "CASOS_ACTIVOS_ESTIMADOS_14D": "Casos Activos Estimados (14D)"},
            color_discrete_sequence=["#2563eb"],
        )
        fig_linea.update_layout(
            margin={"r": 0, "t": 10, "l": 0, "b": 0},
            height=350,
            xaxis_title="",
            yaxis_title="Casos Activos",
        )
        st.plotly_chart(fig_linea, use_container_width=True)
    else:
        st.warning("Verifica el nombre de la columna de fecha en 'casos_covid_activos.csv'.")



#ENTIDADES MAS AEFECTADAS
    st.markdown("#### Entidades más afectadas")
    df_entidades = (
        df_mapa.groupby("ENTIDAD_FEDERATIVA")["CASOS"]
        .sum()
        .reset_index()
        .sort_values(by="CASOS", ascending=False)
    )

    top_5 = df_entidades.head(5).copy()
    
    if len(df_entidades) > 5:
        otros_suma = df_entidades.iloc[5:]["CASOS"].sum()
        df_otros = pd.DataFrame({"ENTIDAD_FEDERATIVA": ["Otros"], "CASOS": [otros_suma]})
        df_pie = pd.concat([top_5, df_otros], ignore_index=True)
    else:
        df_pie = top_5.copy()

    col_bar, col_pie = st.columns(2)

    with col_bar:
        fig_bar = px.bar(
            top_5,
            x="ENTIDAD_FEDERATIVA",
            y="CASOS",
            text="CASOS",
            color="CASOS",
            color_continuous_scale="Plasma",
            labels={"ENTIDAD_FEDERATIVA": "Entidad", "CASOS": "Total de Casos"}
        )
        fig_bar.update_layout(
            xaxis_title="",
            yaxis_title="Casos",
            coloraxis_showscale=False,
            margin={"r":0, "t":20, "l":0, "b":0},
            height=400
        )
        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_pie:
        fig_pie = px.pie(
            df_pie,
            names="ENTIDAD_FEDERATIVA",
            values="CASOS",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig_pie.update_layout(
            margin={"r":0, "t":20, "l":0, "b":0},
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)


#PESTAÑA: H1N1
with tab_h1n1:
    st.markdown("### Análisis de A(H1N1)")
    ano_h1n1 = st.radio(
        "Selecciona el periodo temporal (H1N1):",
        ["Suma de Casos", "1er Año", "Segundo Año", "Tercer Año"],
        index=0,
        horizontal=True,
        key="radio_h1n1",
    )

    if ano_h1n1 == "Suma de Casos":
        st.info("Mostrando la **Suma Total de Casos** de H1N1.")
    elif ano_h1n1 == "1er Año":
        st.info("Mostrando datos del **Primer Año** de H1N1.")