from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.user_forms import UserCreateForm, UserEditForm, ConfirmDeleteForm
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/")
def index():
    users = UserService.get_all()
    return render_template("users/index.html", users=users)

@user_bp.route("/<int:id>")
def detail(id):
    user = UserService.get_by_id(id)
    return render_template("users/detail.html", user=user)

@user_bp.route("/create", methods=["GET", "POST"])
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
            "password": form.password.data,
        }
        UserService.create(data)
        flash("User successfully created!", "success")
        return redirect(url_for("users.index"))
    return render_template("users/create.html", form=form)

@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    form = UserEditForm(original_user=user, obj=user)
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data or None
        UserService.update(user, data, password=password)
        flash("User was updated successfully.", "success")
        return redirect(url_for("users.detail", id=user.id))
    return render_template("users/edit.html", form=form)

# Two-step delete flow: confirm page (GET) + delete action (POST)
@user_bp.route("/<int:user_id>/delete-confirm", methods=["GET"])
def delete_confirm(user_id: int):
    user = UserService.get_by_id(user_id)
    form = ConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user, form=form)

@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id: int):
    user = UserService.get_by_id(user_id)
    form = ConfirmDeleteForm()
    if form.validate_on_submit():
        UserService.delete(user)
        flash("User was deleted successfully.", "success")
        return redirect(url_for("users.index"))
    return render_template("users/delete_confirm.html", user=user, form=form)
