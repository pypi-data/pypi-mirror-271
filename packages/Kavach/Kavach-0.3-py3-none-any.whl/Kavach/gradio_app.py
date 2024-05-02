# gradio_app.py
import gradio as gr
import pandas as pd
import re
from .utils import modify_csv, image_to_base64
from importlib import resources
import warnings
import logging
import sys

# Setup logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def hide_all_warnings():
    """Suppress all warnings."""
    warnings.filterwarnings("ignore")

hide_all_warnings()

# Assuming your package is named RedactPII and logo.png is stored in a directory named data
with resources.path("Kavach.data", "logo.png") as logo_path:
    logo_base64 = image_to_base64(str(logo_path))

columns_to_redact = []

def display_csv(file):
    df = pd.read_csv(file)
    return df

def export_csv(d):
    d.to_csv("output.csv")
    return gr.File(value="output.csv", visible=True)

custom_css = """
body { background-color: #1f1f1f; }
div { color: white; }
h1 { text-align: center; color: #ffffff; }
label { color: #ffffff; }
input, textarea { background-color: #333333; border-color: #555555; color: white; }
"""

def gradio_interface(file):
    global columns_to_redact
    return modify_csv(file, columns_to_redact)

def launch_gradio():
    with gr.Blocks(css=custom_css) as demo:
        with gr.Row():
            gr.Markdown(f"""
                <div style='background-color: #f0eae3; padding: 10px; text-align: center; border-radius: 10px; margin-bottom: 90px;'>
                    <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height: 100px; width: 100px; display: block; margin-left: auto; margin-right: auto;">
                </div>
            """)

        with gr.Column():
            csv_input = gr.File(label="Upload CSV File", file_types = ['.csv'])
            csv_display = gr.Dataframe(visible=False)
            csv_output = gr.Dataframe(type="pandas", col_count=7)
            button = gr.Button("Export")
            csv = gr.File(interactive=False, visible=False)

        button.click(export_csv, csv_output, csv)
        # csv_input.change(display_csv, inputs=csv_input, outputs=csv_display)
        csv_input.change(gradio_interface, inputs=csv_input, outputs=csv_output)
        csv_input.change(modify_csv, inputs=csv_input, outputs=csv_output)

# Launch the Gradio app
    demo.launch(share=True)

def main():
    # Collect user input for columns to redact
    try: 
        input_columns = input("Enter column names to redact, separated by commas: ")
        columns_to_redact.extend([x.strip() for x in input_columns.split(',')])
    # Launch the Gradio interface with the specified columns to redact
        launch_gradio()
    except Exception as e: 
        logging.error(f"Failed to launch the interface: {e}", exc_info=True)
        # Optionally, display a generic error message or none at all
        print("An error occurred, please try again later.")

