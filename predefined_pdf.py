from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (Paragraph, Table, TableStyle, Spacer, Image,
                                 SimpleDocTemplate, PageBreak, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
import os
import datetime

# Image paths
left_logo_path = "./IDEAS-TIH_new.jpg"
right_logo_path = "./CSI_new.jpg"
watermark_path = "./IDEAS-TIH_new.jpg" 

# Output directory
OUTPUT_DIR = "static_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

# Custom Styles
section_title_style = ParagraphStyle(
    'SectionTitle',
    parent=styles['Heading1'],
    fontSize=15,
    textColor=colors.HexColor("#003366"),
    spaceAfter=12,
    backColor=colors.lightblue,
    alignment=TA_CENTER,
    leading=18
)

custom_body_style = ParagraphStyle(
    name='CustomBody',
    parent=styles['Normal'],
    fontsize=12,
    leading=30,
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    bulletIndent=10,
    leftIndent=20,
    spaceAfter=6
)

normal_bold = ParagraphStyle(
    'NormalBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    spaceAfter=10
)

# Today's date
today_str = datetime.datetime.today().strftime("%B %d, %Y")

# Header, footer, watermark
def draw_header_footer(c, doc):
    width, height = A4
    draw_watermark(c, width, height)
    draw_header(c, width, height)
    draw_footer(c, width)

def draw_watermark(c, width, height):
    if os.path.exists(watermark_path):
        watermark = ImageReader(watermark_path)
        w, h = watermark.getSize()
        scale = 300 / w
        c.saveState()
        c.translate((width - w * scale) / 2, (height - h * scale) / 2)
        c.setFillAlpha(0.05)
        c.drawImage(watermark, 0, 0, width=w * scale, height=h * scale, mask='auto')
        c.restoreState()

def draw_header(c, width, height):
    logo_height = 50
    margin = 40
    if os.path.exists(left_logo_path):
        left_logo = ImageReader(left_logo_path)
        w, h = left_logo.getSize()
        scale = logo_height / h
        c.drawImage(left_logo, margin, height - logo_height - margin, width=w * scale, height=logo_height, mask='auto')

    if os.path.exists(right_logo_path):
        right_logo = ImageReader(right_logo_path)
        w, h = right_logo.getSize()
        scale = logo_height / h
        c.drawImage(right_logo, width - w * scale - margin, height - logo_height - margin, width=w * scale, height=logo_height, mask='auto')

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 60, "Heart Murmur Detection System")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, "Collaborative Project of IDEAS and CSI")

def draw_footer(c, width):
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2.0, 0.5 * inch, f"Generated on: {today_str} | Page {c.getPageNumber()}")

