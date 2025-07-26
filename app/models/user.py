from typing import List, Optional, Any, TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, EmailStr

if TYPE_CHECKING:
    from pydantic import ValidationInfo

from ..utils.enums import UserRole, Committee, CommitteeColor, COMMITTEE_COLOR_MAP

class User(BaseModel):
    uid: str = Field(..., description="Unique user identifier")
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address")
    phoneNo: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$', description="Phone number")
    role: UserRole = Field(..., description="User role in the organization")
    committee: Optional[Committee] = Field(None, description="Committee assignment")
    colour: Optional[CommitteeColor] = Field(None, description="Committee color assignment")
    children: List['User'] = Field(default_factory=list, description="Child users in hierarchy") # type: ignore

    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "uid": "firebase_uid_123",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phoneNo": "+1234567890",
                "role": "COORD",
                "committee": "Web and App Dev",
                "colour": "teal",
                "children": []
            }
        }
    }

    @field_validator('colour', mode='before')
    @classmethod
    def set_colour_from_committee(cls, v: Any, info: 'ValidationInfo') -> Any:
        """Automatically set colour based on committee"""
        if v is None and hasattr(info, 'data') and info.data:
            committee = info.data.get('committee')
            if committee and committee in COMMITTEE_COLOR_MAP:
                return COMMITTEE_COLOR_MAP[committee]
        return v

    def addChild(self, user: "User") -> None:
        """Add a child user to this user's hierarchy"""
        self.children.append(user)

    def __repr__(self) -> str:
        return f"{self.role.value}: {self.name} ({self.uid})"

# Update forward reference
User.model_rebuild()
    

def build_user_tree(users: List[User]) -> List[User]:
    """
    Build a hierarchical tree structure from a flat list of users.
    
    Hierarchy: FC -> COORD -> SUBCORD
    Users are grouped by committee colors for COORD and SUBCORD relationships.
    
    Args:
        users: List of User objects
        
    Returns:
        List of root users (FC and users without parents)
    """
    root_users: List[User] = []

    for user in users:
        if user.role == UserRole.SUBCORD:
            # Find parent COORD with same committee color
            for parent in users:
                if parent.role == UserRole.COORD and parent.colour == user.colour:
                    parent.addChild(user)
                    break
        elif user.role == UserRole.COORD:
            # Find parent FC
            for parent in users:
                if parent.role == UserRole.FC:
                    parent.addChild(user)
                    break
        else:
            # FC and other roles are root users
            root_users.append(user)

    return root_users

