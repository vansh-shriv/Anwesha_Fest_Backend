# Import all models to make them available from app.models
from .user import User, build_user_tree
from .meet import (
    Meet, 
    MeetCreate, 
    MeetUpdate, 
    MeetResponse,
    MeetBase
)
from .committee import (
    CommitteeInfo,
    CommitteeResponse, 
    CommitteeStats,
    CommitteeMember,
    CommitteeCreate,
    CommitteeUpdate,
    get_all_committees
)

# Define what gets imported with "from app.models import *"
__all__ = [
    # User models
    "User",
    "build_user_tree",
    
    # Meet models
    "Meet",
    "MeetCreate",
    "MeetUpdate", 
    "MeetResponse",
    "MeetBase",
    
    # Committee models
    "CommitteeInfo",
    "CommitteeResponse",
    "CommitteeStats", 
    "CommitteeMember",
    "CommitteeCreate",
    "CommitteeUpdate",
    "get_all_committees"
]
