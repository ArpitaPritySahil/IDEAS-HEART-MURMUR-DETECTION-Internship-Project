import streamlit_extras
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

import tempfile
import os

import db
import db_2
import ingestion_gui
import Analysis_gui
import Prediction_gui
import model_gui
import predefined_pdf 

# DB setup
db.init_db()
db_2.init_db()

# Set uploaded file default
if st.session_state.get('uploaded_file') is None:
    st.session_state['uploaded_file'] = None
if st.session_state.get('uploaded_file_name') is None:
    st.session_state['uploaded_file_name'] = None

# Streamlit UI setup
st.set_page_config(page_title="IDEAS Webapp", layout="wide")

# Custom styles
st.markdown("""
    <style>
        .reportview-container { margin-top: -2em; }
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

# Header
my_grid = grid([4, 22, 5], [2, 5], 1, vertical_align="center")
my_grid.image('./IDEAS-TIH_new.jpg', width=200)
my_grid.markdown("<h1 style='text-align: center; color: black;'>Heart Murmur Detection System</h1> <p style='text-align: center; color: black; font-size: 16px;'>Collaborative Project of IDEAS and CSI</p>", unsafe_allow_html=True)
my_grid.image('./CSI_new.jpg', width=200)

# Navigation Menu
with my_grid.container(height=640, border=True):
    selected = option_menu(None, ["Ingestion", "Analysis", "Prediction", "Models", "Report"],
                           icons=['database-add', 'bar-chart-steps', 'box', 'kanban', 'file-earmark-pdf'])

# Main Body
body = my_grid.container(height=640, border=True)

# Footer
my_grid.markdown("<h2 style='text-align: center; color: black;'> &#169;IDEAS-TIH </h2>", unsafe_allow_html=True)

# Section Routing
with body:
    if selected == "Ingestion":
        ingestion_gui.ingestion_gui()

    elif selected == "Analysis":
        Analysis_gui.Analysis_gui()

    elif selected == "Prediction":
        Prediction_gui.Prediction_gui()

    elif selected == "Models":
        model_gui.model_gui()

    elif selected == "Report":
        st.markdown("### Report Generation")
        st.markdown("#### Select a section to download its report:")
            
        predefined_pdfs = {
                    "Ingestion": "static_reports/ingestion_report.pdf",
                    "Analysis": "static_reports/analysis_report.pdf",
                    "Prediction": "static_reports/prediction_report.pdf",
                    "Model": "static_reports/model_report.pdf",
                    "Overview": "static_reports/overview_report.pdf"
                          }

        selected_report = st.selectbox("Choose Report", list(predefined_pdfs.keys()))

    # Ingestion PDF generator
        def generate_ingestion_report():
                from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                import matplotlib.pyplot as plt
                import pandas as pd

                os.makedirs("static_reports", exist_ok=True)
                chart_path = "static_reports/sample_ingestion_chart.png"

                # Generate a sample chart
                df = pd.DataFrame({
                    'Feature': ['Age', 'Heart Rate', 'Blood Pressure', 'Oxygen Level'],
                    'Average': [29, 78, 120, 96]
                })
                plt.figure(figsize=(6, 4))
                plt.bar(df['Feature'], df['Average'], color='skyblue')
                plt.title('Feature Averages')
                plt.ylabel('Value')
                plt.tight_layout()
                plt.savefig(chart_path)
                plt.close()

                # Create the PDF
                doc = SimpleDocTemplate(predefined_pdfs["Ingestion"], pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()

                logo1_path = './IDEAS-TIH_new.jpg'
                logo2_path = './CSI_new.jpg'

                if os.path.exists(logo1_path) and os.path.exists(logo2_path):
                    logo1 = Image(logo1_path, width=1.5*inch, height=1*inch)
                    logo2 = Image(logo2_path, width=1.5*inch, height=1*inch)
                    logo_table = Table([[logo1, '', logo2]], colWidths=[2*inch, 3*inch, 2*inch])
                    logo_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                    ]))
                    elements.append(logo_table)

                elements.append(Spacer(1, 12))
                title_style = ParagraphStyle(name='CenterTitle', parent=styles['Heading1'], fontSize=18, alignment=1)
                subtitle_style = ParagraphStyle(name='SubTitle', parent=styles['Normal'], alignment=1, fontSize=12)

                elements.append(Paragraph("Heart Murmur Detection System", title_style))
                elements.append(Paragraph("Collaborative Project of IDEAS and CSI", subtitle_style))
                elements.append(Spacer(1, 20))

                elements.append(Paragraph("Ingestion Report", styles['Heading2']))
                elements.append(Spacer(1, 12))

                summary_text = """
                This section presents an overview of the data ingestion process. It includes uploaded data previews, 
                basic statistics, data type identification, and error handling during upload.
                """
                elements.append(Paragraph(summary_text, styles['BodyText']))
                elements.append(Spacer(1, 12))

                data = [['Column', 'Data Type', 'Missing Values'],
                        ['Age', 'Integer', '0'],
                        ['Gender', 'Categorical', '2'],
                        ['Heart Rate', 'Float', '1']]
                table = Table(data, colWidths=[2*inch]*3)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))

                if os.path.exists(chart_path):
                    chart = Image(chart_path, width=5*inch, height=3*inch)
                    elements.append(Paragraph("Feature Distribution", styles['Heading3']))
                    elements.append(Spacer(1, 6))
                    elements.append(chart)

                doc.build(elements)

        def download_button(label, file_path, filename, generator_fn=None):
                if not os.path.exists(file_path) and generator_fn:
                    generator_fn()
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(label, f, file_name=filename)
                else:
                    st.warning(f"{filename} not found!")

            # Trigger the download button only for the selected report
        if   selected_report == "Ingestion":
                download_button("Download Ingestion Report", predefined_pdfs["Ingestion"], "ingestion_report.pdf", generate_ingestion_report)
        elif selected_report == "Analysis":
                download_button("Download Analysis Report", predefined_pdfs["Analysis"], "analysis_report.pdf")
        elif selected_report == "Prediction":
                download_button("Download Prediction Report", predefined_pdfs["Prediction"], "prediction_report.pdf")
        elif selected_report == "Model":
                download_button("Download Model Report", predefined_pdfs["Model"], "model_report.pdf")
        elif selected_report == "Overview":
                download_button("Download Overview Report", predefined_pdfs["Overview"], "overview_report.pdf")