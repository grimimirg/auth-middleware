from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json

@dataclass
class AuthenticateResponse:
    accessToken: str
    userId: Optional[int] = field(default=None)
    expiresOn: Optional[datetime] = field(default=None)
    refreshToken: str

    def toJson(self):
        return json.dumps({
            "access_token": self.accessToken,
            "user_id": self.userId,
            "expires_on": self.expiresOn.isoformat() if self.expiresOn else None,
            "refresh_token": self.refreshToken
        })

    def __str__(self):
        return (f"AuthenticateResponse(accessToken={self.accessToken}, userId={self.userId}, "
                f"expiresOn={self.expiresOn}, refreshToken={self.refreshToken})")
