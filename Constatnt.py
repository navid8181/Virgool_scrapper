
from enum import Enum

BASE_URL = "https://virgool.io/api2/app/users"

class UserType(Enum):
    following = "following",
    followers = "followers"