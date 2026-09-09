from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    name: str
    department: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)