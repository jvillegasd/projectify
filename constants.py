import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'temp')
UPLOAD_EXTENSIONS = ['.xlsx', '.xls', '.csv']
MAX_CONTENT_LENGTH = 3 * 1024 * 1024 # 3mb
