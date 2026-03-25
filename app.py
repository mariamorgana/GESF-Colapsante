import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="GESF Colapsante", layout="wide")

# Tente carregar seu arquivo real, se não existir, usa dados de exemplo
try:
    df = pd.read_csv("dados.csv")
    st.success("Dados carregados com sucesso!")
except:
    st.warning("Aguardando arquivo 'dados.csv'. Mostrando exemplo...")
    # Dados fictícios para teste inicial
    df = pd.DataFrame({
        'PROC': ['São Paulo', 'Rio', 'Salvador'],
        'lat': [-23.55, -22.90, -12.97],
        'lon': [-46.63, -43.17, -38.50],
        'casos': [50, 30, 20],
        'creat': [1.2, 1.5, 1.1]
    })

st.title("📊 Estatísticas de Procedência")

# Mapa proporcional
map_data = df.groupby(['PROC', 'lat', 'lon']).size().reset_index(name='casos')
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(latitude=-15, longitude=-50, zoom=3),
    layers=[pdk.Layer("ScatterplotLayer", map_data, get_position='[lon, lat]', 
            get_radius='casos * 5000', get_color='[200, 30, 0, 160]', pickable=True)],
    tooltip={"text": "{PROC}: {casos} casos"}
))

st.write("### Resumo dos Dados", df.describe())
