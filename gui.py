import streamlit as st
import pandas as pd
import numpy as np

st.text_input('Your name', key='name')

# Access the value at any point with:
print(st.session_state.name)
