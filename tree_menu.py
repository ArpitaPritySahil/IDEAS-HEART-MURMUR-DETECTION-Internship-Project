import streamlit_extras
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

import tempfile
import os
from urllib.parse import urlparse
import io

import db
import db_2
import ingestion_gui
import Analysis_gui
import Prediction_gui
import model_gui

db.init_db() #Create the tables and sequences in DuckDB if not present
db_2.init_db()

uploaded_file="wav"

# Initialize session state variables
if st.session_state.get('uploaded_file') is None:
    st.session_state['uploaded_file'] = None
    print("Setting st.session_state['uploaded_file'] to None")

if st.session_state.get('uploaded_file_name') is None:
    st.session_state['uploaded_file_name'] = None

st.set_page_config(page_title="IDEAS Webapp", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

my_grid = grid([4,22,5], [2,5],1, vertical_align="center")

my_grid.image('./IDEAS-TIH_new.jpg', width=200)
my_grid.markdown("<h1 style='text-align: center; color: black;'>Heart Murmur Detection System</h1> <p style='text-align: center; color: black; font-size: 16px;'>Collaborative Project of IDEAS and CSI</p>", unsafe_allow_html=True)
my_grid.image('./CSI_new.jpg',width=200)

# Define the tree menu structure
menu = {
    'Home': {},
    'Ingestion ': {
        'Upload Data ': {}
    },
    'Analysis ': {
        'Data Visualization ': {}
    },
    'Prediction ': {
        'Model Training ': {}
    },
    'Models ': {
        'Model 1 ': {}
    }
}

# Create the tree menu
def tree_menu(options):
    for label, children in options.items():
        if children:
            expander = st.expander(label)
            with expander:
                tree_menu(children)
        else:
            if st.checkbox(label):
                if label == 'Upload Data ':
                    with my_grid.container(height=640, border=True):  
                        ingestion_gui.ingestion_gui()
                elif label == 'Data Visualization ':
                    with my_grid.container(height=640, border=True):  
                        Analysis_gui.Analysis_gui()
                elif label == 'Model Training ':
                    with my_grid.container(height=640, border=True):  
                        Prediction_gui.Prediction_gui()
                elif label == 'Model 1 ':
                    with my_grid.container(height=640, border=True):  
                        model_gui.model_gui()

with my_grid.container(height=640, border=True):  #Menu
    tree_menu(menu)

my_grid.markdown("<h2 style='text-align: center; color: black;'> &#169;IDEAS-TIH </h2>", unsafe_allow_html=True)  #&#169; HTML code for copyright emoji