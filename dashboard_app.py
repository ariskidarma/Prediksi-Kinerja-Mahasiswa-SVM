import streamlit as st
import altair as alt
import main_dash
import prediksi_dash
# import layout_style_ex

st.set_page_config(
        page_title="Prediksi Kinerja Mahasiswa Berdasarkan Faktor Afektif Pada HSS Learning Menggunakan Metode Support Vector Machine",
        layout='wide'  # Halaman streamlit dipaksa untuk menggunakan wide mode
)

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
brush = alt.selection_interval()  
nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['x'], empty='none')

lang = st.sidebar.radio("Pilih bahasa / Select language:", ('Indonesia', 'English'))

page_names_to_funcs = {
    "Hasil Penelitian" if lang == "Indonesia" else "Research Results": main_dash.main_page,
    "Prediksi Kinerja Mahasiswa" if lang == "Indonesia" else "Student Performance Prediction": prediksi_dash.prediksi_page
}

selected_page = st.sidebar.selectbox("Pilih halaman" if lang == "Indonesia" else "Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page](lang)

