import streamlit as st
from aise_toolkit_demo.app import app_utiles
import aise_toolkit_demo.utils as utils

st.write(f"Hello world {utils.calculate()}")
st.write(f"Hello world {utils.get_message()}")
st.write(f"Hello world {app_utiles.app_calculate()}")