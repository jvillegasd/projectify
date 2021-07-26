import os
import uuid
import pandas as pd
from constants import UPLOAD_FOLDER

def get_file_extension(filename):
  file_ext = os.path.splitext(filename)[1]
  return file_ext

def sanitize_reports(df, user_id):
  df['user'] = user_id

  df['user'] = df['user'].apply(lambda x: uuid.UUID(x))
  df['project'] = df['project_id'].apply(lambda x: uuid.UUID(x))

  df.drop('project_id', axis=1, inplace=True)

  df['report_date'] = pd.to_datetime(df['report_date'], format='%Y-%m-%d')
  df['report_iso_year'] = df['report_date'].apply(lambda x: x.isocalendar()[0])
  df['report_iso_week'] = df['report_date'].apply(lambda x: x.isocalendar()[1])

  # Delete duplicates
  sanitized_df = df.drop_duplicates(['project', 'user', 'report_iso_year', 'report_iso_week'], keep='first')
  return sanitized_df

def file_to_dataframe(filename):
  path = os.path.join(UPLOAD_FOLDER, filename)

  file_ext = get_file_extension(filename)
  if file_ext in ['.xlsx', '.xls']:
    df = pd.read_excel(path)
  else:
    df = pd.read_csv(path)
  
  return df

def delete_file(filename):
  path = os.path.join(UPLOAD_FOLDER, filename)
  os.remove(path)