# Build PDF sections
def build_ingestion_pdf():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Ingestion_Report.pdf"), pagesize=A4)
    elements = [Spacer(1, 10)]
    elements.append(Paragraph("Ingestion Module", section_title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<font size=15 color='darkblue'><b>Overview:</b></font>",normal_bold ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "<font size=12>The Ingestion Module provides a structured interface for uploading, managing, and interacting with <b>.wav</b> audio files. It enables users"
        " to upload files locally, display existing datasets, and perform essential actions like selecting, downloading, and deleting audio data. All operations"
        " are integrated into a dynamic GUI built with Streamlit and connected to a backend database for persistent storage and retrieval."
        "This module ensures effective dataset handling by combining metadata management, session handling, and interactive data controls—laying a foundation" 
        " for clean ingestion workflows in data-driven applications..</font>", styles["Normal"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<font color='darkgreen'><b>Key Features:</b></font>", normal_bold))
    bullets = [
        "<b>Upload WAV files</b> via a local file uploader, with the ability to add metadata like descriptions for better organization.",
        "<b>View and select audio datasets</b> from a dynamic, editable table interface with real-time selection and checkbox controls.",
        "<b>Download or delete selected files</b> with integrated session state tracking and UI feedback mechanisms.",
        "<b>Automatically update dataset display</b> post any operation to reflect the current state of the database.",
        "<b>Maintain session-driven context</b> for selected files, ensuring smooth user interaction across all functionalities."
    ]
    elements.append(ListFlowable([ListItem(Paragraph(f"<font size=11>{b}</font>", bullet_style)) for b in bullets]))
    elements.append(Spacer(1, 5))
    if os.path.exists("ingestion_box_.png"):
        elements.append(Image("ingestion_box_.png", width=200, height=300))
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

def build_analysis_pdf():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Analysis_Report.pdf"), pagesize=A4)
    elements = [Spacer(1, 50)]
    elements.append(Paragraph("Analysis Module", section_title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<font size=15 color='darkblue'><b>Overview:</b></font>",normal_bold ))
    elements.append(Paragraph(
        "<font size=12>""The Analysis Module is designed as a comprehensive interface for exploring and interpreting heart sound recordings with precision "
        "and clarity. It allows users to interactively select and visualize .wav audio files, rendering both the <b>Phonocardiogram (PCG)</b> waveform and its "
        "corresponding Mel spectrogram. Additionally, users can inspect extracted acoustic features and play back audio to support qualitative evaluation."
        "The system extracts a rich set of 19 features per frame, systematically capturing both time-domain and frequency-domain characteristics of heart sounds:"
        "  1. <b>Time-Domain Features</b> (3): <b>Amplitude Envelope</b>,<b>Root Mean Square (RMS) Energy</b>,<b>Zero Crossing Rate</b>."
        "  2. <b>Frequency-Domain Features</b> (3): <b>Spectral Centroid</b>,<b>Spectral Bandwidth</b>,<b>Spectral Rolloff</b>."
        "  3. <b>MFCCs</b> (13): Mel-Frequency Cepstral Coefficients, widely used for audio signal representation."
        " For each audio file, <b>160 frames</b> are processed, resulting in a total of 3,040 features per sample (160 frames × 19 features), forming a robust"
        "feature matrix suitable for downstream analytics and machine learning workflows.</font>", styles["Normal"]
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<font color='darkgreen'><b>Core Capabilities:</b></font>", normal_bold))
    bullets =["<b>Select and visualize audio files</b> using waveform (PCG) plots to understand amplitude variations over time.",
              "<b>Generate and display Mel Spectrograms</b> to observe frequency-based patterns in heart sounds.",
              "<b>Review feature description images</b> for additional interpretation and context.",
              "<b>Play converted audio files</b> through the browser using a standardized format for playback."]
    elements.append(ListFlowable([ListItem(Paragraph(f"<font size=10>{b}</font>",bullet_style)) for b in bullets]))
    elements.append(Spacer(1, 15))
    if os.path.exists("output.png"):
        elements.append(Image("output.png", width=400, height=250))
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

def build_prediction_pdf():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Prediction_Report.pdf"), pagesize=A4)
    elements = [Spacer(1, 10)]
    elements.append(Paragraph("Prediction Module", section_title_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "<font size=15 color='darkblue'><b>Overview:</b></font>",normal_bold ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "<font size=13>This project presents a refined diagnostic framework that employs machine learning methodologies for the classification of heart"
        "sound recordings (phonocardiograms), with the objective of detecting pathological murmurs. Two classification models are employed : a <b>Support Vector "
        "Machine (SVM)</b> and a <b>Random Forest classifier</b>. Both models operate on meticulously preprocessed and feature-engineered audio inputs to "
        "distinguish between <b>normal</b> and <b>murmur</b> cases. The system processes raw heart sound recordings by excising initial noise segments "
        "and isolating a diagnostically relevant duration of the signal. From these segments, it extracts a comprehensive suite of time-domain and "
        "frequency-domain features across short, fixed-length frames. The extracted features are standardized and subsequently passed through the "
        "selected classifier to generate diagnostic predictions. An interactive Streamlit-based graphical user interface (GUI) facilitates user engagement, "
        "enabling intuitive selection of input audio files and classification models, while displaying predictions along with real-time inference "
        "latency.</font>", styles["Normal"]
    ))
    elements.append(Spacer(1, 10))
    if os.path.exists("prediction_performance.png"):
        elements.append(Image("prediction_performance.png", width=450, height=200))
    elements.append(Paragraph("<font size=15 color='darkgreen'><b>Features:</b></font>", normal_bold))
    bullets = ["<b>Dual Classifiers</b>: Includes both SVM and Random Forest models with distinct scaling parameters.",
               "<b>Frame-Based Feature Extraction</b>: Processes 50 ms frames to extract detailed signal characteristics.",
               "<b>Time & Frequency Domain Metrics</b>: Captures amplitude, RMS, ZCR, spectral properties, and MFCCs.",
               "<b>Noise-Resilient Preprocessing</b>: Removes initial noise and extracts a clean 8-second segment.",
               "<b>Real-Time Prediction</b>: Returns classification results with precise inference timing.",
               "<b>Interactive Streamlit UI</b>: Simple dropdown-based interface for file selection and prediction."
    ]
    elements.append(ListFlowable([ListItem(Paragraph(f"<font size=11>{b}</font>", bullet_style)) for b in bullets]))
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

def build_model_pdf():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Model_Report.pdf"), pagesize=A4)
    elements = [Spacer(1, 15)]
    elements.append(Paragraph("Model Management Module", section_title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "<font size=15 color='darkblue'><b>Overview:</b></font>",normal_bold ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "<font size=12>This module presents a streamlined interface for managing machine learning models utilized in the classification of heart sound "
        "recordings. Developed using Streamlit, it facilitates core functionalities such as uploading, listing, downloading, and deleting .pkl model "
        "files. The system integrates with a backend database (db_2) to maintain structured records of model metadata, ensuring efficient file handling"
        " and traceability.Each uploaded model is accompanied by descriptive metadata including its title, file name, MIME type, file size, and upload "
        "timestamp. The application initializes session state variables to support smooth user interaction and employs validation mechanisms to ensure "
        "compatibility and consistency across uploaded files. This interface serves as a centralized environment for curating and managing diagnostic "
        "models critical to the system’s classification tasks..</font>", styles["Normal"]
    ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<font color='darkgreen'><b>Key Functionalities:</b></font>", normal_bold))
    bullets = [
       "<b>Model Upload Support</b>: Enables uploading of <b>.pkl</b> models with custom titles.",
       "<b>Metadata Management</b>: Records file name, type, size, and other relevant attributes.",
       "<b>Session State Handling</b>: Initializes key session variables to support persistent interaction.",
       "<b>Model Listing</b>: Displays existing models along with their metadata in a tabular format.",
       "<b>Model Download</b>: Allows users to download selected models from the local repository.",
       "<b>Safe Deletion Workflow</b>: Permits removal of selected models with feedback and refresh.",
       ]
    elements.append(ListFlowable([ListItem(Paragraph(f"<font size=11>{b}</font>", bullet_style)) for b in bullets]))
    elements.append(Spacer(1, 5))
    if os.path.exists("model_performace.png"):
        elements.append(Image("model_performace.png", width=200, height=250))
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

# Overview PDF
def build_overview_pdf():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Overview_Report.pdf"), pagesize=A4)
    elements = [Spacer(1, 80)]
    elements.append(Paragraph("System Overview",section_title_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b><font size=25 color='darkblue'>Table of Contents</font></b>", styles["Heading2"]))
    elements.append(Spacer(1, 30))

    toc_items = [
        ("1.", "About the project"),
        ("2.", "Ingestion Module"),
        ("3.", "Analysis Module"),
        ("4.", "Prediction Module"),
        ("5.", "Model Management Module"),
        ("6.", "Report Module"),
        ("7.", "Conclusion"),
    ]

    for number, title in toc_items:
        elements.append(Paragraph(
            f"<font size=15 color='black'><b>{number}</b> {title}</font>", styles["Normal"]
        ))
        elements.append(Spacer(1, 50))

    elements.append(PageBreak())

    sections = [
        ("1. About the project","Streamlit is a lightweight Python framework for building interactive data applications quickly and efficiently. " 
        "It’s ideal for deploying machine learning models and data visualizations with minimal code.The <b>Heart Murmur Detection System</b> is a " 
        "comprehensively integrated diagnostic apparatus, meticulously engineered to enhance the operational efficacy of clinicians and researchers " 
        "alike. This system encapsulates the entirety of cardiac auscultation analysis within a unified framework composed of four interlinked " 
        "modules: <b>Ingestion, Analysis, Prediction,</b> and <b>Model Management</b>. Each module contributes a vital procedural function, enabling " 
        "an uninterrupted, intelligent flow of phonocardiographic data through acquisition, interpretation, prognostication, and model oversight. The " 
        "architecture is designed to uphold analytical rigor and predictive accuracy, offering a scalable and clinically viable solution for automated " 
        "heart murmur detection. Its seamless integration and data coherence render it a formidable tool in the realm of digital health diagnostics."),
        ("2. Ingestion Module", "The Ingestion Module serves as the foundation for managing and organizing heart sound datasets by offering a user-friendly, "
        "structured interface for handling <b>.wav</b> audio files. It allows users to upload files locally while attaching relevant metadata such as descriptions, "
        "which aids in systematic organization and retrieval. Once uploaded, users can view and interact with their datasets through an editable, dynamic " 
        "table that includes real-time checkbox controls for selecting multiple files. From this interface, users can download or delete specific files, " 
        "with the application leveraging session state tracking to ensure smooth and consistent user experiences. Importantly, any changes made—such as " 
        "<b>uploading, deleting,</b> or <b>downloading</b> —are immediately reflected in the UI, keeping the dataset view in sync with the underlying database. This " 
        "module effectively integrates metadata management, session handling, and interactive controls into a single streamlined GUI, providing a " 
        "robust solution for clean and traceable audio ingestion workflows in data-centric applications."),
        ("3. Analysis Module","The Analysis Module is designed to enable in-depth exploration of heart sound recordings through both visual and " 
        "auditory means. Users can select .wav audio files to generate <b>Phonocardiogram (PCG)</b> waveforms that show how the signal amplitude varies " 
        "over time, alongside Mel spectrograms that illustrate frequency-based energy distribution. The module extracts a rich set of 19 features "
        "per frame, combining both <b>time-domain</b> (Amplitude Envelope, RMS Energy, Zero Crossing Rate) and <b>frequency-domain</b> metrics (Spectral Centroid, " 
        "Spectral Bandwidth, Spectral Rolloff), along with 13 Mel-Frequency Cepstral Coefficients (MFCCs), which are widely used in audio analysis. " 
        "With 160 frames processed per file, this results in a total of 3,040 features per sample, providing a comprehensive matrix that captures "
        "essential acoustic characteristics for downstream machine learning tasks. Additionally, users can view graphical representations of feature " 
        "distributions and play back the standardized audio directly in the browser to support qualitative interpretation. This module bridges " 
        "technical analysis with intuitive interaction, making acoustic feature extraction both accessible and insightful."),
         ("4. Prediction Module","The Prediction Module focuses on the automated classification of heart sound recordings, particularly aimed at " 
        "detecting pathological murmurs. It incorporates two machine learning models— <b>Support Vector Machine (SVM)</b> and <b>Random Forest</b> —both trained to " 
        "distinguish between <b>normal</b> and <b>murmur</b> cases using preprocessed and feature-engineered input data. Raw audio is first cleaned by removing noise " 
        "and isolating diagnostically meaningful segments, typically an 8-second window, which is then divided into 50ms frames for detailed analysis. " 
        "From each frame, a comprehensive set of time-domain and frequency-domain features is extracted, standardized, and passed into the selected classifier " 
        "to generate real-time diagnostic predictions. The module features an interactive Streamlit-based GUI that allows users to choose audio files " 
        "and classification models from dropdown menus, with predictions and inference latency displayed immediately. This real-time, noise-resilient " 
        "classification pipeline combines robust feature extraction with user-friendly visualization, making it a practical tool for heart sound diagnostics."),
        ("5. Model Management Module","The Model Module provides a centralized platform for handling the machine learning models used in the heart " 
        "sound classification process. It enables users to upload <b>.pkl</b> model files along with descriptive metadata such as titles, file names, " 
        "MIME types, sizes, and timestamps, ensuring all relevant information is recorded systematically. Uploaded models are stored in a dedicated " 
        "backend database (db_2), allowing for persistent and organized access. Users can view existing models in a tabular display, download selected " 
        "models, or safely delete them using built-in validation mechanisms and interactive feedback. The interface uses session state variables to " 
        "maintain continuity and ensure smooth user interactions across uploads and actions. By offering robust model traceability, metadata tracking, " 
        "and streamlined model curation in a secure environment, this module plays a vital role in maintaining the integrity and usability of diagnostic " 
        "models within the broader application ecosystem."),
        ("6. Report Module", "ReportLab is a robust Python library for programmatic PDF generation, enabling precise control over layouts, styled text, " 
        "imagery, and vector graphics. It's especially suited for dynamic, data-driven document creation. "
        "This project heavily utilizes ReportLab to automate polished, modular PDF reports across stages of a heart murmur detection pipeline— <b>ingestion, " 
        "analysis, prediction</b>, and <b>model diagnostics</b>. Key constructs like BaseDocTemplate, Frame, and Paragraph orchestrate document flow, while custom " 
        "elements (headers, footers, watermarks, logos) are rendered via draw_header_footer() for consistent branding. Visuals such as performance plots " 
        "are embedded when present. "
        "Each module has a discrete builder function — e.g., <b>build_ingestion_pdf()</b> —ensuring structural clarity and content encapsulation. Outputs are " 
        "stored in a <b>static_reports</b> directory for easy retrieval. The system integrates with a Streamlit frontend, using session state to sync user " 
        "actions with backend automation, thus fusing accessibility with architectural sophistication."),
        ("7. Conclusion", "By integrating modular functionality and advanced ML techniques,the <b>Heart Murmur Detection System</b> offers a "
        "robust and scalable solution for early cardiac dignosis .It bridges the gap between raw audio data and meaningful clinical insights")
    ]

    for title, description in sections:
        elements.append(Spacer(1, 15))
        elements.append(Paragraph(f"""<para align='center'><b><font size=12 color='navy'>{title}</font></b></para>""", section_title_style))
        elements.append(Spacer(1, 15))
        elements.append(Paragraph(f"<font size=15>{description}</font>",custom_body_style))
        elements.append(PageBreak())
       

    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

# Generate all reports
build_ingestion_pdf()
build_analysis_pdf()
build_prediction_pdf()
build_model_pdf()
build_overview_pdf()