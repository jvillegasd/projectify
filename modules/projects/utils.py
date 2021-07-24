from modules.projects.models import Project

def check_project_existance(name):
  project = Project.objects.filter(name=name)
  return True if project else False
