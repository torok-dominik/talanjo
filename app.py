from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    lecture_choices = db.Column(db.String(200), nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        first_name = request.form['first_name']
        email = request.form['email']
        class_name = request.form['class_name']
        lecture_choices = request.form.getlist('lecture')

        if not surname or not first_name or not email or not class_name:
            flash('Please fill in all fields!', 'error')
            return redirect(url_for('register'))

        if Student.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        new_student = Student(surname=surname, first_name=first_name, email=email, class_name=class_name, lecture_choices=",".join(lecture_choices))
        db.session.add(new_student)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/admin')
def admin():
    students = Student.query.all()
    return render_template('admin.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
