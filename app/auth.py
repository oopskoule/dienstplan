from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/profil", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        new_password_confirm = request.form.get("new_password_confirm", "")

        if not check_password_hash(
            current_user.password_hash,
            current_password
        ):
            flash("Das aktuelle Passwort ist nicht korrekt.", "danger")
            return render_template("profile.html")

        if len(new_password) < 12:
            flash(
                "Das neue Passwort muss mindestens 12 Zeichen lang sein.",
                "danger",
            )
            return render_template("profile.html")

        if new_password != new_password_confirm:
            flash("Die neuen Passwörter stimmen nicht überein.", "danger")
            return render_template("profile.html")

        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        flash("Dein Passwort wurde erfolgreich geändert.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("profile.html")

