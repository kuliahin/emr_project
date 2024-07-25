from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import User, Patient
from app.forms import AddPatientForm
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse

def create_routes(app):
    @app.route('/')
    @app.route('/index')
    @login_required
    def index():
        return render_template('index.html', title='Home')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/patient', methods=['GET', 'POST'])
    @login_required
    def patient():
        form = AddPatientForm()
        if form.validate_on_submit():
            patient = Patient(name=form.name.data, dob=form.dob.data, medical_history=form.medical_history.data)
            db.session.add(patient)
            db.session.commit()
            flash('Patient record added successfully')
            return redirect(url_for('patient'))
        patients = Patient.query.all()
        return render_template('patient.html', title='Patients', patients=patients, form=form)
    
    @app.route('/view_patients')
    @login_required
    def view_patients():
        patients = Patient.query.all()
        return render_template('view_patients.html', title='View Patients', patients=patients)
