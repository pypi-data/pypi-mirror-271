
from sqlalchemy import Column, DateTime, ForeignKey, Enum, JSON,Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Float,Integer, Boolean
from espy_contact.util.enums import ResourceEnum, GradeLevel, Term
from espy_contact.model.models import Appuser, Address
from espy_contact.util.db import Base
import uuid


class Resource(Base):
    """Type of resource can be Poll, Form Builder, Questionnaire, RichText, Video, Audio, File, Hyperlink."""

    __tablename__ = "resources"
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    type = Column(Enum(ResourceEnum))
    lesson_id = Column(String, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", foreign_keys=[lesson_id])


# class QuizOption(Base):
#     __tablename__ = "quiz_options"
#     id = Column(String, primary_key=True, index=True)
#     option_text = Column(String)
#     quiz_id = Column(String, ForeignKey("quizzes.id"))
#     quiz = relationship("Quiz", back_populates="options", foreign_keys=[quiz_id])

# class Quiz(Base):
#     __tablename__ = "quizzes"
#     id = Column(String, primary_key=True, index=True)
#     question = Column(String)
#     options = relationship("QuizOption", back_populates="quiz",foreign_keys=[QuizOption.quiz_id])
#     answer_id = Column(String, ForeignKey("quiz_options.id"))
#     answer = relationship("QuizOption",foreign_keys=[answer_id])
#     lesson_id = Column(String, ForeignKey("lessons.id"))
#     lesson = relationship("Lesson", foreign_keys=[lesson_id])


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    question = Column(String)
    options = Column(JSON)  # Store options as JSON
    answer = Column(String)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    Lesson = relationship("Lesson", foreign_keys=[lesson_id])


class LessonNote(Base):
    __tablename__ = "lesson_notes"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    title = Column(String)
    lesson = relationship("Lesson", back_populates="note")


class LessonResource(Base):
    __tablename__ = "lesson_resource"

    lesson_id = Column(String, ForeignKey("lessons.id"), primary_key=True)
    resource_id = Column(String, ForeignKey("resources.id"), primary_key=True)


class LessonAssets(Base):
    __tablename__ = "lessons_assets"
    asset = Column(String)
    lesson_id = Column(String, ForeignKey("lessons.id"), primary_key=True)
    lesson = relationship("Lesson", back_populates="assets")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    note_id = Column(String, ForeignKey("lesson_notes.id"))
    note = relationship("LessonNote", back_populates="lesson")
    assets = relationship(
        "LessonAssets", back_populates="lesson"
    )  # Consider using a separate table for assets
    topic_id = Column(String, ForeignKey("topics.id"))
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", foreign_keys=[quiz_id])


class Topic(Base):
    __tablename__ = "topics"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    title = Column(String)
    lessons = relationship("Lesson", backref="topic")
    subject_id = Column(String, ForeignKey("subjects.id"))
    timestamp = Column(DateTime(), server_default=func.now())


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    grade = Column(Enum(GradeLevel))
    topics = relationship("Topic", backref="subject")
    term = Column(Enum(Term))
    reviews = relationship("Review", backref="reviewed_subject")
    class_id = Column(String, ForeignKey("classrooms.id"))
    classroom = relationship("Classroom", back_populates="subjects")


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    title = Column(String, unique=True)
    timestamp = Column(DateTime(), server_default=func.now())
    teacher_id = Column(String, ForeignKey("appusers.id"), nullable=True)
    teacher = relationship("Appuser")  # Optional backref
    school_id = Column(String)

    subjects = relationship("Subject", back_populates="classroom")
    students = relationship("Student", back_populates="classroom")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    review = Column(String)
    rating = Column(Float)
    reviewer = Column(String)
    created_at = Column(DateTime)
    subject_id = Column(String, ForeignKey("subjects.id"))
    # reviewed_subject = relationship("Subject", foreign_keys=[subject_id])


class ClassroomSubject(Base):
    __tablename__ = "classroom_subjects"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    classroom_id = Column(String, ForeignKey("classrooms.id"))
    subject_id = Column(String, ForeignKey("subjects.id"))

# class ReachBase:
#     id = Column(String, primary_key=True, index=True)
#     timestamp = Column(DateTime(), server_default=func.now())
# address_associations = Table(
#     "address_associations", Base.metadata,
#     Column("id", String, primary_key=True, index=True),
#     Column("school_id", String, ForeignKey("schools.id")),
#     Column("user_id", String, ForeignKey("appusers.id")),
#     Column("address_id", String, ForeignKey("addresses.id")),
# )


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dob = Column(Date)
    gender = Column(String)
    nationality = Column(String)
    user_id = Column(String, ForeignKey("appusers.id"))
    user = relationship("Appuser", foreign_keys=[user_id])
    parent_email = Column(String)
    current_school = Column(String)
    current_class = Column(String)
    achievements = Column(String)
    extracurricular = Column(String)
    parent_phone = Column(String)
    parent_name = Column(String)
    parent_occupation = Column(String)
    religion = Column(String)
    grade_level = Column(Enum(GradeLevel))
    term = Column(Enum(Term))
    academic_year = Column(Integer)
    remarks = Column(String)
    photo = Column(String)
    birth_certificate = Column(String)
    signature = Column(String)
    is_paid = Column(Boolean)


class School(Base):
    __tablename__ = "schools"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    owner_id = Column(String, ForeignKey("appusers.id"))
    timestamp = Column(DateTime(), server_default=func.now())
    address_id = Column(
        String, ForeignKey("addresses.id"), nullable=True
    )  # Add foreign key
    address = relationship(
        "Address", uselist=False, backref="school"
    )  # One-to-one relationship


class Student(Base):
    __tablename__ = "student"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    biodata_id = Column(
        String, ForeignKey("appusers.id")
    )  # Define ForeignKey for relationship
    biodata = relationship("Appuser")  # Define relationship
    date_of_birth = Column(String)
    id_card = Column(String)
    class_id = Column(String, ForeignKey("classrooms.id"))
    classroom = relationship("Classroom", foreign_keys=[class_id])


class Student_attendance(Base):
    __tablename__ = "attendance"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    student_id = Column(String, ForeignKey("student.id"))
    is_present = Column(Boolean, default=False)
    remarks = Column(String)
    created_by = Column(String)  # email of the teacher who makrked the attendance


class EnrollmentRequest(Base):
    __tablename__ = "enrollment"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    student_id = Column(
        String, ForeignKey("student.id")
    )  # Define ForeignKey for relationship
    student_profile = relationship("Student")
    grade_level = Column(String)
    academic_year = Column(Integer)
    remarks = Column(String)


class AcademicHistory(Base):
    """Student or teacher can have multiple AcademicHistory."""

    __tablename__ = "academic_history"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    school_name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(String)
    grade_level = Column(String)
    reason_for_leaving = Column(String)
    classroom = Column(String)
    owner_id = Column(String, ForeignKey("appusers.id"))
    owner = relationship("Appuser", backref="academic_history")


# Additional model for assignment relationship (optional):
# class Class_Teacher(Base):
#     __tablename__ = "class_teacher"
#     id = Column(String, primary_key=True, index=True)
#     timestamp = Column(DateTime(), server_default=func.now())
#     classroom_id= Column(Integer, ForeignKey("classrooms.id"))  # ForeignKey to Classroom
#     teacher= Column(Integer, ForeignKey("appuser.id"))  # ForeignKey to Teacher
