from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
from .models import Employee, Position, Project
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json



class EmployeeView(View):
    def get(self, request):
        numemp = Employee.objects.count()
        info = Employee.objects.all()
        dic = {"dicnumemp":numemp, 'info':info}
        return render(request, "employee.html", dic,)
    
class PositionView(View):
    def get(self, request):
        position = Position.objects.all().annotate(numPosi=Count('employee'))
        dic = {"position":position,}
        return  render(request, "position.html", dic,)
    
class ProjectView(View):
    def get(self, request):
        project = Project.objects.all()
        dic = {"project":project,}
        return  render(request, "project.html", dic,)
    
class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        startdate = project.start_date.strftime('%Y-%m-%d')
        duedate = project.due_date.strftime('%Y-%m-%d')
        projectStaff = project.staff.all()
        
        dic = {"project":project,
               'startdate':startdate,
               'duedate':duedate,
               'projectStaff': projectStaff}
        return  render(request, "project_detail.html", dic,)
    
    def put(self, request, project_id, emp_id):
        try:
            
            project = Project.objects.get(id=project_id)
            employee = Employee.objects.get(id=emp_id)

            # Add employee to project
            project.staff.add(employee)
            return JsonResponse({'message': 'Employee added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    def delete(self, request, project_id, emp_id):
        try: 
            project = Project.objects.get(id=project_id)
            employee = Employee.objects.get(id=emp_id)
            project.staff.remove(employee)
            return JsonResponse({"message": "Project deleted successfully."}, status=200)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)
        
    
class ProjectDeleteView(View):
    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({"message": "Project deleted successfully."}, status=200)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)
