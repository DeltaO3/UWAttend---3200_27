from typing import List, Optional
from datetime import date, time
from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app import db

class User(db.Model) :
    userID: Mapped[int] = mapped_column(primary_key=True)
    uwaID: Mapped[int] = mapped_column(unique=True, nullable=False)
    firstName: Mapped[Optional[str]] = mapped_column(String(50))
    lastName: Mapped[Optional[str]] = mapped_column(String(50))
    passwordHash: Mapped[str] = mapped_column(String(256), nullable=False)
    type: Mapped[int] = mapped_column(nullable=False)   # 1 (admin), 2 (coordinator), 3 (facilitator)

    unitsCoordinate: Mapped[List['Unit']] = relationship(secondary='Units_Coordinators_Table', back_populates='coordinators')
    unitsFacilitate: Mapped[List['Unit']] = relationship(secondary='Units_Facilitators_Table', back_populates='facilitators')

class Unit(db.Model) :
    unitID: Mapped[int] = mapped_column(primary_key=True)
    unitCode: Mapped[str] = mapped_column(String(50), nullable=False)
    unitName: Mapped[Optional[str]] = mapped_column(String(50))
    studyPeriod: Mapped[str] = mapped_column(String(50), nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    startDate: Mapped[date] = mapped_column(nullable=False)
    endDate: Mapped[date] = mapped_column(nullable=False)

    coordinators: Mapped[List['User']] = relationship(secondary='Units_Coordinators_Table', back_populates='unitsCoordinate')
    facilitators: Mapped[List['User']] = relationship(secondary='Units_Facilitators_Table', back_populates='unitsFacilitate')
    students: Mapped[List['Student']] = relationship()

    sessionNames: Mapped[str] = mapped_column(String(2000), nullable=False)     # | separated string
    sessionTimes: Mapped[str] = mapped_column(String(2000), nullable=False)     # | separated string
    comments: Mapped[bool] = mapped_column(nullable=False)
    marks: Mapped[bool] = mapped_column(nullable=False)
    consent: Mapped[bool] = mapped_column(nullable=False)
    commentSuggestions: Mapped[Optional[str]] = mapped_column(String(2000))     # | separated string

class Student(db.Model) :
    studentID: Mapped[int] = mapped_column(primary_key=True)
    studentNumber: Mapped[int] = mapped_column(nullable=False)
    firstName: Mapped[str] = mapped_column(String(50), nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    preferredName: Mapped[str] = mapped_column(String(50), nullable=False)
    unitID: Mapped[int] = mapped_column(ForeignKey('unit.unitID'), nullable=False)
    consent: Mapped[int] = mapped_column(nullable=False)   # 0 (no), 1 (yes), -1 (consent not required)

class Session(db.Model) :
    sessionID: Mapped[int] = mapped_column(primary_key=True)
    unitID: Mapped[int] = mapped_column(ForeignKey('unit.unitID'), nullable=False)
    sessionName: Mapped[str] = mapped_column(String(50), nullable=False)
    sessionTime: Mapped[str] = mapped_column(String(50), nullable=False)
    sessionDate: Mapped[date] = mapped_column(nullable=False)

class Attendance(db.Model) :
    attendanceID: Mapped[int] = mapped_column(primary_key=True)
    sessionID: Mapped[int] = mapped_column(ForeignKey('session.sessionID'), nullable=False)
    studentID: Mapped[int] = mapped_column(ForeignKey('student.studentID'), nullable=False)
    signInTime: Mapped[time] = mapped_column(nullable=False)
    signOutTime: Mapped[time] = mapped_column()
    facilitatorID: Mapped[int] = mapped_column(ForeignKey('user.userID'), nullable=False)
    marks: Mapped[Optional[str]] = mapped_column(String(100))         # | separated string
    comments: Mapped[Optional[str]] = mapped_column(String(1000))     # | separated string
    consent_given: Mapped[int] = mapped_column(nullable=False)

class Base(DeclarativeBase):
    pass

Units_Coordinators_Table = Table(
    'Units_Coordinators_Table',
    Base.metadata,
    Column('userID', Integer, ForeignKey('user.userID'), primary_key=True),
    Column('unitID', Integer, ForeignKey('unit.unitID'), primary_key=True)
)

Units_Facilitators_Table = Table(
    'Units_Facilitators_Table',
    Base.metadata,
    Column('userID', Integer, ForeignKey('user.userID'), primary_key=True),
    Column('unitID', Integer, ForeignKey('unit.unitID'), primary_key=True)
)

