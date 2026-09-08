from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    name: str
    department: str
    salary: float

class EmployeeCreate(EmployeeBase):
    name : str
    department: str
    salary : float

class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)