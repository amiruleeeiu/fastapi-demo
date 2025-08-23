from app.models.user import User


def has_role(user: User, roles: list[str]) -> bool:
    return any(role in user.roles for role in roles)