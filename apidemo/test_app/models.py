from django.db import models


# Create your models here.
# The Department class is a model that represents a department with a title attribute.
class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.title}"

# The Employee class represents an employee with attributes such as first name, last name, department,
# and birthdate.
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
