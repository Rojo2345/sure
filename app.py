import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# Estilo personalizado
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
    monto_B, inversion_total, ganancia_neta, gA, gB, rentabilidad = calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B)

    # Color según rentabilidad
    if rentabilidad > 0:
        rent_color = "#00c17d"
        rent_text = f"📈 Ganancia +{rentabilidad:.2f}%"
        resultado_texto = f"🟢 Gana: <strong>${ganancia_neta:,.2f}</strong>"
    elif rentabilidad < 0:
        rent_color = "#ff4d4d"
        rent_text = f"🔻 Pérdida {abs(rentabilidad):.2f}%"
        resultado_texto = f"🔴 Pierde: <strong>${abs(ganancia_neta):,.2f}</strong>"
    else:
        rent_color = "#ffd700"
        rent_text = "🟡 Sin ganancia / pérdida"
        resultado_texto = "🟡 Resultado neutro: <strong>$0.00</strong>"

    # Mostrar en la interfaz
    st.markdown(f"""
    <div class="result-box">
        <h4>📊 <strong>Resultados:</strong></h4>
        <p>Apostar: <span class="highlight">${monto_B:,.2f}</span> a cuota B</p>
        <p>💰 Inversión total: <span class="highlight">${inversion_total:,.2f}</span></p>

        <p style="background-color: {rent_color};
                  color: black;
                  display: inline-block;
                  padding: 0.4em 0.8em;
                  border-radius: 5px;
                  margin: 0.5em 0;
                  font-weight: bold;">
            {rent_text}
        </p>

        <div class="profit-box">✅ Si gana A: ${gA:,.2f}</div>
        <div class="profit-box">✅ Si gana B: ${gB:,.2f}</div>

        <div style="margin-top: 0.7em; font-size: 1.1em;">
            {resultado_texto}
        </div>
    </div>
    """, unsafe_allow_html=True)
