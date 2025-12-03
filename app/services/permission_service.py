from typing import List, Optional, Dict
from extensions import db
from app.models.permission import Permission

class PermissionService:
    @staticmethod
    def get_all() -> List[Permission]:
        """Return all permissions ordered by newest first."""
        return Permission.query.order_by(Permission.id.desc()).all()

    @staticmethod
    def get_by_id(permission_id: int) -> Optional[Permission]:
        """Return a permission by its ID."""
        return Permission.query.get(permission_id)

    @staticmethod
    def create(data: Dict) -> Permission:
        """Create a new permission."""
        permission = Permission(
            code=data["code"],
            name=data["name"],
            module=data["module"],
            description=data.get("description")
        )
        db.session.add(permission)
        db.session.commit()
        return permission

    @staticmethod
    def update(permission: Permission, data: Dict) -> Permission:
        """Update an existing permission."""
        permission.code = data["code"]
        permission.name = data["name"]
        permission.module = data["module"]
        permission.description = data.get("description")
        db.session.commit()
        return permission

    @staticmethod
    def delete(permission: Permission) -> None:
        """Delete a permission."""
        db.session.delete(permission)
        db.session.commit()

    @staticmethod
    def get_choices() -> List[tuple]:
        """Return choices for forms as (code, name)."""
        return [(p.code, p.name) for p in Permission.query.order_by(Permission.code).all()]
