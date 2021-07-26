import os
from constants import UPLOAD_FOLDER

def delete_temp_files():
  files = os.listdir(UPLOAD_FOLDER)
  
  filtered_files = [
    file
    for file in files
    if (
        file.endswith('.xlsx') or 
        file.endswith('.xls') or
        file.endswith('.csv')
    )
  ]

  for file in filtered_files:
    path = os.path.join(UPLOAD_FOLDER, file)
    os.remove(path)
