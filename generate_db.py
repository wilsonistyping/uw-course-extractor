from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses_AUT2023'
    sln = Column("sln", Integer, primary_key=True)
    subject_code = Column("subject_code", String)
    course_code = Column("course_code", String)
    course_title = Column("course_title", String)
    restrictions = Column("restrictions", String)
    section_id = Column("section_id", String)
    credits = Column("credits", String)
    dates = Column("dates", String)
    times = Column("times", String)
    building = Column("building", String)
    room = Column("room", String)
    instructor = Column("instructor", String)
    status = Column("status", String)
    enrollment = Column("enrollment", String)
    enrollment_limit = Column("enrollment_limit", String)
    grading = Column("grading", String)
    course_fee = Column("course_fee", String)
    modality = Column("modality", String)
    other = Column("other", String)

def __init__(self, sln, subject_code, course_code, course_title, restrictions, section_id, credits, dates, times, building, room, instructor, status, enrollment, enrollment_limit, grading, course_fee, modality, other):
    self.sln = sln
    self.subject_code = subject_code
    self.course_code = course_code
    self.course_title = course_title
    self.restrictions = restrictions
    self.section_id = section_id
    self.credits = credits
    self.dates = dates
    self.times = times
    self.building = building
    self.room = room
    self.instructor = instructor
    self.status = status
    self.enrollment = enrollment
    self.enrollment_limit = enrollment_limit
    self.grading = grading
    self.course_fee = course_fee
    self.modality = modality
    self.other = other

def __repr__(self):
    return f"<Course(sln={self.sln}, course_title={self.course_title}, restrictions={self.restrictions}, section_id={self.section_id}, credits={self.credits}, dates={self.dates}, times={self.times}, building={self.building}, room={self.room}, instructor={self.instructor}, status={self.status}, enrollment={self.enrollment}, enrollment_limit={self.enrollment_limit}, grading={self.grading}, course_fee={self.course_fee}, modality={self.modality}, other={self.other})>"

engine = create_engine('sqlite:///courses_AUT2023.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

autumn_qtr_filepath = "course_data/AUT2023_COMPREHENSIVE_data.json"

with open(autumn_qtr_filepath, "r") as json_file:
    data = json.load(json_file)
    for course in data:
        for section in course['sections']:
            session.add(Course(
                sln=int(section['SLN']),
                subject_code=course['subject_code'],
                course_code=course['course_code'],
                course_title=course['course_title'],
                restrictions=section['restrictions'],
                section_id=section['section_id'],
                credits=section['credits'],
                dates=section['dates'],
                times=section['times'],
                building=section['building'],
                room=section['room'],
                instructor=section['instructor'],
                status=section['status'],
                enrollment=section['enrollment'],
                enrollment_limit=section['enrollment_limit'],
                grading=section['grading'],
                course_fee=section['course_fee'],
                modality=section['modality'],
                other=section['other']
            ))

session.commit()
session.close()


    
