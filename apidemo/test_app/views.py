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
    department_id: int
    birthdate: date


class DepartmentIn(Schema):
    title: str


# Output Schema(GET)


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department__title: str
    birthdate: date


class DeptOut(Schema):
    id: int
    title: str


# Create your views here.


@api_v1.get("/add")
def add(request, a: int, b: int) -> dict[str, int]:
    """
    The function "add" takes two integer inputs and returns a dictionary with the sum of the inputs.

    :param request: The `request` parameter is typically used to handle HTTP requests in web
    applications. It can contain information about the incoming request, such as headers, cookies, and
    query parameters. In this specific function, the `request` parameter is not used, so it can be
    ignored
    :param a: An integer representing the first number to be added
    :type a: int
    :param b: The parameter "b" is an integer that represents the second number to be added
    :type b: int
    :return: A dictionary with a single key-value pair is being returned. The key is "result" and the
    value is the sum of the two input integers, a and b.
    """
    return {"result": a + b}


@api_v1.post("/employees")
def create_employee(request, payload: EmployeeIn):
    """
    The function creates a new employee object using the provided payload and returns the ID of the
    created employee.

    :param request: The `request` parameter is an object that represents the HTTP request made to the
    server. It contains information such as the request method (GET, POST, etc.), headers, and query
    parameters
    :param payload: The payload parameter is of type EmployeeIn, which is likely a data model or class
    representing the data needed to create a new employee. It is expected to have attributes or fields
    that match the fields of the Employee model, such as name, age, email, etc. The payload parameter is
    used to
    :type payload: EmployeeIn
    :return: a dictionary with the key "id" and the value being the id of the created employee.
    """
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}  # type: ignore


@api_v1.get("/departments", response=List[DeptOut])
def get_all_emps_depart_wise(request):
    """
    The function "get_all_emps_depart_wise" returns all departments ordered by title.

    :param request: The `request` parameter is typically an HTTP request object that contains
    information about the current request being made by the user. It can include details such as the
    user's IP address, the requested URL, any submitted form data, and more. In this case, it seems that
    the `request` parameter
    :return: a queryset of all departments ordered by their title.
    """
    depts = Department.objects.all().order_by("title")
    return depts


@api_v2.get("/departments", response=List[DeptOut])
async def get_all_employees_departmentwise_async(request):
    """
    The function retrieves all employees grouped by department asynchronously.

    :param request: The `request` parameter is likely an HTTP request object that is passed to the
    function. It could contain information about the client's request, such as headers, query
    parameters, and request body. However, in the given code snippet, the `request` parameter is not()
    used, so it may not
    :return: a list of all the Department objects, ordered by their title.
    """
    depts = Department.objects.all().order_by("title")
    await sync_to_async(list)(depts)
    return depts


@api_v1.get("/emp_dept", response=List[EmployeeOut])
def fetch_all_details(request):
    """
    The function "fetch_all_details" retrieves all details of employees including their ID, first name,
    last name, department title, and birthdate.

    :param request: The `request` parameter is typically used in Django views to represent an HTTP
    request made by a client. It contains information about the request, such as the method (GET, POST,
    etc.), headers, and any data sent with the request. However, in the given code snippet, the `request
    :return: a queryset containing the details of all employees. The details include the employee's ID,
    first name, last name, department title, and birthdate.
    """
    qs = Employee.objects.all().values(
        "id", "first_name", "last_name", "department__title", "birthdate"
    )
    return qs


@api_v2.get("/emp_dept", response=List[EmployeeOut])
async def fetch_all_details_async(request):
    """
    The function retrieves all details of employees asynchronously and returns them as a queryset.

    :param request: The `request` parameter is the HTTP request object that is passed to the view
    function. It contains information about the current request, such as the request method, headers,
    and query parameters. In this case, it is not being used in the function, so it can be removed if
    not needed
    :return: a queryset of Employee objects with the following fields: "id", "first_name", "last_name",
    "department__title", and "birthdate".
    """
    qs = Employee.objects.all().values(
        "id", "first_name", "last_name", "department__title", "birthdate"
    )
    await sync_to_async(list)(qs)
    return qs


@api_v1.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    """
    The function updates an employee's information based on the provided payload.

    :param request: The `request` parameter is an object that represents the HTTP request made to the
    server. It contains information about the request, such as the headers, body, and query parameters
    :param employee_id: The employee_id parameter is an integer that represents the unique identifier of
    the employee you want to update
    :type employee_id: int
    :param payload: The `payload` parameter is an instance of the `EmployeeIn` class. It represents the
    data that will be used to update the employee
    :type payload: EmployeeIn
    :return: a dictionary with a single key-value pair. The key is "success" and the value is True.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api_v1.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    """
    The `delete_employee` function deletes an employee with the given `employee_id` and returns a
    success message.

    :param request: The request object represents the HTTP request made by the client. It contains
    information such as the HTTP method (GET, POST, etc.), headers, and any data sent in the request
    :param employee_id: The `employee_id` parameter is an integer that represents the unique identifier
    of the employee that needs to be deleted
    :type employee_id: int
    :return: a dictionary with a key "success" and a value of True.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
