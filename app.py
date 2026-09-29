import time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
st.set_page_config(
    page_title="Simulador de Oscilaciones", layout="centered"
)
st.title("Simulador de Oscilaciones")
st.write(
    "Ajusta los parámetros con los controles de la izquierda y haz clic en"
    " **Play**."
)
st.sidebar.header("Parámetros")
A = st.sidebar.slider("Amplitud (m)", 10, 60, 30, 1)
omega = st.sidebar.slider("Frecuencia angular", 0.1, 10.0, 1.0, 0.1)
phi = st.sidebar.slider("Desfase", -3.14, 3.14, 0.0, 0.1)

try:
  canon = Image.open("cañon.png")
  fondo = Image.open("fondo.jpg")
  bola = Image.open("bola.png")
  soporte = Image.open("soporte.png")
except FileNotFoundError as e:
  st.error(f"Falta una imagen en la carpeta: {e}")
  st.stop()
col1, col2 = st.sidebar.columns(2)
play = col1.button("Play")
if "animando" not in st.session_state:
  st.session_state.animando = False
if play:
  st.session_state.animando = True
contenedor_grafico = st.empty()
def generar_escenario(
    x_anim=None, y_anim=None, mostrar_bola_en_vuelo=False, frame_actual=0
):
  fig, axis = plt.subplots(figsize=(8, 4.5))
  fig.patch.set_facecolor("#1e1e1e")
  axis.set_facecolor("#1e1e1e")
  axis.tick_params(colors="white", which="both")
  for spine in axis.spines.values():
    spine.set_edgecolor("white")
  axis.set_xlim([0, 500])
  axis.set_ylim([0, 280])
  axis.imshow(fondo, extent=[0, 70, 0, 40], zorder=0)
  if mostrar_bola_en_vuelo and x_anim is not None:
    axis.imshow(
        bola,
        extent=[
            x_anim[frame_actual] - 6,
            x_anim[frame_actual] + 6,
        ],
        zorder=9,
    )
  return fig
if st.session_state.animando:
  rad = np.pi / 180 * phi
  t_max = 2*np.pi/omega
  t = np.linspace(0, t_max, 30)
  x_trayectoria = A*np.cos(omega*t+phi)
  for i in range(1, len(x_trayectoria)):
    fig = generar_escenario(
        x_trayectoria, mostrar_bola_en_vuelo=True, frame_actual=i
    )
    contenedor_grafico.pyplot(fig)
    plt.close(fig)
    time.sleep(0.01)
else:
  fig = generar_escenario()
  contenedor_grafico.pyplot(fig)
  plt.close(fig)
