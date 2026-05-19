from enum import Enum


class EventMatchType(str, Enum):
    SINGLE = "SINGLE"
    TOURNAMENT = "TOURNAMENT"


class EventStatus(str, Enum):
    CREATED = "CREATED"
    REGISTRATION = "REGISTRATION"
    IDLE = "IDLE"
    FORMATION = "FORMATION"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TeamFormation(str, Enum):
    DRAFT = "DRAFT"
    BALANCE = "BALANCE"
    MANUAL = "MANUAL"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAITLIST = "WAITLIST"


class EventPlayerStatus(str, Enum):
    REGISTERED = "REGISTERED"
    SELECTED = "SELECTED"
    PLAYING = "PLAYING"
    COMPLETED = "COMPLETED"
    BENCHED = "BENCHED"


class DraftStatus(str, Enum):
    OPEN = "OPEN"
    BALANCE_REQUESTED = "BALANCE_REQUESTED"
    BALANCE_SELECTED = "BALANCE_SELECTED"
    COMPLETED = "COMPLETED"
