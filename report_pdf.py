import streamlit as st
from streamlit_extras.grid import grid
from streamlit_option_menu import option_menu
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

import db
import db_2
import ingestion_gui
import Analysis_gui
import Prediction_gui
import model_gui

# Initialize databases
db.init_db()
db_2.init_db()

# Session state setup
if st.session_state.get('uploaded_file') is None:
    st.session_state['uploaded_file'] = None
if st.session_state.get('uploaded_file_name') is None:
    st.session_state['uploaded_file_name'] = None

# Streamlit config and styles
st.set_page_config(page_title="IDEAS Webapp", layout="wide")
st.markdown("""
    <style>
        .reportview-container { margin-top: -2em; }
        #MainMenu, footer, .stDeployButton, #stDecoration { display: none; visibility: hidden; }
        .block-container { padding: 1rem 5rem 0rem 5rem; }
    </style>
""", unsafe_allow_html=True)

# App header
my_grid = grid([4, 22, 5], [2, 5], 1, vertical_align="center")
my_grid.image('./IDEAS-TIH_new.jpg', width=200)
my_grid.markdown("<h1 style='text-align: center; color: black;'>Heart Murmur Detection System</h1><p style='text-align: center; color: black; font-size: 16px;'>Collaborative Project of IDEAS and CSI</p>", unsafe_allow_html=True)
my_grid.image('./CSI_new.jpg', width=200)

# Menu and layout
with my_grid.container(height=640, border=True):
    selected = option_menu(None, ["Ingestion", "Analysis", "Prediction", "Models"], icons=['database-add', 'bar-chart-steps', 'box'])

body = my_grid.container(height=640, border=True)

my_grid.markdown("<h2 style='text-align: center; color: black;'> &#169;IDEAS-TIH </h2>", unsafe_allow_html=True)


#-------------------------- 
#PDF GENERATORS BY SECTION 
#-------------------------- 
def generate_ingestion_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Ingestion Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "This section allows users to upload audio files for analysis.")
    c.drawString(50, height - 120, "Functionality:")
    c.drawString(70, height - 140, "- Upload local WAV files")
    c.drawString(70, height - 160, "- View metadata and description")
    c.drawString(70, height - 180, "- Save file to database")
    if st.session_state.get("uploaded_file_name"):
        c.drawString(50, height - 200, "Uploaded file:")
        c.drawString(70, height - 220, st.session_state["uploaded_file_name"])
    else:
        c.drawString(50, height - 200, "No file uploaded.")
    c.save()
    buffer.seek(0)
    return buffer

def generate_analysis_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "This section performs signal analysis on the uploaded audio files.")
    c.drawString(50, height - 120, "Functionality:")
    c.drawString(70, height - 140, "- Display waveform of the audio signal")
    c.drawString(70, height - 160, "- Show spectrogram and frequency content")
    c.drawString(70, height - 180, "- Highlight abnormalities in signal")
    c.save()
    buffer.seek(0)
    return buffer

def generate_prediction_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Prediction Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "This section uses machine learning models to predict the presence of heart murmurs.")
    c.drawString(50, height - 120, "Functionality:")
    c.drawString(70, height - 140, "- Load a trained ML model")
    c.drawString(70, height - 160, "- Predict presence of heart murmurs")
    c.drawString(70, height - 180, "- Display prediction results")
    c.save()
    buffer.seek(0)
    return buffer

def generate_model_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Modeling Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "This section trains machine learning models using audio features.")
    c.drawString(50, height - 120, "Functionality:")
    c.drawString(70, height - 140, "- Train on extracted features from heart audio")
    c.drawString(70, height - 160, "- Evaluate using accuracy, precision, recall")
    c.drawString(70, height - 180, "- Save trained models for reuse")
    c.save()
    buffer.seek(0)
    return buffer


# --------------------------
# MAIN APP LOGIC
# --------------------------

with body:
    if selected == "Ingestion":
        ingestion_gui.ingestion_gui()
        st.markdown("---")
        if st.button("Generate Ingestion PDF Report"):
            pdf_buffer = generate_ingestion_pdf()
            st.download_button("Download Ingestion Report", data=pdf_buffer, file_name="ingestion_report.pdf", mime="application/pdf")

    elif selected == "Analysis":
        Analysis_gui.Analysis_gui()
        st.markdown("---")
        if st.button("Generate Analysis PDF Report"):
            pdf_buffer = generate_analysis_pdf()
            st.download_button("Download Analysis Report", data=pdf_buffer, file_name="analysis_report.pdf", mime="application/pdf")

    elif selected == "Prediction":
        Prediction_gui.Prediction_gui()
        st.markdown("---")
        if st.button("Generate Prediction PDF Report"):
            pdf_buffer = generate_prediction_pdf()
            st.download_button("Download Prediction Report", data=pdf_buffer, file_name="prediction_report.pdf", mime="application/pdf")

    elif selected == "Models":
        model_gui.model_gui()
        st.markdown("---")
        if st.button("Generate Model PDF Report"):
            pdf_buffer = generate_model_pdf()
            st.download_button("Download Model Report", data=pdf_buffer, file_name="model_report.pdf", mime="application/pdf")