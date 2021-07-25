import os
import pandas as pd

def get_file_extension(filename):
  file_ext = os.path.splitext(filename)[1]
  return file_ext

def sanitize_duplicate_reports(df):
  pass

def file_to_dic(filename):
  file_ext = get_file_extension(filename)
  if file_ext in ['.xlsx', '.xls']:
    df = pd.read_excel(filename)
  else:
    df = pd.read_csv(filename)
  
  sanitized_df = sanitize_duplicate_reports(df)
  