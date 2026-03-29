import json
from app.config import settings


def validate_friend_password(password: str) -> str | None:
    """
    Validate the friend password and return the friend_id if valid.
    Returns None if password is invalid.
    """
    friend_passwords = settings.friend_passwords

    # Try JSON format first
    try:
        mapping = json.loads(friend_passwords)
        if isinstance(mapping, dict):
            for friend_id, pwd in mapping.items():
                if pwd == password:
                    return friend_id
    except json.JSONDecodeError:
        pass

    # Try comma-separated format: "friend1:pass1,friend2:pass2"
    pairs = friend_passwords.split(",")
    for pair in pairs:
        if ":" in pair:
            friend_id, pwd = pair.split(":", 1)
            if pwd == password:
                return friend_id.strip()

    return None
