# backend/app/models.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .db import Base

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Patient(Base, TimestampMixin):
    __tablename__ = "patients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(String(32), nullable=True)
    sex = Column(String(16), nullable=True)
    notes = Column(Text, nullable=True)
    scans = relationship("Scan", back_populates="patient", cascade="all, delete-orphan")

class Scan(Base, TimestampMixin):
    __tablename__ = "scans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    body_part = Column(String(64), nullable=False)
    modality = Column(String(32), nullable=False)
    image_path = Column(String(1024), nullable=True)
    scan_metadata = Column(JSON, nullable=True)
    patient = relationship("Patient", back_populates="scans")
    predictions = relationship("Prediction", back_populates="scan", cascade="all, delete-orphan")

class Prediction(Base, TimestampMixin):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"), nullable=False)
    label = Column(String(128), nullable=False)
    probabilities = Column(JSON, nullable=True)
    uncertainty = Column(JSON, nullable=True)
    nl_explanation = Column(Text, nullable=True)
    xai = Column(JSON, nullable=True)
    scan = relationship("Scan", back_populates="predictions")

class ClinicianFeedback(Base, TimestampMixin):
    __tablename__ = "clinician_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id"), nullable=False)
    clinician_id = Column(String(128), nullable=True)
    override_label = Column(String(128), nullable=True)
    notes = Column(Text, nullable=True)

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(32), nullable=False, default="clinician")  # clinician, admin, researcher