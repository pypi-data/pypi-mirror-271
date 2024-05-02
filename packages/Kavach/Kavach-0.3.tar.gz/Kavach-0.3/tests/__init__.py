import sys
import os

# Add the directory containing utils.py to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import process_column, modify_csv
