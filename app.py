import streamlit as st
from decimal import Decimal, InvalidOperation

# Configuración de la página
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

# Función para convertir texto a float (acepta , o .)
def to_float(s: str, allow_zero=False):
    s = (s or "").strip().replace(",", ".")
    try:
        x = float(Decimal(s))
        if not allow_zero and x == 0.0:
            return None
        return x
    except (InvalidOperation, ValueError):
        return None

# Título
st.markdown("## 🧮 Calculadora Betmastian.p")
st.caption("Calcula el monto para cubrir la apuesta")

# Formulario
with st.form("form_apuesta"):
    col1, col2 = st.columns(2)
    with col1:
        monto_A_str = st.text_input("Monto (A)", value="0.00", placeholder="Ej: 1000,50")
        cuota_B_str = st.text_input("Cuota B", value="3.00", placeholder="Ej: 2.35")
    with col2:
        cuota_A_str = st.text_input("Cuota A", value="1.50", placeholder="Ej: 1.80")
        dolar_casino_str = st.text_input("💲 Precio Dólar Casino (opcional)", placeholder="Ej: 1200,00")

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
    porcentaje_ganancia = (ganancia_neta / inversion_total) * 100 if inversion_total else 0.0
    return monto_B, inversion_total, ganancia_neta, ganancia_neta_A, ganancia_neta_B, porcentaje_ganancia

# Mostrar resultados
if calcular:
    monto_A = to_float(monto_A_str)
    cuota_A = to_float(cuota_A_str, allow_zero=False)
    cuota_B = to_float(cuota_B_str, allow_zero=False)
    dolar_casino = to_float(dolar_casino_str, allow_zero=True) if dolar_casino_str else None

    errores = []
    if monto_A is None or monto_A <= 0:
        errores.append("⚠️ El monto debe ser un número válido > 0.")
    if cuota_A is None or cuota_A <= 1.0:
        errores.append("⚠️ La **Cuota A** debe ser un número > 1.00.")
    if cuota_B is None or cuota_B <= 1.0:
        errores.append("⚠️ La **Cuota B** debe ser un número > 1.00.")

    if errores:
        for e in errores:
            st.error(e)
    else:
        monto_B, inversion_total, ganancia_neta, gA, gB, rentabilidad = calcular_apuesta_opuesta(
            cuota_A, monto_A, cuota_B
        )

        # Estilo según rentabilidad
        color = "#00c17d" if rentabilidad > 0 else ("#ff4d4d" if rentabilidad < 0 else "#ffd700")
        if rentabilidad > 0:
            tag = f"📈 Rentabilidad +{rentabilidad:.2f}%"
            pierde_gana = f"🟢 Gana: <strong>${ganancia_neta:,.2f}</strong>"
        elif rentabilidad < 0:
            tag = f"🔻 Pérdida {abs(rentabilidad):.2f}%"
            pierde_gana = f"🔴 Pierde: <strong>${abs(ganancia_neta):,.2f}</strong>"
        else:
            tag = "🟡 Sin ganancia / pérdida"
            pierde_gana = "🟡 Resultado neutro: <strong>$0.00</strong>"

        # Mostrar resultados con estilo
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

