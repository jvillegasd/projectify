from rq.decorators import job
from worker import conn as redis_conn

@job('docs', connection=redis_conn, timeout=600)
def process_uploaded_document(filename, user_id):
  print(filename, user_id, flush=True)
  pass
