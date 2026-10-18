import time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Simulador de Oscilaciones", layout="centered"
)
st.title("Simulador de Oscilaciones con Resorte y Bloque")
st.write(
    "Ajusta los parámetros con los controles de la izquierda y haz clic en"
    " **Play**."
)

st.sidebar.header("Parámetros")
A = st.sidebar.slider("Amplitud (m)", 10, 100, 40, 1)
omega = st.sidebar.slider("Frecuencia angular", 0.1, 10.0, 2.0, 0.1)
phi = st.sidebar.slider("Desfase (rad)", -3.14, 3.14, 0.0, 0.1)

@st.cache_data
def cargar_imagenes():
    try:
        bloque = Image.open("bloque.png")
        resorte = Image.open("resorte.png")
        fondo = Image.open("fondo.jpg")
        return bloque, resorte, fondo
    except FileNotFoundError as e:
        return None, None, None

bloque, resorte, fondo = cargar_imagenes()
if bloque is None or resorte is None or fondo is None:
    st.error("Faltan algunas imágenes en la carpeta ('bloque.png', 'resorte.png' o 'fondo.jpg').")
    st.stop()

col1, col2 = st.sidebar.columns(2)
play = col1.button("Play")
reiniciar = col2.button("Reiniciar")

if "animando_osc" not in st.session_state:
    st.session_state.animando_osc = False

if reiniciar:
    st.session_state.animando_osc = False
    st.rerun()

if play:
    st.session_state.animando_osc = True

contenedor_grafico = st.empty()

def crear_figura_base():
    fig, axis = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#1e1e1e")
    axis.set_facecolor("#1e1e1e")
    axis.tick_params(colors="white", which="both")
    for spine in axis.spines.values():
        spine.set_edgecolor("white")
        
    axis.set_xlim([0, 500])
    axis.set_ylim([0, 280])
    
    axis.imshow(fondo, extent=[0, 500, 0, 280], zorder=0)
    
    axis.fill_between([0, 500], 0, 110, color="olivedrab", zorder=1)
    axis.axhline(y=110, color="dimgray", linestyle="-", linewidth=2, zorder=2)
    
    resorte_im = axis.imshow(resorte, extent=[0, 150, 120, 150], zorder=3)
    bloque_im = axis.imshow(bloque, extent=[130, 190, 110, 165], zorder=4)
    
    return fig, axis, resorte_im, bloque_im

fig, axis, resorte_im, bloque_im = crear_figura_base()

x_pared = 0
y_centro = 137

if st.session_state.animando_osc:
    t_max = 4 * np.pi / omega
    t = np.linspace(0, t_max, 80)
    
    x_desplazamiento = A * np.cos(omega * t + phi)
    x_bloque_centro = 250 + x_desplazamiento
    
    contenedor_grafico.pyplot(fig)
    
    for i in range(1, len(x_bloque_centro)):
        xb = x_bloque_centro[i]
        
        bloque_im.set_extent([xb - 30, xb + 30, y_centro - 27, y_centro + 28])
        resorte_im.set_extent([x_pared, xb - 25, y_centro - 12, y_centro + 12])
        
        contenedor_grafico.pyplot(fig)
        time.sleep(0.02)
        
    st.session_state.animando_osc = False
    plt.close(fig)
else:
    bloque_im.set_extent([250 - 30, 250 + 30, y_centro - 27, y_centro + 28])
    resorte_im.set_extent([x_pared, 250 - 25, y_centro - 12, y_centro + 12])
    contenedor_grafico.pyplot(fig)
    plt.close(fig)
