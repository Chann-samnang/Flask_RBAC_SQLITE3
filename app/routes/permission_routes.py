from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.permission_forms import PermissionForm
from app.services.permission_service import PermissionService

permission_bp = Blueprint("permissions", __name__, url_prefix="/permissions")

@permission_bp.route("/")
def index():
    permissions = PermissionService.get_all()
    return render_template("permissions/index.html", permissions=permissions)

@permission_bp.route("/create", methods=["GET", "POST"])
def create():
    form = PermissionForm()
    if form.validate_on_submit():
        PermissionService.create(form.data)
        flash("Permission created successfully.", "success")
        return redirect(url_for("permissions.index"))
    return render_template("permissions/create.html", form=form)

@permission_bp.route("/<int:permission_id>/detail")
def detail(permission_id):
    permission = PermissionService.get_by_id(permission_id)
    return render_template("permissions/detail.html", permission=permission)

@permission_bp.route("/<int:permission_id>/edit", methods=["GET", "POST"])
def edit(permission_id):
    permission = PermissionService.get_by_id(permission_id)
    form = PermissionForm(obj=permission)
    if form.validate_on_submit():
        PermissionService.update(permission, form.data)
        flash("Permission updated.", "success")
        return redirect(url_for("permissions.index"))
    return render_template("permissions/edit.html", form=form)

@permission_bp.route("/<int:permission_id>/delete-confirm", methods=["GET"])
def delete_confirm(permission_id):
    permission = PermissionService.get_by_id(permission_id)
    form = PermissionForm()
    return render_template("permissions/delete_confirm.html", permission=permission, form=form)

@permission_bp.route("/<int:permission_id>/delete", methods=["POST"])
def delete(permission_id):
    permission = PermissionService.get_by_id(permission_id)
    PermissionService.delete(permission)
    flash("Permission deleted.", "success")
    return redirect(url_for("permissions.index"))
