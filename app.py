import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

st.set_page_config(page_title="Dashboard Clínico", layout="wide")

@st.cache_data
def load_data():
    # Carrega seu arquivo 'dados.csv' do GitHub
    df = pd.read_csv("dados.csv")
    return df

try:
    df = load_data()
    st.title("🏥 GESF Colpasante")

    # --- SIDEBAR: FILTROS ---
    st.sidebar.header("Filtros Gerais")
    sexo_filtro = st.sidebar.multiselect("Filtrar por Sexo", options=df['SEXO'].unique(), default=df['SEXO'].unique())
    df_filtrado = df[df['SEXO'].isin(sexo_filtro)]

    # --- SEÇÃO 1: MAPA E APOL1 ---
    col_mapa, col_apol = st.columns([2, 1])

    with col_mapa:
        st.subheader("📍 Casos por Cidade")
        map_df = df_filtrado.groupby(['PROC', 'lat', 'lon']).size().reset_index(name='casos')
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(), zoom=4),
            layers=[pdk.Layer(
                "ScatterplotLayer", map_df, get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]', get_radius='casos * 5000', pickable=True
            )],
            tooltip={"text": "{PROC}: {casos} casos"}
        ))

    with col_apol:
        st.subheader("🧬 Distribuição APOL1")
        # Gráfico de barras para as categorias de APOL1
        fig_apol = px.bar(
            df_filtrado['APOL1'].value_counts().reset_index(),
            x='APOL1', 
            y='count',
            labels={'APOL1': 'Categoria', 'count': 'Frequência'},
            color='APOL1',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_apol, use_container_width=True)

    st.divider()

    # --- SEÇÃO 2: BOXPLOTS (VARIÁVEIS NUMÉRICAS) ---
    st.subheader("📊 Boxplots: Distribuição por Variável")
    
    # Seleção múltipla para comparar variáveis
    var_numerica = st.selectbox("Escolha a variável numérica para o Boxplot:", ['IDADE', 'CREAT', 'P24H', 'IFTA'])
    
    # Criando o Boxplot interativo
    fig_box = px.box(
        df_filtrado, 
        x='APOL1', # Compara a variável numérica entre as categorias de APOL1
        y=var_numerica, 
        color='APOL1',
        points="all", 
        title=f"Distribuição de {var_numerica.upper()} por categoria de APOL1",
        notched=True # Ajuda a visualizar a diferença estatística entre as medianas
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # --- SEÇÃO 3: OUTROS FATORES ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.write("**HBS (Fator)**")
        st.bar_chart(df_filtrado['HBS'].value_counts())
    with c2:
        st.write("**IRA (Fator)**")
        st.bar_chart(df_filtrado['IRA'].value_counts())

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")

