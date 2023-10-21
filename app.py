from flask import Flask, render_template, url_for, request, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, text


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/SSIS'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Colleges(db.Model):
    __tablename__ = "Colleges"
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    conn_course = db.relationship('Courses', cascade = "all,delete", backref = "courses")

    def __repr__(self):
        return '<College %r>' % self.id
    
class Courses(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    #College reference
    collegeid = db.Column(db.String(10), db.ForeignKey('Colleges.id'))
    conn_student = db.relationship('Students', cascade = "all,delete", backref = "students")

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
    courseid = db.Column(db.String(10), db.ForeignKey('Courses.id'))

    def __repr__(self):
        return '<Student %r>' % self.id

#Forms    
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

#College Form
class ClForm(FlaskForm):
    id = StringField("Enter College Code", validators=[DataRequired()])
    name = StringField("Enter College Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
#Course Form
class CrForm(FlaskForm):
    id = StringField("Enter Course Code", validators=[DataRequired()])
    name = StringField("Enter Course Name", validators=[DataRequired()])
    collg = StringField("Enter College", validators=[DataRequired()])
    submit = SubmitField("Submit")
#Student Form
class StForm(FlaskForm):
    id = StringField("Enter ID Number (YYYY-NNNN)", validators=[DataRequired()])
    firstname = StringField("Enter First Name", validators=[DataRequired()])
    lastname = StringField("Enter Last Name", validators=[DataRequired()])
    year = StringField("Enter Year Level (only the Integer)", validators=[DataRequired()])
    gender = StringField("Enter Gender", validators=[DataRequired()])
    course = StringField("Enter Course", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("Home.html")
#College Table
@app.route('/colleges/', methods=['GET', 'POST'])    
def college():
    colgs = Colleges.query.order_by(Colleges.id).all()
    return render_template("College.html", colgs=colgs)
#Course Table
@app.route('/courses/', methods=['GET', 'POST'])    
def course():
    cours = Courses.query.order_by(Courses.id).all()
    return render_template("Courses.html", cours=cours)
#Student Table
@app.route('/students/', methods=['GET', 'POST'])    
def student():
    studs = Students.query.order_by(Students.lastname).all()
    return render_template("Students.html", studs=studs)       
#College funtions
#Add
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
#Edit
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
#Delete    
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

#Course functions
#Add
@app.route('/courses/add/', methods=['GET', 'POST'])
def addCR():
    id = None
    name = None
    collg = None
    form = CrForm()

    if form.validate_on_submit():
        cors=Courses.query.filter_by(name=form.name.data).first()
        if cors is None:
            try:
                collg = SelectField()
                cors = Courses(id = form.id.data, name = form.name.data, collegeid = form.collg.data)
                db.session.add(cors)
                db.session.commit()
                flash("Course Added Successfully!")
            except:
                flash("That Course Code is already in use!")
        id = form.id.data
        form.id.data = ''
        name = form.name.data
        form.name.data = ''
        collg = form.collg.data
        form.collg.data = ''
        flash("Add a another Course")        
    return render_template("AddCR.html", id=id, name=name, collg=collg, form=form) 
#Edit
@app.route('/courses/update/<string:id>', methods=['GET', 'POST'])
def updateCR(id):
    form = CrForm()
    name_to_update = Courses.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.id = request.form['id']
        name_to_update.name = request.form['name']
        name_to_update.collegeid = request.form['collg']
        try:
            db.session.commit()
            flash("Course Updated Successfully!")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("UpdateCR.html", form=form, name_to_update=name_to_update)
#Delete    
@app.route('/courses/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCR(id):
    name_to_delete = Courses.query.get_or_404(id)
    id = None
    name = None
    form = CrForm()

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("Course Deleted Successfully!")
        return render_template("Deleted.html", id=id, name=name, form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", id=id, name=name, form=form,)

#Student functions
#Add
@app.route('/students/add/', methods=['GET', 'POST'])
def addST():
    id = None
    fname = None
    lname = None
    yr = None
    gen = None
    cour = None
    form = StForm()

    if form.validate_on_submit():
        stud=Students.query.filter_by(firstname=form.firstname.data).first()
        if stud is None:
            try:
                stud = Students(id = form.id.data, firstname = form.firstname.data, lastname = form.lastname.data, year = form.year.data, gender = form.gender.data, courseid = form.course.data)
                db.session.add(stud)
                db.session.commit()
                flash("Student Added Successfully!")
            except:
                flash("Error! Either the ID Number is already in use or values are in incorrect form...")
        id = form.id.data
        form.id.data = ''
        fname = form.firstname.data
        form.firstname.data = ''
        lname = form.lastname.data
        form.lastname.data = ''
        yr = form.year.data
        form.year.data = ''
        gen = form.gender.data
        form.gender.data = ''
        cour = form.course.data
        form.course.data = ''
        flash("Add a another Student")        
    return render_template("AddST.html", id=id, fname=fname, lname=lname, yr=yr, gen=gen, cour=cour, form=form) 
#Edit
@app.route('/students/update/<string:id>', methods=['GET', 'POST'])
def updateST(id):
    form = StForm()
    name_to_update = Students.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.id = request.form['id']
        name_to_update.firstname = request.form['firstname']
        name_to_update.lastname = request.form['lastname']
        name_to_update.year = request.form['year']
        name_to_update.gender = request.form['gender']
        name_to_update.courseid = request.form['course']
        try:
            db.session.commit()
            flash("Student Updated Successfully!")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("UpdateST.html", form=form, name_to_update=name_to_update)
#Delete    
@app.route('/students/deleted/<string:id>', methods=['GET', 'POST'])
def deleteST(id):
    name_to_delete = Students.query.get_or_404(id)
    id = None
    fname = None
    lname = None
    yr = None
    gen = None
    cour = None
    form = StForm()

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("Student Deleted Successfully!")
        return render_template("Deleted.html", id=id, fname=fname, lname=lname, yr=yr, gen=gen, cour=cour, form=form)
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", id=id, fname=fname, lname=lname, yr=yr, gen=gen, cour=cour, form=form)
    
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

#Search    
@app.route('/search', methods=["POST"])
def search():
  form = SearchForm()
  search = '%' + str(form.searched) + '%'
  if form.validate_on_submit:
    results = Colleges.query.join(Courses).join(Students)
    results = results.filter(text('%' + search + '%'))
  return render_template("Search.html", form=form, search=search, results=results)



 
        

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