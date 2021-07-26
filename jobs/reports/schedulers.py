import os

def delete_temp_files():
  files = os.listdir('temp')
  print(files, 'aaa', flush=True)
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
    path = os.path.join('temp', file)
    os.remove(path)
