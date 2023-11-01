from datetime import date
from typing import List

from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from test_app.models import Department, Employee

api_v1 = NinjaAPI()
api_v2 = NinjaAPI(version="2.0")


# Input Schemas(POST/PUT)
class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class DepartmentIn(Schema):
    title: str


# Output Schema(GET)


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department__title: str = None
    birthdate: date = None


class DeptOut(Schema):
    id: int
    title: str


# Create your views here.


@api_v1.get("/add")
def add(request, a: int, b: int) -> dict[str, int]:
    return {"result": a + b}


@api_v1.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@api_v1.get("/departments", response=List[DeptOut])
def get_all_emps_departwise(request):
    depts = Department.objects.all().order_by("title")
    return depts


@api_v2.get("/departments", response=List[DeptOut])
async def get_all_emps_departwise_async(request):
    depts = Department.objects.all().order_by("title")
    await sync_to_async(list)(depts)
    return depts


@api_v1.get("/emp_dept", response=List[EmployeeOut])
def get_all_details(request):
    qs = Employee.objects.all().values(
        "id", "first_name", "last_name", "department__title", "birthdate"
    )
    return qs


@api_v2.get("/emp_dept", response=List[EmployeeOut])
async def get_all_details_async(request):
    qs = Employee.objects.all().values(
        "id", "first_name", "last_name", "department__title", "birthdate"
    )
    await sync_to_async(list)(qs)
    return qs


@api_v1.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api_v1.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}