import datetime
from modules.reports.models import Report

def report_already_done(project, user, report_date):
  report_date = datetime.datetime.strptime(report_date, '%Y-%m-%d')
  report_iso_date = report_date.isocalendar()
  report_iso_year = report_iso_date[0]
  report_iso_week = report_iso_date[1]

  db_report = Report.objects.filter(
    project=project,
    user=user,
    report_iso_year=report_iso_year,
    report_iso_week=report_iso_week
  ).first()

  return True if db_report else False

