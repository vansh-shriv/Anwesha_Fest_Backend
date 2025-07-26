from typing import List, Optional
from pydantic import BaseModel, Field
from ..utils.enums import Committee, CommitteeColor, COMMITTEE_COLOR_MAP

class CommitteeStats(BaseModel):
    """Statistics for a committee"""
    total_members: int = Field(default=0, ge=0, description="Total number of committee members")
    coordinators: int = Field(default=0, ge=0, description="Number of coordinators")
    sub_coordinators: int = Field(default=0, ge=0, description="Number of sub-coordinators")
    active_meets: int = Field(default=0, ge=0, description="Number of active meetings")
    completed_meets: int = Field(default=0, ge=0, description="Number of completed meetings")

class CommitteeMember(BaseModel):
    """Individual committee member information"""
    uid: str = Field(..., description="User ID")
    name: str = Field(..., description="Member name")
    role: str = Field(..., description="Role in committee (COORD/SUBCORD)")
    email: str = Field(..., description="Member email")
    joined_date: Optional[str] = Field(None, description="Date joined committee")

class CommitteeBase(BaseModel):
    """Base committee model"""
    name: Committee = Field(..., description="Committee name")
    description: Optional[str] = Field(None, max_length=500, description="Committee description")
    
class CommitteeCreate(CommitteeBase):
    """Model for creating committee (though committees are predefined)"""
    pass

class CommitteeUpdate(BaseModel):
    """Model for updating committee information"""
    description: Optional[str] = Field(None, max_length=500, description="Committee description")

class CommitteeInfo(CommitteeBase):
    """Complete committee information with members and stats"""
    colour: CommitteeColor = Field(..., description="Committee color")
    stats: CommitteeStats = Field(default_factory=lambda: CommitteeStats(), description="Committee statistics")
    members: List[CommitteeMember] = Field(default_factory=list, description="Committee members") # type: ignore
    coordinator_ids: List[str] = Field(default_factory=list, description="List of coordinator UIDs")
    sub_coordinator_ids: List[str] = Field(default_factory=list, description="List of sub-coordinator UIDs")
    
    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "name": "Web and App Dev",
                "description": "Responsible for website and mobile app development",
                "colour": "teal",
                "stats": {
                    "total_members": 5,
                    "coordinators": 1,
                    "sub_coordinators": 2,
                    "active_meets": 3,
                    "completed_meets": 10
                },
                "members": [
                    {
                        "uid": "user_123",
                        "name": "John Doe",
                        "role": "COORD",
                        "email": "john@example.com",
                        "joined_date": "2025-01-01"
                    }
                ],
                "coordinator_ids": ["user_123"],
                "sub_coordinator_ids": ["user_456", "user_789"]
            }
        }
    }
    
    @classmethod
    def create_from_committee(cls, committee: Committee, description: Optional[str] = None) -> "CommitteeInfo":
        """Create CommitteeInfo from Committee enum with default color"""
        return cls(
            name=committee,
            description=description,
            colour=COMMITTEE_COLOR_MAP[committee]
        )

class CommitteeResponse(CommitteeInfo):
    """Committee response with additional computed fields"""
    can_manage: bool = Field(False, description="Whether current user can manage this committee")
    is_member: bool = Field(False, description="Whether current user is a member")
    user_role_in_committee: Optional[str] = Field(None, description="Current user's role in this committee")
    
    @classmethod
    def from_committee_info(cls, committee_info: CommitteeInfo, user_id: str, user_role: str) -> "CommitteeResponse":
        """Create CommitteeResponse with user-specific permissions"""
        is_coordinator = user_id in committee_info.coordinator_ids
        is_sub_coordinator = user_id in committee_info.sub_coordinator_ids
        is_member = is_coordinator or is_sub_coordinator
        
        user_role_in_committee = None
        if is_coordinator:
            user_role_in_committee = "COORD"
        elif is_sub_coordinator:
            user_role_in_committee = "SUBCORD"
        
        return cls(
            **committee_info.model_dump(),
            can_manage=user_role == "FC" or is_coordinator,
            is_member=is_member,
            user_role_in_committee=user_role_in_committee
        )

def get_all_committees() -> List[CommitteeInfo]:
    """Get information for all predefined committees"""
    committees = []
    
    # Committee descriptions
    descriptions = {
        Committee.MARKETING_SPONSORSHIPS: "Handle marketing campaigns and sponsor relationships",
        Committee.MEDIA_PR: "Manage media coverage and public relations",
        Committee.EVENTS_LOGISTICS: "Organize events and handle logistics",
        Committee.PRODUCTION: "Handle technical production and equipment",
        Committee.DESIGN: "Create visual designs and branding materials",
        Committee.WEB_APP_DEV: "Develop and maintain website and mobile applications",
        Committee.REGISTRATION_SECURITY: "Manage registrations and security protocols",
        Committee.HOSPITALITY: "Handle guest relations and hospitality services"
    }
    
    for committee in Committee:
        committee_info = CommitteeInfo.create_from_committee(
            committee, 
            descriptions.get(committee)
        )
        committees.append(committee_info) # type: ignore
    
    return committees # pyright: ignore[reportUnknownVariableType]
