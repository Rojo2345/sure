# app.py
import streamlit as st

def calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B):
    monto_B = (cuota_A * monto_A) / cuota_B
    inversion_total = monto_A + monto_B
    ganancia_A = cuota_A * monto_A
    ganancia_neta_A = ganancia_A - inversion_total
    ganancia_B = cuota_B * monto_B
    ganancia_neta_B = ganancia_B - inversion_total
    ganancia_neta = min(ganancia_neta_A, ganancia_neta_B)
    porcentaje_ganancia = (ganancia_neta / inversion_total) * 100

    st.subheader("Resumen General")
    st.write(f"Apostar en A: ${monto_A:.2f}")
    st.write(f"Apostar en B: ${monto_B:.2f}")
    st.write(f"Inversión total: ${inversion_total:.2f}")
    st.write(f"Ganancia neta asegurada: ${ganancia_neta:.2f}")
    st.write(f"Ganancia si sale A: ${ganancia_neta_A:.2f}")
    st.write(f"Ganancia si sale B: ${ganancia_neta_B:.2f}")
    st.write(f"Rentabilidad: {porcentaje_ganancia:.2f}%")

st.title("Calculadora de Apuesta Opuesta")
cuota_A = st.number_input("Cuota A", min_value=1.0)
monto_A = st.number_input("Monto en A", min_value=0.0)
cuota_B = st.number_input("Cuota B", min_value=1.0)

if st.button("Calcular"):
    calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B)
