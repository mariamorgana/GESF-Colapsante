import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Mapa de Procedência", layout="wide")

@st.cache_data
def load_excel():
    # Carrega o arquivo Excel (certifique-se de que o nome coincida com o arquivo no GitHub)
    df = pd.read_excel("dados.xlsx", engine='openpyxl')
    # Padroniza nomes das colunas para minúsculo e remove espaços
    df.columns = df.columns.str.strip().str.lower()
    return df

try:
    df = load_excel()
    st.title("📍 Mapa de Procedência por Cidade")

    # 1. Agrupar dados para contar casos por cidade e coordenada
    # O código assume que as colunas no Excel se chamam: proc, lat, lon
    map_df = df.groupby(['proc', 'lat', 'lon']).size().reset_index(name='casos')

    # 2. Configurar a visualização do Mapa
    view_state = pdk.ViewState(
        latitude=map_df['lat'].mean(),
        longitude=map_df['lon'].mean(),
        zoom=4,
        pitch=0
    )

    # 3. Criar a camada de círculos proporcionais
    layer = pdk.Layer(
        "ScatterplotLayer",
        map_df,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]', # Cor vermelha com transparência
        get_radius='casos * 3000',     # Ajuste este multiplicador para o tamanho das bolas
        pickable=True,
    )

    # 4. Renderizar o Mapa
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{proc}\nCasos: {casos}"}
    ))

    st.write(f"Exibindo dados de **{len(df)}** registros em **{len(map_df)}** cidades.")

except Exception as e:
    st.error(f"Erro ao ler o arquivo Excel: {e}")
    st.info("Dica: Verifique se o arquivo se chama 'dados.xlsx' e se as colunas 'proc', 'lat' e 'lon' existem.")


