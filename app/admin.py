from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from app import db
from app.models import Admin, Project, Skill, Service


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = Admin.query.filter(
            (Admin.username == username_or_email) |
            (Admin.email == username_or_email)
        ).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template(
        "admin/login.html"
    )


@admin.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("admin.login")
    )


@admin.route("/")
@login_required
def dashboard():

    projects_count = Project.query.count()
    skills_count = Skill.query.count()
    services_count = Service.query.count()

    return render_template(
        "admin/dashboard.html",
        projects_count=projects_count,
        skills_count=skills_count,
        services_count=services_count
    )


@admin.route("/projects")
@login_required
def projects():
    project_list = Project.query.order_by(Project.created_at.desc()).all()

    return render_template(
        "admin/projects.html",
        projects=project_list
    )


@admin.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():

    if request.method == "POST":
        project = Project(
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            category=request.form.get("category", "").strip() or None,
            technologies=request.form.get("technologies", "").strip() or None,
            github_url=request.form.get("github_url", "").strip() or None,
            live_url=request.form.get("live_url", "").strip() or None,
            image=request.form.get("image", "").strip() or None,
        )

        db.session.add(project)
        db.session.commit()

        flash("Project created successfully.", "success")
        return redirect(url_for("admin.projects"))

    return render_template(
        "admin/project_form.html",
        project=None,
        action="Create"
    )


@admin.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        project.title = request.form.get("title", "").strip()
        project.description = request.form.get("description", "").strip()
        project.category = request.form.get("category", "").strip() or None
        project.technologies = request.form.get("technologies", "").strip() or None
        project.github_url = request.form.get("github_url", "").strip() or None
        project.live_url = request.form.get("live_url", "").strip() or None
        project.image = request.form.get("image", "").strip() or None

        db.session.commit()

        flash("Project updated successfully.", "success")
        return redirect(url_for("admin.projects"))

    return render_template(
        "admin/project_form.html",
        project=project,
        action="Edit"
    )


@admin.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully.", "success")
    return redirect(url_for("admin.projects"))


@admin.route("/skills")
@login_required
def skills():
    skill_list = Skill.query.order_by(Skill.created_at.desc()).all()

    return render_template(
        "admin/skills.html",
        skills=skill_list
    )


@admin.route("/skills/new", methods=["GET", "POST"])
@login_required
def new_skill():

    if request.method == "POST":
        skill = Skill(
            name=request.form.get("name", "").strip(),
            category=request.form.get("category", "").strip() or None,
        )

        db.session.add(skill)
        db.session.commit()

        flash("Skill created successfully.", "success")
        return redirect(url_for("admin.skills"))

    return render_template(
        "admin/skill_form.html",
        skill=None,
        action="Create"
    )


@admin.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if request.method == "POST":
        skill.name = request.form.get("name", "").strip()
        skill.category = request.form.get("category", "").strip() or None

        db.session.commit()

        flash("Skill updated successfully.", "success")
        return redirect(url_for("admin.skills"))

    return render_template(
        "admin/skill_form.html",
        skill=skill,
        action="Edit"
    )


@admin.route("/skills/<int:skill_id>/delete", methods=["POST"])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()

    flash("Skill deleted successfully.", "success")
    return redirect(url_for("admin.skills"))


@admin.route("/services")
@login_required
def services():
    service_list = Service.query.order_by(Service.created_at.desc()).all()

    return render_template(
        "admin/services.html",
        services=service_list
    )


@admin.route("/services/new", methods=["GET", "POST"])
@login_required
def new_service():

    if request.method == "POST":
        service = Service(
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
        )

        db.session.add(service)
        db.session.commit()

        flash("Service created successfully.", "success")
        return redirect(url_for("admin.services"))

    return render_template(
        "admin/service_form.html",
        service=None,
        action="Create"
    )


@admin.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        service.title = request.form.get("title", "").strip()
        service.description = request.form.get("description", "").strip()

        db.session.commit()

        flash("Service updated successfully.", "success")
        return redirect(url_for("admin.services"))

    return render_template(
        "admin/service_form.html",
        service=service,
        action="Edit"
    )


@admin.route("/services/<int:service_id>/delete", methods=["POST"])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()

    flash("Service deleted successfully.", "success")
    return redirect(url_for("admin.services"))