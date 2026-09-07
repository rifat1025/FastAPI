from fastapi import FastAPI,HTTPException
from validate import Employee


app = FastAPI()


# Temporary Database
employees = []


@app.get('/')

def home():
    return {'message': 'Run the code '}

@app.get('/about')

def about():
    return {'About': 'Rifat,24 years old'}




#create employee
@app.post("/employees")

def create_employee(employee:Employee):
    employees.append(employee.dict())
    return {
        "Employes":"employee create succesfull",
        "employee":employee
    }

@app.get('/employees/{id}')
def get_employee(id: int):
    if id >= len(employees):
        raise HTTPException (
            status_code = 404,
            detaile = "employee not found"
        )          

    return employees[id]

# update employee

@app.put('/employees/{id}')

def update_employee(id:int, employee:Employee):

    if id >= len(employees):
            raise HTTPException (
                status_code = 404,
                detaile = "employee not found"
            )
    employees[id] =employee.dict()
    return {
         'employee':"employee updated successfullY",
         'employee' : employees[id]
    }          
    
    return employees
