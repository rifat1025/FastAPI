from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from database import engine
from models import Base
from validate import EmployeeCreate,EmployeeResponse
from database import SessionLocal,get_db
from models import Employee

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "MySQL Connected"}

@app.post("/employees")
def create_employees(employee:EmployeeCreate, db: Session = Depends(get_db)):
    

    new_employee=Employee(
        name = employee.name,
        department = employee.department,
        salary = employee.salary
    ) 

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

# Get all employee's 
@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    # database connection
    
    #from tabnle get all employee 
    employees = db.query(Employee).all()

    db.close()

    return employees 


# Get employee  for sepcific user id
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    # db connection
    

    # employee query for find from table
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    db.close()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

# update the employee information 

@app.put("/employees/{employee_id}")
def update_employee(employee_id:int, employee:EmployeeCreate, db: Session = Depends(get_db)):
    

    existing_employee = (db.query(Employee).filter(Employee.id == employee_id).first() )

    if not existing_employee:
        db.close()
        raise HTTPException(
            status_code= 404,
            detail= "Employee not Found"

        )
    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee . salary = employee.salary
    

    db.commit()
    db.refresh(existing_employee)
    db.close()
    return {
        "message": "Employee updated successfully",
        "employee": existing_employee
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    db.close()

    return {
        "message": "Employee deleted successfully"
    }

      
    
    

