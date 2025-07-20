import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# 🔐 Alias del usuario
st.sidebar.title("👤 Usuario")
usuario = st.sidebar.text_input("Ingresa tu alias:", value="")

if usuario.strip() == "":
    st.warning("⚠️ Por favor, ingresa tu alias en la barra lateral para continuar.")
    st.stop()

# 📁 Inicializar historial global
if "historial" not in st.session_state:
    st.session_state.historial = {}

# 📂 Cargar historial desde CSV si existe
archivo_csv = f"{usuario}_historial.csv"
if usuario not in st.session_state.historial:
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        st.session_state.historial[usuario] = df.to_dict("records")
    else:
        st.session_state.historial[usuario] = []

# 🧮 Interfaz de cálculo
st.markdown("### 🧮 Calculadora Betmastian.p")
st.caption("Calcula el monto para cubrir la apuesta")

with st.form("form_apuesta"):
    col1, col2 = st.columns(2)
    with col1:
        monto_A = st.number_input("Monto (A)", min_value=0.0, format="%.2f", value=0.0)
        cuota_B = st.number_input("Cuota B", min_value=1.01, format="%.2f", value=3.0)
    with col2:
        cuota_A = st.number_input("Cuota A", min_value=1.01, format="%.2f", value=1.5)
        dolar_casino = st.text_input("💲 Precio Dólar Casino (opcional)", placeholder="Ej: 1200")

    calcular = st.form_submit_button("Calcular")

# 🧠 Lógica de cálculo
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

# 🎯 Mostrar resultados
if calcular:
    monto_B, inversion_total, ganancia_neta, gA, gB, rentabilidad = calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B)

    st.markdown("### 🎯 Resultados:")
    with st.container():
        st.markdown(f"**Apostar:** `${monto_B:,.2f}` a cuota B")
        st.markdown(f"💰 **Inversión total:** `${inversion_total:,.2f}`")
        st.markdown(f"📈 **Rentabilidad:** `{rentabilidad:.2f}%`")
        colA, colB = st.columns(2)
        with colA:
            st.success(f"✅ **Si gana A:** `${gA:,.2f}`")
        with colB:
            st.success(f"✅ **Si gana B:** `${gB:,.2f}`")

        marcar = st.checkbox("Marcar como apuesta realizada")
        if marcar:
            st.session_state.historial[usuario].append({
                "Monto A": monto_A,
                "Cuota A": cuota_A,
                "Cuota B": cuota_B,
                "Monto B": monto_B,
                "Inversión Total": inversion_total,
                "Ganancia neta": ganancia_neta,
                "Rentabilidad": rentabilidad
            })
            # Guardar historial en CSV
            df = pd.DataFrame(st.session_state.historial[usuario])
            df.to_csv(archivo_csv, index=False)
            st.success("✅ Apuesta guardada en tu historial")

# 📚 Mostrar historial del usuario actual
historial_usuario = st.session_state.historial.get(usuario, [])

if historial_usuario:
    st.markdown(f"### 📚 Historial de {usuario}")

    # 🔘 Opciones de gestión
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Borrar historial"):
            st.session_state.historial[usuario] = []
            if os.path.exists(archivo_csv):
                os.remove(archivo_csv)
            st.success("✅ Historial borrado correctamente.")
            st.experimental_rerun()

    with col2:
        df_export = pd.DataFrame(historial_usuario)
        st.download_button(
            label="📥 Exportar historial",
            data=df_export.to_csv(index=False).encode("utf-8"),
            file_name=f"{usuario}_historial.csv",
            mime="text/csv"
        )

    # Mostrar apuestas
    for idx, item in enumerate(historial_usuario[::-1], 1):
        with st.expander(f"Apuesta #{len(historial_usuario) - idx + 1}"):
            st.write(f"🟢 Monto A: ${item['Monto A']:,.2f}")
            st.write(f"🔵 Cuota A: {item['Cuota A']}")
            st.write(f"🔴 Cuota B: {item['Cuota B']}")
            st.write(f"🟡 Monto B: ${item['Monto B']:,.2f}")
            st.write(f"💰 Inversión Total: ${item['Inversión Total']:,.2f}")
            st.write(f"📈 Rentabilidad: {item['Rentabilidad']:.2f}%")
            st.write(f"💵 Ganancia Neta: ${item['Ganancia neta']:,.2f}")
else:
    st.info("ℹ️ Aún no hay historial registrado para este usuario.")
