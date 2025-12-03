# app/routes/role_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.role_forms import RoleForm
from app.services.role_service import RoleService
from app.services.permission_service import PermissionService

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.route("/")
def index():
    roles = RoleService.get_all()
    return render_template("roles/index.html", roles=roles)

@role_bp.route("/create", methods=["GET", "POST"])
def create():
    form = RoleForm()
    form.permissions.choices = PermissionService.get_choices()
    if form.validate_on_submit():
        RoleService.create(form.data)
        flash("Role created successfully.", "success")
        return redirect(url_for("roles.index"))
    return render_template("roles/create.html", form=form)

@role_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
def edit(role_id):
    role = RoleService.get_by_id(role_id)
    form = RoleForm(obj=role)
    form.permissions.choices = PermissionService.get_choices()
    form.permissions.data = [p.code for p in role.permissions]
    if form.validate_on_submit():
        RoleService.update(role, form.data)
        flash("Role updated.", "success")
        return redirect(url_for("roles.index"))
    return render_template("roles/edit.html", form=form)

@role_bp.route("/<int:role_id>/delete-confirm", methods=["GET"])
def delete_confirm(role_id):
    role = RoleService.get_by_id(role_id)
    form = RoleForm()
    return render_template("roles/delete_confirm.html", role=role, form=form)

@role_bp.route("/<int:role_id>/delete", methods=["POST"])
def delete(role_id):
    role = RoleService.get_by_id(role_id)
    RoleService.delete(role)
    flash("Role deleted.", "success")
    return redirect(url_for("roles.index"))
