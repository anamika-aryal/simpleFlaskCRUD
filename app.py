from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student.db'

db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    address=db.Column(db.String(50))
    sgpa=db.Column(db.Float)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
        student_name=request.form['sname']
        crn=request.form['crn']
        print(student_name)
        print(crn)
        return redirect('/')
    return render_template("login.html")

@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method=='POST':
        all_stud=Student.query.all()
        student_name=request.form['fname']
        address=request.form['address']
        sgpa=float(request.form['sgpa'])

        for s in all_stud:
            if s.name==student_name:
                return render_template('insert.html', error='Name already taken')
        
        new_student=Student(name=student_name, address=address,sgpa=sgpa)

        db.session.add(new_student)
        db.session.commit()
    return render_template ('insert.html')

@app.route('/view')
def view():
    all_students=Student.query.all()
    return render_template('table.html',all_students=all_students)

@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    student=Student.query.filter_by(id=id).first()
    if request.method=='POST':
        student_name=request.form['fname']
        address=request.form['address']
        sgpa=float(request.form['sgpa'])

        student.name=student_name
        student.address=address
        student.sgpa=sgpa

        db.session.add(student)
        db.session.commit()

        return render_template('table.html')
    
    return render_template('update.html',student=student)

if __name__=="__main__":
    app.run(debug=True)