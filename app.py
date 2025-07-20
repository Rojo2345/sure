import streamlit as st

# Configurar página
st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# Alternar modo desde la barra lateral
if "modo_claro" not in st.session_state:
    st.session_state.modo_claro = False

modo_actual = st.sidebar.checkbox("🔆 Modo claro", value=st.session_state.modo_claro)

if modo_actual != st.session_state.modo_claro:
    st.session_state.modo_claro = modo_actual
    st.rerun()  # 👈 Forzar recarga de estilos

modo_claro = st.session_state.modo_claro

# Colores según modo
if modo_claro:
    fondo = "#f4f4f4"
    texto = "#000000"
    fondo_resultado = "#ffffff"
    borde = "#cccccc"
    color_etiqueta = "#333333"
else:
    fondo = "#0f1117"
    texto = "#ffffff"
    fondo_resultado = "#2c2f36"
    borde = "#444444"
    color_etiqueta = "#00ffae"

# Estilos CSS aplicados dinámicamente
st.markdown(f"""
    <style>
    body {{
        background-color: {fondo};
        color: {texto};
    }}
    .main {{
        background-color: {fondo};
        color: {texto};
    }}
    .result-box {{
        background-color: {fondo_resultado};
        padding: 1.2em;
        border-radius: 10px;
        color: {texto};
        margin-top: 1em;
        border: 1px solid {borde};
    }}
    .highlight {{
        font-size: 1.2em;
        font-weight: bold;
        color: {color_etiqueta};
    }}
    .profit-box {{
        background-color: #1e442f;
        color: white;
        padding: 0.5em;
        border-radius: 8px;
        text-align: center;
        margin-top: 0.4em;
    }}
    .stButton>button {{
        background-color: #2e64fe;
        color: white;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)
# Configuración
st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# Estilos personalizados
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
        color: white;
    }
    .main {
        background-color: #0f1117;
        color: white;
    }
    .result-box {
        background-color: #2c2f36;
        padding: 1.2em;
        border-radius: 10px;
        color: white;
        margin-top: 1em;
        border: 1px solid #444;
    }
    .highlight {
        font-size: 1.2em;
        font-weight: bold;
        color: #00ffae;
    }
    .profit-box {
        background-color: #1e442f;
        color: white;
        padding: 0.5em;
        border-radius: 8px;
        text-align: center;
        margin-top: 0.4em;
    }
    .stButton>button {
        background-color: #2e64fe;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("## 🧮 Calculadora Betmastian.p")
st.caption("Calcula el monto para cubrir la apuesta")

# Formulario
with st.form("form_apuesta"):
    col1, col2 = st.columns(2)
    with col1:
        monto_A = st.number_input("Monto (A)", min_value=0.0, format="%.2f", value=0.0)
        cuota_B = st.number_input("Cuota B", min_value=1.01, format="%.2f", value=3.0)
    with col2:
        cuota_A = st.number_input("Cuota A", min_value=1.01, format="%.2f", value=1.5)
        dolar_casino = st.text_input("💲 Precio Dólar Casino (opcional)", placeholder="Ej: 1200")

    calcular = st.form_submit_button("Calcular")

# Función de cálculo
def calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B):
    monto_B = (cuota_A * monto_A) / cuota_B
    inversion_total = monto_A + monto_B
    ganancia_A = cuota_A * monto_A
    ganancia_neta_A = ganancia_A - inversion_total
    ganancia_B = cuota_B * monto_B
    ganancia_neta_B = ganancia_B - inversion_total
    ganancia_neta = min(ganancia_neta_A, ganancia_neta_B)
    porcentaje_ganancia = (ganancia_neta / inversion_total) * 100
    return monto_B, inversion_total, ganancia_neta, ganancia_neta_A, ganancia_neta_B, porcentaje_ganancia

# Mostrar resultados
if calcular:
    # 🔴 Manejo de errores
    if monto_A == 0:
        st.error("⚠️ El monto debe ser mayor que cero.")
    elif cuota_A <= 1.0 or cuota_B <= 1.0:
        st.error("⚠️ Las cuotas deben ser mayores a 1.00.")
    else:
        monto_B, inversion_total, ganancia_neta, gA, gB, rentabilidad = calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B)

        # Estilo rentabilidad
        if rentabilidad > 0:
            color = "#00c17d"
            tag = f"📈 Rentabilidad +{rentabilidad:.2f}%"
            pierde_gana = f"🟢 Gana: <strong>${ganancia_neta:,.2f}</strong>"
        elif rentabilidad < 0:
            color = "#ff4d4d"
            tag = f"🔻 Pérdida {abs(rentabilidad):.2f}%"
            pierde_gana = f"🔴 Pierde: <strong>${abs(ganancia_neta):,.2f}</strong>"
        else:
            color = "#ffd700"
            tag = "🟡 Sin ganancia / pérdida"
            pierde_gana = "🟡 Resultado neutro: <strong>$0.00</strong>"

        # Mostrar resultados
        st.markdown(f"""
        <div class="result-box">
            <h4>📊 <strong>Resultados:</strong></h4>
            <p>Apostar: <span class="highlight">${monto_B:,.2f}</span> a cuota B</p>
            <p>💰 Inversión total: <span class="highlight">${inversion_total:,.2f}</span></p>
            <p style="background-color: {color};
                      color: black;
                      display: inline-block;
                      padding: 0.4em 0.8em;
                      border-radius: 5px;
                      margin: 0.5em 0;
                      font-weight: bold;">
                {tag}
            </p>
            <div class="profit-box">✅ Si gana A: ${gA:,.2f}</div>
            <div class="profit-box">✅ Si gana B: ${gB:,.2f}</div>
            <div style="margin-top: 0.7em; font-size: 1.1em;">
                {pierde_gana}
            </div>
        </div>
        """, unsafe_allow_html=True)
