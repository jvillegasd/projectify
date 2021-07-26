import os
import uuid
import datetime
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

@job('docs', connection=redis_conn, timeout=600)
def generate_report_document(start_date, end_date):
  from constants import UPLOAD_FOLDER
  from pandas.io.json import json_normalize
  from modules.reports.models import Report
  from modules.reports.serializers import ReportDetailSchema

  filename = str(uuid.uuid4()) + '.xlsx'
  path = os.path.join(UPLOAD_FOLDER, filename)

  start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
  end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

  reports = Report.objects.filter(report_date__gte=start_date, report_date__lte=end_date)
  reports = ReportDetailSchema(many=True).dump(reports)

  df = json_normalize(reports)
  df = df.rename(columns={ 'project.doc_id': 'project_id' })

  df.drop(columns=[
    'doc_id',
    'report_iso_year',
    'report_iso_week',
    'created_at',
    'updated_at'
  ], axis=1, inplace=True)
  df.to_excel(path, index=False)
  return filename
