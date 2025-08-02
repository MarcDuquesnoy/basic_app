from logging import basicConfig

import streamlit as st
from utils import *

st.set_page_config(page_title="Général", page_icon="👋")
st.title("Résultats au global des séances 👋")
st.markdown("#")

st.set_page_config(layout="wide")

basic_results()