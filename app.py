import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Planograma Visual")

st.title("📦 Visualizador de Gôndola e Planograma")

# Carrega a base atualizada em cache para maior velocidade
@st.cache_data
def carregar_dados():
    df = pd.read_csv("bi_produtos_atualizado.csv")
    # Mantém apenas os produtos que possuem o link da foto
    return df.dropna(subset=['Foto Produto'])

df = carregar_dados()

# Filtros laterais para escolher a visualização
st.sidebar.header("Filtros de Gôndola")
categorias = df['Categorias'].dropna().unique()
categoria_selecionada = st.sidebar.selectbox("Selecione a Categoria:", categorias)

# Filtra a base pela categoria escolhida
df_gondola = df[df['Categorias'] == categoria_selecionada]

st.markdown(f"### Prateleira: {categoria_selecionada}")
st.divider()

# Simulação da prateleira organizando os produtos lado a lado
if not df_gondola.empty:
    # Cria uma coluna do Streamlit para cada produto renderizado
    colunas = st.columns(len(df_gondola))
    
    for index, (col, row) in enumerate(zip(colunas, df_gondola.iterrows())):
        produto = row[1]
        with col:
            # Renderiza a imagem nativamente usando a URL extraída
            st.image(produto['Foto Produto'], use_container_width=True)
            # Legendas com a descrição e medidas
            st.markdown(f"**{produto['Largura']}cm (L)** x {produto['Altura']}cm (A)")
            st.caption(f"{produto['Descricao'][:25]}")
else:
    st.warning("Nenhum produto com imagem encontrada para esta categoria.")
