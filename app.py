from flask import Flask, render_template, url_for, request, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ssisforms import ClForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/SSIS'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Colleges(db.Model):
    __tablename__ = "Colleges"
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<College %r>' % self.id
    
class Courses(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    #College reference
    collegeid = db.Column(db.String(10), db.ForeignKey(Colleges.id))
    c_college = db.relationship(Colleges, cascade = "all,delete", backref = "courses")

    def __repr__(self):
        return '<Course %r>' % self.id
    
class Students(db.Model):
    __tablename__ = "Students"
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    firstname = db.Column(db.String(200), nullable = False)
    lastname = db.Column(db.String(200), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(200), nullable = False)
    #Course reference
    courseid = db.Column(db.String(10), db.ForeignKey(Courses.id))
    c_college = db.relationship(Courses, cascade = "all,delete", backref = "students")

    def __repr__(self):
        return '<Student %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("Home.html")

@app.route('/colleges/', methods=['GET', 'POST'])    
def college():
    colgs = Colleges.query.order_by(Colleges.id).all()

    return render_template("College.html", colgs=colgs)

@app.route('/courses/', methods=['GET', 'POST'])    
def course():
    if request.method == 'POST':
        course_id = request.form['id']
        course_name = request.form['name']
        course_college = request.form['college_id']
        new_course = Courses(id=course_id)
        name_course = Courses(name=course_name)
        conn_college = Courses(collegeid=course_college)

        try:
            db.session.add(new_course)
            db.session.add(name_course)
            db.session.add(conn_college)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error :('
        
    else:
        cours = Courses.query.order_by(Courses.id).all()

        return render_template("Courses.html", cours=cours)

@app.route('/students/', methods=['GET', 'POST'])    
def student():
    if request.method == 'POST':
        student_id = request.form['id']
        student_fname = request.form['firstname']
        student_lname = request.form['lastname']
        student_year = request.form['year']
        student_gender = request.form['gender']
        student_course = request.form['course']
        new_student = Students(id=student_id)
        fname_student = Students(firstname=student_fname)
        lname_student = Students(secondname=student_lname)
        year_student = Students(year=student_year)
        gender_student = Students(id=student_gender)
        conn_student = Students(name=student_course)

        try:
            db.session.add(new_student)
            db.session.add(fname_student)
            db.session.add(lname_student)
            db.session.add(year_student)
            db.session.add(gender_student)
            db.session.add(conn_student)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error :('
        
    else:
        stud = Students.query.order_by(Students.id).all()

        return render_template("Students.html", stud=stud)       

@app.route('/colleges/add/', methods=['GET', 'POST'])
def addCL():
    id = None
    name = None
    form = ClForm()

    if form.validate_on_submit():
        colgs=Colleges.query.filter_by(name=form.name.data).first()
        if colgs is None:
            try:
                coll = Colleges(id = form.id.data, name = form.name.data)
                db.session.add(coll)
                db.session.commit()
                flash("College Added Successfully!")
            except:
                flash("That College Code is already in use!")
        id = form.id.data
        form.id.data = ''
        name = form.name.data
        form.name.data = ''
        flash("Add a another College")        
    return render_template("AddCL.html", id=id, name=name, form=form) 

@app.route('/colleges/update/<string:id>', methods=['GET', 'POST'])
def updateCL(id):
    form = ClForm()
    name_to_update = Colleges.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.id = request.form['id']
        name_to_update.name = request.form['name']
        try:
            db.session.commit()
            flash("College Updated Successfully!")
            return render_template("UpdateCL.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCL.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("UpdateCL.html", form=form, name_to_update=name_to_update)
    
@app.route('/colleges/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCL(id):
    name_to_delete = Colleges.query.get_or_404(id)
    id = None
    name = None
    form = ClForm()

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("College Deleted Successfully!")
        return render_template("Deleted.html", id=id, name=name, form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", id=id, name=name, form=form,) 

if __name__ == "__main__":
    app.run(debug=True)

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404".html), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500".html), 500