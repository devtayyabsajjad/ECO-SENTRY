import os
from flask import render_template
from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Report, EnvironmentalData
from app.forms import LoginForm, RegistrationForm, ReportForm
from app.ai_utils import analyze_report, generate_recommendations, analyze_image, predict_environmental_trends

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    reports = Report.query.filter_by(user_id=current_user.id).all()
    env_data = EnvironmentalData.query.order_by(EnvironmentalData.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', reports=reports, env_data=env_data)

@bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        report = Report(
            user_id=current_user.id,
            description=form.description.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            image_filename=filename
        )
        db.session.add(report)
        db.session.commit()

        # Analyze report and generate recommendations using AI
        insights = analyze_report(form.description.data)
        recommendations = generate_recommendations(form.description.data)
        
        if filename:
            image_analysis = analyze_image(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            image_analysis = None

        report.ai_analysis = insights
        report.recommendations = recommendations
        db.session.commit()

        # Update user points
        current_user.points += 10
        db.session.commit()

        flash('Report submitted successfully. You earned 10 points!')
        return render_template('report_result.html', insights=insights, recommendations=recommendations, image_analysis=image_analysis)
    return render_template('report.html', form=form)

@bp.route('/trends')
@login_required
def trends():
    historical_data = EnvironmentalData.query.order_by(EnvironmentalData.timestamp).all()
    predictions = predict_environmental_trends(str(historical_data))
    return render_template('trends.html', predictions=predictions)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500