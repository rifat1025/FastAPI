from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from practice.models import Base, Employee
from practice.validate import EmployeeCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "MySQL Connected"}


# Create Employee
@app.post("/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    

    new_employee = Employee(
        name=employee.name,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# Get All Employees
@app.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    return employees


# Get Employee By ID
@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# Update Employee
@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if existing_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary

    db.commit()
    db.refresh(existing_employee)

    return {
        "message": "Employee updated successfully",
        "id": existing_employee.id,
        "name": existing_employee.name,
        "department": existing_employee.department,
        "salary": existing_employee.salary,
    }


# Delete Employee
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    } 