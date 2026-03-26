import streamlit as st
from supabase import create_client

# Configuración de la interfaz
st.set_page_config(page_title="Control de Tienda", page_icon="💰")
st.title("Gestión de Ingresos y Egresos")

# Aquí conectarás tus llaves de Supabase (Paso 2 anterior)
url = "TU_URL_DE_SUPABASE"
key = "TU_API_KEY_ANON"
supabase = create_client(url, key)

# --- FORMULARIO DE REGISTRO ---
with st.expander("➕ Registrar Nuevo Movimiento", expanded=True):
    tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
    monto = st.number_input("Monto (Bs.)", min_value=0.0, step=10.0)
    categoria = st.text_input("Categoría (Ventas, Alquiler, Repuestos, etc.)")
    descripcion = st.text_area("Notas adicionales")
    
    if st.button("Guardar en la Nube"):
        data = {
            "tipo": tipo,
            "monto": monto,
            "categoria": categoria,
            "descripcion": descripcion
        }
        supabase.table("movimientos").insert(data).execute()
        st.success("¡Datos sincronizados!")
        st.rerun()

# --- BALANCE EN TIEMPO REAL ---
st.divider()
st.subheader("Resumen de Caja")
res = supabase.table("movimientos").select("*").execute()
datos = res.data

if datos:
    total_ingresos = sum(d['monto'] for d in datos if d['tipo'] == 'Ingreso')
    total_egresos = sum(d['monto'] for d in datos if d['tipo'] == 'Egreso')
    saldo = total_ingresos - total_egresos
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"{total_ingresos} Bs")
    col2.metric("Egresos", f"-{total_egresos} Bs", delta_color="inverse")
    col3.metric("Saldo Actual", f"{saldo} Bs")
    
    st.write("### Historial Reciente")
    st.dataframe(datos)
else:
    st.info("Aún no hay movimientos registrados.")