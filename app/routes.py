from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, CampaignForm, AdRequestForm
from .models import db, User, Campaign, AdRequest

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data:
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password_hash=form.password.data,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registration successful!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("register.html", form=form)


@bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "sponsor":
        campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
        return render_template("dashboard.html", campaigns=campaigns)
    elif current_user.role == "influencer":
        ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
        return render_template("dashboard.html", ad_requests=ad_requests)
    elif current_user.role == "admin":
        users = User.query.all()
        campaigns = Campaign.query.all()
        ad_requests = AdRequest.query.all()
        return render_template(
            "dashboard.html", users=users, campaigns=campaigns, ad_requests=ad_requests
        )


@bp.route("/create_campaign", methods=["GET", "POST"])
@login_required
def create_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data,
            sponsor_id=current_user.id,
        )
        db.session.add(campaign)
        db.session.commit()
        flash("Campaign created successfully!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("campaign.html", form=form)


@bp.route("/create_ad_request/<int:campaign_id>", methods=["GET", "POST"])
@login_required
def create_ad_request(campaign_id):
    form = AdRequestForm()
    form.influencer_id.choices = [
        (user.id, user.username)
        for user in User.query.filter_by(role="influencer").all()
    ]

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_id=form.influencer_id.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status="Pending",
        )
        db.session.add(ad_request)
        db.session.commit()
        flash("Ad request sent successfully!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("ad_request.html", form=form, campaign_id=campaign_id)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))
