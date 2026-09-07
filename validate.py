from pydantic import BaseModel

class Employee(BaseModel):
    Name: str
    Department : str
    Salary : int