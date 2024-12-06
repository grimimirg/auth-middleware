from dataclasses import dataclass
from typing import Collection, Optional
from user import User

@dataclass
class AuthenticatedUser:
    username: str
    token: str
    user: User
    authorities: Collection[str]
    
    def isAccountNonExpired(self) -> bool:
        return True

    def isAccountNonLocked(self) -> bool:
        return True

    def isCredentialsNonExpired(self) -> bool:
        return True

    def isEnabled(self) -> bool:
        return True

    def getPassword(self) -> Optional[str]:
        return None

    def getAuthorities(self) -> Collection[str]:
        return self.authorities

    def getCappUser(self) -> User:
        return self.user

    def __str__(self):
        return (f"AuthenticatedUser(username={self.username}, token={self.token}, "
                f"user={self.user}, authorities={self.authorities})")
