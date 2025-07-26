from enum import Enum

class UserRole(str, Enum):
    """User roles in the organization hierarchy"""
    FC = "FC"
    COORD = "COORD"
    SUBCORD = "SUBCORD"
    IT_GUY = "IT_GUY"

class Committee(str, Enum):
    """Available committees in the organization"""
    MARKETING_SPONSORSHIPS = "Marketing and Sponsorships"
    MEDIA_PR = "Media and Public Relations"
    EVENTS_LOGISTICS = "Events and Logistics"
    PRODUCTION = "Production"
    DESIGN = "Design"
    WEB_APP_DEV = "Web and App Dev"
    REGISTRATION_SECURITY = "Registration Security and Planning"
    HOSPITALITY = "Hospitality"

class CommitteeColor(str, Enum):
    """Colors assigned to committees for identification"""
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    ORANGE = "orange"
    TEAL = "teal"
    YELLOW = "yellow"
    PINK = "pink"

# Mapping committees to their assigned colors
COMMITTEE_COLOR_MAP = {
    Committee.MARKETING_SPONSORSHIPS: CommitteeColor.RED,
    Committee.MEDIA_PR: CommitteeColor.BLUE,
    Committee.EVENTS_LOGISTICS: CommitteeColor.GREEN,
    Committee.PRODUCTION: CommitteeColor.PURPLE,
    Committee.DESIGN: CommitteeColor.ORANGE,
    Committee.WEB_APP_DEV: CommitteeColor.TEAL,
    Committee.REGISTRATION_SECURITY: CommitteeColor.YELLOW,
    Committee.HOSPITALITY: CommitteeColor.PINK,
}

class MeetType(str, Enum):
    """Types of meetings"""
    GENERAL = "general"
    COMMITTEE = "committee"
    EMERGENCY = "emergency"
    ONE_ON_ONE = "one_on_one"

class MeetStatus(str, Enum):
    """Meeting status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
