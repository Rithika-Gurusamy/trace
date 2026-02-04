from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas
from typing import Optional
from models import User
from models import Student
from datetime import date
from auth import hash_password
from auth import verify_password
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.role not in ["student", "faculty"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created"}
@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "role": user.role
    }

@app.post("/student/profile")
def create_student_profile(
    # Mandatory
    name: str,
    register_no: str,

    # Optional basic info
    roll_no: Optional[str] = None,
    mobile_no: Optional[str] = None,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    scholar_type: Optional[str] = None,

    # Parent details
    father_name: Optional[str] = None,
    father_mobile_no: Optional[str] = None,
    mother_name: Optional[str] = None,
    mother_mobile_no: Optional[str] = None,

    # Personal & community
    blood_group: Optional[str] = None,
    residential_address: Optional[str] = None,
    community: Optional[str] = None,
    caste: Optional[str] = None,

    # Academic records
    hslc_total_marks: Optional[str] = None,
    hslc_cutoff_marks: Optional[str] = None,
    hslc_percentage: Optional[str] = None,

    sslc_total_marks: Optional[str] = None,
    sslc_percentage: Optional[str] = None,

    # Government IDs
    emis_number: Optional[str] = None,
    umis_number: Optional[str] = None,
    aadhar_number: Optional[str] = None,

    # Student categories & scholarships
    first_graduate: Optional[bool] = None,
    first_graduate_certificate_number: Optional[str] = None,
    pudhumai_pen: Optional[bool] = None,

    sc_st_scholarship: Optional[bool] = None,
    pmss_scholarship: Optional[bool] = None,
    category_7_5_scholarship: Optional[bool] = None,
    mudhalvan_scholarship: Optional[bool] = None,

    other_scholarship: Optional[bool] = None,
    other_scholarship_name: Optional[str] = None,

    db: Session = Depends(get_db)
):
    student = Student(
        name=name,
        register_no=register_no,
        roll_no=roll_no,
        mobile_no=mobile_no,
        date_of_birth=date_of_birth,
        gender=gender,
        scholar_type=scholar_type,

        father_name=father_name,
        father_mobile_no=father_mobile_no,
        mother_name=mother_name,
        mother_mobile_no=mother_mobile_no,

        blood_group=blood_group,
        residential_address=residential_address,
        community=community,
        caste=caste,

        hslc_total_marks=hslc_total_marks,
        hslc_cutoff_marks=hslc_cutoff_marks,
        hslc_percentage=hslc_percentage,

        sslc_total_marks=sslc_total_marks,
        sslc_percentage=sslc_percentage,

        emis_number=emis_number,
        umis_number=umis_number,
        aadhar_number=aadhar_number,

        first_graduate=first_graduate,
        first_graduate_certificate_number=first_graduate_certificate_number,
        pudhumai_pen=pudhumai_pen,

        sc_st_scholarship=sc_st_scholarship,
        pmss_scholarship=pmss_scholarship,
        category_7_5_scholarship=category_7_5_scholarship,
        mudhalvan_scholarship=mudhalvan_scholarship,

        other_scholarship=other_scholarship,
        other_scholarship_name=other_scholarship_name,

        class_id=1  # 3 CSE B
    )

    db.add(student)
    db.commit()

    return {"message": "Student profile created successfully"}

@app.get("/student/profile/{register_no}")
def get_student_profile(register_no: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.register_no == register_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.put("/student/profile/{register_no}")
def update_student_profile(
    register_no: str,

    # Optional fields (only update what user sends)
    name: Optional[str] = None,
    roll_no: Optional[str] = None,
    mobile_no: Optional[str] = None,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    scholar_type: Optional[str] = None,

    father_name: Optional[str] = None,
    father_mobile_no: Optional[str] = None,
    mother_name: Optional[str] = None,
    mother_mobile_no: Optional[str] = None,

    blood_group: Optional[str] = None,
    residential_address: Optional[str] = None,
    community: Optional[str] = None,
    caste: Optional[str] = None,

    hslc_total_marks: Optional[str] = None,
    hslc_cutoff_marks: Optional[str] = None,
    hslc_percentage: Optional[str] = None,

    sslc_total_marks: Optional[str] = None,
    sslc_percentage: Optional[str] = None,

    # Government IDs
    emis_number: Optional[str] = None,
    umis_number: Optional[str] = None,
    aadhar_number: Optional[str] = None,

    # Student categories & scholarships
    first_graduate: Optional[bool] = None,
    first_graduate_certificate_number: Optional[str] = None,
    pudhumai_pen: Optional[bool] = None,

    sc_st_scholarship: Optional[bool] = None,
    pmss_scholarship: Optional[bool] = None,
    category_7_5_scholarship: Optional[bool] = None,
    mudhalvan_scholarship: Optional[bool] = None,

    other_scholarship: Optional[bool] = None,
    other_scholarship_name: Optional[str] = None,

    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.register_no == register_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update only provided fields
    params = locals()
    for field, value in params.items():
        if field not in ["db", "register_no", "student", "params"] and value is not None:
            if hasattr(student, field):
                setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return {"message": "Student profile updated successfully"}

