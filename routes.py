from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Sample
from .. import db
from ..forms import SampleForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("main/index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    sample_count = Sample.query.count()
    recent_samples = Sample.query.order_by(Sample.created_at.desc()).limit(5).all()
    return render_template(
        "main/dashboard.html",
        sample_count=sample_count,
        recent_samples=recent_samples,
    )


@main_bp.route("/samples")
@login_required
def samples():
    all_samples = Sample.query.order_by(Sample.created_at.desc()).all()
    return render_template("main/samples.html", samples=all_samples)


@main_bp.route("/samples/new", methods=["GET", "POST"])
@login_required
def new_sample():
    form = SampleForm()
    if form.validate_on_submit():
        sample = Sample(
            sample_code=form.sample_code.data,
            collection_date=form.collection_date.data,
            received_by=current_user,
            status=form.status.data,
            organism=form.organism.data,
            result=form.result.data,
        )
        db.session.add(sample)
        db.session.commit()
        flash("Sample created successfully.", "success")
        return redirect(url_for("main.samples"))
    return render_template("main/sample_form.html", form=form, title="New Sample")


@main_bp.route("/samples/<int:sample_id>")
@login_required
def sample_detail(sample_id):
    sample = Sample.query.get_or_404(sample_id)
    return render_template("main/sample_detail.html", sample=sample)