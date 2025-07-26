from typing import List, Optional

cDict = {
    "Marketing and Sponsorships": "red",
    "Media and Public Relations": "blue",
    "Events and Logistics": "green",
    "Production": "purple",
    "Design": "orange",
    "Web and App Dev": "teal",
    "Registration Security and Planning": "yellow",
    "Hospitality": "pink",
}

class User:
    def __init__(self, uid: str, name:str , email: str, phoneNo: str, role: str, committee: Optional[str] = None) -> None:
        self.uid = uid
        self.name = name
        self.email = email
        self.phoneNo = phoneNo
        self.role = role.upper() # FC, Coord, Subcoord, IT Guy
        self.committee = committee
        self.colour = cDict[committee] # type: ignore
        self.children: List["User"] = []

    def addChild(self, user: "User"):
        self.children.append(user)

    def __repr__(self) -> str:
        return f"{self.role}: {self.name} ({self.uid})"
    

def build_user_tree(users: List[User]) -> List[User]:
    root_users: List[User] = []

    for user in users:
        if user.role == "SUBCORD":
            for parent in users:
                if parent.role == "COORD" and parent.colour == user.colour:
                    parent.addChild(user)
                    break
        elif user.role == "COORD":
            for parent in users:
                if parent.role == "FC":
                    parent.addChild(user)
                    break
        
        else:
            root_users.append(user) # type: ignore

    return root_users

