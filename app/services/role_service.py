from typing import List, Optional, Dict
from extensions import db
from app.models.role import Role
from app.models.permission import Permission

class RoleService:
    @staticmethod
    def get_all() -> List[Role]:
        """Return all roles ordered by newest first."""
        return Role.query.order_by(Role.id.desc()).all()

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        """Return a role by its ID."""
        return Role.query.get(role_id)

    @staticmethod
    def create(data: Dict) -> Role:
        """Create a new role with selected permissions."""
        role = Role(
            name=data["name"],
            description=data.get("description")
        )

        # Attach permissions if provided
        if "permissions" in data and data["permissions"]:
            role.permissions = Permission.query.filter(
                Permission.code.in_(data["permissions"])
            ).all()

        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def update(role: Role, data: Dict) -> Role:
        """Update an existing role and its permissions."""
        role.name = data["name"]
        role.description = data.get("description")

        # Update permissions
        if "permissions" in data:
            role.permissions = Permission.query.filter(
                Permission.code.in_(data["permissions"])
            ).all()

        db.session.commit()
        return role

    @staticmethod
    def delete(role: Role) -> None:
        """Delete a role."""
        db.session.delete(role)
        db.session.commit()
