from rq.job import Job
from worker import conn as redis_conn
from rq.exceptions import NoSuchJobError

def get_job_result(job_id):
  job = Job.fetch(job_id, redis_conn)
  
  if not job.is_finished:
    return None, job.get_status()
  else:
    return job.result, job.get_status()

def get_job_status(job_id):
  try:
    job = Job.fetch(job_id, redis_conn)
    return job.get_status()
  except NoSuchJobError:
    return 'not_found'
