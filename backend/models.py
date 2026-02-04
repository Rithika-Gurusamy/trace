from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    register_no = Column(String, unique=True)
    roll_no = Column(String)
    mobile_no = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)

    scholar_type = Column(String)  # Day Scholar / Hosteller
    class_id = Column(Integer, ForeignKey("classes.id"))

    father_name = Column(String)
    father_mobile_no = Column(String)
    mother_name = Column(String)
    mother_mobile_no = Column(String)

    blood_group = Column(String)
    residential_address = Column(String)
    community = Column(String)
    caste = Column(String)

    hslc_total_marks = Column(String)
    hslc_cutoff_marks = Column(String)
    hslc_percentage = Column(String)

    sslc_total_marks = Column(String)
    sslc_percentage = Column(String)

    emis_number = Column(String)
    umis_number = Column(String)
    aadhar_number = Column(String)

    first_graduate = Column(Boolean)
    first_graduate_certificate_number = Column(String)
    pudhumai_pen = Column(Boolean)

    sc_st_scholarship = Column(Boolean)
    pmss_scholarship = Column(Boolean)
    category_7_5_scholarship = Column(Boolean)
    mudhalvan_scholarship = Column(Boolean)

    other_scholarship = Column(Boolean)
    other_scholarship_name = Column(String)