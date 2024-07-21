from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin', 'sponsor', 'influencer'


class SponsorProfile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    company_name = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    budget = db.Column(db.Float)
    user = db.relationship("User", backref=db.backref("sponsor_profile", uselist=False))


class InfluencerProfile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    name = db.Column(db.String(128))
    category = db.Column(db.String(128))
    niche = db.Column(db.String(128))
    reach = db.Column(db.Integer)
    user = db.relationship(
        "User", backref=db.backref("influencer_profile", uselist=False)
    )


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)  # 'public', 'private'
    goals = db.Column(db.Text, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sponsor = db.relationship("User", backref=db.backref("campaigns", lazy=True))


class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(10), nullable=False
    )  # 'Pending', 'Accepted', 'Rejected'
    campaign = db.relationship("Campaign", backref=db.backref("ad_requests", lazy=True))
    influencer = db.relationship("User", backref=db.backref("ad_requests", lazy=True))
