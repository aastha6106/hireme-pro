import re
import pdfkit
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, abort, current_app, make_response,
)
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Resume, Education, Experience, Skill

main = Blueprint("main", __name__)


def get_user_resume(resume_id):
    resume = db.session.get(Resume, resume_id)
    if resume is None:
        abort(404)
    if resume.user_id != current_user.id:
        abort(403)
    return resume


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("main.register"))

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return redirect(url_for("main.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(url_for("main.register"))

        if password != confirm:
            flash("Passwords do not match.", "error")
            return redirect(url_for("main.register"))

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=username).first():
            flash("That username is taken.", "error")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome to HireMe Pro.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for("main.login"))

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("main.login"))

        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.dashboard"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))


@main.route("/dashboard")
@login_required
def dashboard():
    resumes = (
        Resume.query
        .filter_by(user_id=current_user.id)
        .order_by(Resume.updated_at.desc())
        .all()
    )
    return render_template("dashboard.html", resumes=resumes)


@main.route("/resume/new", methods=["GET", "POST"])
@login_required
def create_resume():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()

        if not title:
            flash("Your resume needs a title.", "error")
            return redirect(url_for("main.create_resume"))

        resume = Resume(title=title, summary=summary, user_id=current_user.id)
        db.session.add(resume)
        db.session.commit()

        flash("Resume created.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("resume_form.html", resume=None)


@main.route("/resume/<int:id>")
@login_required
def resume_detail(id):
    resume = get_user_resume(id)
    return render_template("resume_detail.html", resume=resume)


@main.route("/resume/<int:id>/builder", methods=["GET", "POST"])
@login_required
def builder(id):
    resume = get_user_resume(id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()

        if not title:
            flash("Title cannot be empty.", "error")
            return redirect(url_for("main.builder", id=id))

        resume.title = title
        resume.summary = summary
        db.session.commit()

        flash("Resume saved.", "success")
        return redirect(url_for("main.builder", id=id))

    return render_template("resume_edit.html", resume=resume)


@main.route("/resume/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_resume(id):
    resume = get_user_resume(id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()

        if not title:
            flash("Title cannot be empty.", "error")
            return redirect(url_for("main.edit_resume", id=id))

        resume.title = title
        resume.summary = summary
        db.session.commit()

        flash("Resume updated.", "success")
        return redirect(url_for("main.builder", id=id))

    return render_template("resume_form.html", resume=resume)


@main.route("/resume/<int:id>/delete", methods=["POST"])
@login_required
def delete_resume(id):
    resume = get_user_resume(id)
    db.session.delete(resume)
    db.session.commit()
    flash("Resume deleted.", "success")
    return redirect(url_for("main.dashboard"))


# ---- Education ----

@main.route("/resume/<int:resume_id>/education/add", methods=["GET", "POST"])
@login_required
def add_education(resume_id):
    resume = get_user_resume(resume_id)

    if request.method == "POST":
        school = request.form.get("school", "").strip()
        degree = request.form.get("degree", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        description = request.form.get("description", "").strip()

        if not school:
            flash("School name is required.", "error")
            return redirect(url_for("main.add_education", resume_id=resume_id))

        entry = Education(
            resume_id=resume.id,
            school=school,
            degree=degree,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        db.session.add(entry)
        db.session.commit()

        flash("Education added.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("education_form.html", resume=resume, entry=None)


@main.route("/education/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_education(id):
    entry = db.session.get(Education, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    if request.method == "POST":
        school = request.form.get("school", "").strip()
        degree = request.form.get("degree", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        description = request.form.get("description", "").strip()

        if not school:
            flash("School name is required.", "error")
            return redirect(url_for("main.edit_education", id=id))

        entry.school = school
        entry.degree = degree
        entry.start_date = start_date
        entry.end_date = end_date
        entry.description = description
        db.session.commit()

        flash("Education updated.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("education_form.html", resume=resume, entry=entry)


@main.route("/education/<int:id>/delete", methods=["POST"])
@login_required
def delete_education(id):
    entry = db.session.get(Education, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    db.session.delete(entry)
    db.session.commit()

    flash("Education removed.", "success")
    return redirect(url_for("main.builder", id=resume.id))


# ---- Experience ----

@main.route("/resume/<int:resume_id>/experience/add", methods=["GET", "POST"])
@login_required
def add_experience(resume_id):
    resume = get_user_resume(resume_id)

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        description = request.form.get("description", "").strip()

        if not company or not role:
            flash("Company and role are required.", "error")
            return redirect(url_for("main.add_experience", resume_id=resume_id))

        entry = Experience(
            resume_id=resume.id,
            company=company,
            role=role,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        db.session.add(entry)
        db.session.commit()

        flash("Experience added.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("experience_form.html", resume=resume, entry=None)


@main.route("/experience/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_experience(id):
    entry = db.session.get(Experience, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        description = request.form.get("description", "").strip()

        if not company or not role:
            flash("Company and role are required.", "error")
            return redirect(url_for("main.edit_experience", id=id))

        entry.company = company
        entry.role = role
        entry.start_date = start_date
        entry.end_date = end_date
        entry.description = description
        db.session.commit()

        flash("Experience updated.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("experience_form.html", resume=resume, entry=entry)


@main.route("/experience/<int:id>/delete", methods=["POST"])
@login_required
def delete_experience(id):
    entry = db.session.get(Experience, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    db.session.delete(entry)
    db.session.commit()

    flash("Experience removed.", "success")
    return redirect(url_for("main.builder", id=resume.id))


# ---- Skills ----

@main.route("/resume/<int:resume_id>/skill/add", methods=["GET", "POST"])
@login_required
def add_skill(resume_id):
    resume = get_user_resume(resume_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        level = request.form.get("level", "").strip()

        if not name:
            flash("Skill name is required.", "error")
            return redirect(url_for("main.add_skill", resume_id=resume_id))

        entry = Skill(resume_id=resume.id, name=name, level=level)
        db.session.add(entry)
        db.session.commit()

        flash("Skill added.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("skill_form.html", resume=resume, entry=None)


@main.route("/skill/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_skill(id):
    entry = db.session.get(Skill, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        level = request.form.get("level", "").strip()

        if not name:
            flash("Skill name is required.", "error")
            return redirect(url_for("main.edit_skill", id=id))

        entry.name = name
        entry.level = level
        db.session.commit()

        flash("Skill updated.", "success")
        return redirect(url_for("main.builder", id=resume.id))

    return render_template("skill_form.html", resume=resume, entry=entry)


@main.route("/skill/<int:id>/delete", methods=["POST"])
@login_required
def delete_skill(id):
    entry = db.session.get(Skill, id)
    if entry is None:
        abort(404)

    resume = get_user_resume(entry.resume_id)

    db.session.delete(entry)
    db.session.commit()

    flash("Skill removed.", "success")
    return redirect(url_for("main.builder", id=resume.id))


# ---- PDF Download ----

@main.route("/resume/<int:id>/download")
@login_required
def download_resume(id):
    resume = get_user_resume(id)

    html = render_template("resume_pdf.html", resume=resume)

    try:
        wkhtmltopdf_path = current_app.config.get("WKHTMLTOPDF_PATH")
        if wkhtmltopdf_path:
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            config = pdfkit.configuration()

        options = {
            "page-size": "Letter",
            "margin-top": "0.6in",
            "margin-right": "0.7in",
            "margin-bottom": "0.6in",
            "margin-left": "0.7in",
            "encoding": "UTF-8",
            "no-outline": None,
            "enable-local-file-access": None,
        }

        pdf = pdfkit.from_string(html, False, options=options, configuration=config)

        safe_title = re.sub(r"[^\w\s-]", "", resume.title).strip()
        safe_title = re.sub(r"\s+", "_", safe_title)
        filename = f"{safe_title}_Resume.pdf" if safe_title else "Resume.pdf"

        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception:
        flash("PDF generation is not available on this server.", "error")
        return redirect(url_for("main.resume_detail", id=id))