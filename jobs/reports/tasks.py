import uuid
from rq.decorators import job
from worker import conn as redis_conn
from jobs.reports.utils import file_to_dataframe, sanitize_reports, delete_file
from pymongo.errors import BulkWriteError

@job('docs', connection=redis_conn, timeout=600)
def process_uploaded_document(filename, user_id):
  from modules.reports.models import Report

  try:
    df = file_to_dataframe(filename)
    sanitized_df = sanitize_reports(df, user_id)
    reports_dict = sanitized_df.to_dict('records')

    # Memory overhead
    report_instances = [Report(**data).to_mongo() for data in reports_dict]
    Report._get_collection().insert_many(report_instances, ordered=False)
  except BulkWriteError as bwe:
    print('There were some duplicate documents skipped from bulk insert', flush=True)
  except Exception as e:
    print(e, flush=True)
  finally:
    delete_file(filename)
