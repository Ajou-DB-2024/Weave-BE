from dataclasses import dataclass

@dataclass
class GoogleOAuthToken:
  access_token: str
  expires_in: int
  refresh_token: str
