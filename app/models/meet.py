from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from ..utils.enums import MeetType, MeetStatus

class MeetBase(BaseModel):
    """Base meet model with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Meeting title")
    description: Optional[str] = Field(None, max_length=1000, description="Meeting description")
    scheduled_time: datetime = Field(..., description="Scheduled meeting time")
    duration_minutes: int = Field(60, ge=15, le=480, description="Meeting duration in minutes (15-480)")
    meet_type: MeetType = Field(MeetType.GENERAL, description="Type of meeting")
    location: Optional[str] = Field(None, max_length=200, description="Meeting location")
    is_virtual: bool = Field(False, description="Whether the meeting is virtual")
    meeting_link: Optional[str] = Field(None, description="Virtual meeting link")

class MeetCreate(MeetBase):
    """Model for creating a new meeting"""
    attendee_ids: List[str] = Field(default_factory=list, description="List of attendee UIDs")

class MeetUpdate(BaseModel):
    """Model for updating meeting information"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    location: Optional[str] = Field(None, max_length=200)
    is_virtual: Optional[bool] = None
    meeting_link: Optional[str] = None
    status: Optional[MeetStatus] = None

class Meet(MeetBase):
    """Complete meeting model"""
    meet_id: str = Field(..., description="Unique meeting identifier")
    created_by: str = Field(..., description="UID of the user who created the meeting")
    created_at: datetime = Field(default_factory=datetime.now, description="Meeting creation timestamp")
    status: MeetStatus = Field(MeetStatus.SCHEDULED, description="Current meeting status")
    attendee_ids: List[str] = Field(default_factory=list, description="List of attendee UIDs")
    actual_attendees: List[str] = Field(default_factory=list, description="List of users who actually attended")
    notes: Optional[str] = Field(None, description="Meeting notes")
    
    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "meet_id": "meet_123",
                "title": "Weekly Committee Meeting",
                "description": "Discussion about upcoming events",
                "scheduled_time": "2025-01-15T10:00:00Z",
                "duration_minutes": 60,
                "meet_type": "committee",
                "location": "Conference Room A",
                "is_virtual": False,
                "meeting_link": None,
                "created_by": "user_123",
                "status": "scheduled",
                "attendee_ids": ["user_123", "user_456"],
                "actual_attendees": [],
                "notes": None
            }
        }
    }

class MeetResponse(Meet):
    """Meeting response model with additional computed fields"""
    can_edit: bool = Field(False, description="Whether current user can edit this meeting")
    can_join: bool = Field(False, description="Whether current user can join this meeting")
    
    @classmethod
    def from_meet(cls, meet: Meet, user_id: str) -> "MeetResponse":
        """Create MeetResponse from Meet with user-specific permissions"""
        return cls(
            **meet.model_dump(),
            can_edit=meet.created_by == user_id,
            can_join=user_id in meet.attendee_ids
        )
