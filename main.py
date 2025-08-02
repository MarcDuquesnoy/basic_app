import streamlit as st
from utils import *

st.set_page_config(page_title="Page principale", page_icon="👋")
st.title("Bienvenue sur BasicApp Performances 👋")
st.markdown("""Renseigne tes dernières séances de musculation.""")
st.markdown("#")

st.set_page_config(layout="wide")

date, exercices, stretch, series = selector()
body_id = list_body()

st.markdown("#")
st.markdown("#")
for i in range(1, series + 1):

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.session_state['A'+str(i)] = st.selectbox("Exercice n°" + str(i), body_id)
    with col2:
        st.session_state['B'+str(i)] = st.slider("Séries n°" + str(i), 1, 10)
    with col3:
        st.session_state['C'+str(i)] = st.text_input("Poids n°" + str(i))
    with col5:
        st.session_state['E' + str(i)] = st.text_input("Répétition n°" + str(i))
    with col4:
        st.session_state['D'+str(i)] = st.text_input("Commentaire n°" + str(i))


if st.button("Validation"):

    import_training(date=date, exercices=exercices, stretch=stretch)

    import_series(series=series)

    # st.switch_page("pages/general.py")