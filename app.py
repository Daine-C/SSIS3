from flask import Flask, render_template, url_for, request, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy


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
    
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

class ClForm(FlaskForm):
    id = StringField("Enter College Code", validators=[DataRequired()])
    name = StringField("Enter College Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CrForm(FlaskForm):
    id = StringField("Enter Course Code", validators=[DataRequired()])
    name = StringField("Enter Course Name", validators=[DataRequired()])
    collg = StringField("Enter College", validators=[DataRequired()])
    submit = SubmitField("Submit")

class StForm(FlaskForm):
    id = StringField("Enter ID Number", validators=[DataRequired(), Length(min=9, max=9)])
    fname = StringField("Enter First Name", validators=[DataRequired()])
    lname = StringField("Enter Last Name", validators=[DataRequired()])
    yr = StringField("Enter Year Level", validators=[DataRequired()])
    gender = StringField("Enter Gender", validators=[DataRequired()])
    cour = StringField("Enter Course", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
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
    cours = Courses.query.order_by(Courses.id).all()

    return render_template("Courses.html", cours=cours)

@app.route('/students/', methods=['GET', 'POST'])    
def student():
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
    
@app.route('/courses/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCR(id):
    name_to_delete = Courses.query.get_or_404(id)
    id = None
    name = None
    form = CrForm()

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("College Deleted Successfully!")
        return render_template("Deleted.html", id=id, name=name, form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", id=id, name=name, form=form,)

@app.route('/students/add/', methods=['GET', 'POST'])
def addST():
    id = None
    fname = None
    lname = None
    year = None
    gender = None
    cours = None
    form = StForm()

    if form.validate_on_submit():
        cors=Courses.query.filter_by(name=form.name.data).first()
        if cors is None:
            try:
                cours = SelectField()
                cors = Courses(id = form.id.data, fname = form.fname.data, lname=form.lname.data, 
                                year = form.yr.data, gender = form.gender.data, cours = form.cour.data)
                db.session.add(cors)
                db.session.commit()
                flash("Student Added Successfully!")
            except:
                flash("That ID Number is already in use!")
        id = form.id.data
        form.id.data = ''
        fname = form.fname.data
        form.fname.data = ''
        lname = form.lname.data
        form.lname.data = ''
        year = form.yr.data
        form.yr.data = ''
        gender = form.gender.data
        form.gender.data = ''
        cours = form.cours.data
        form.cours.data = ''
        flash("Add a another Student")        
    return render_template("AddST.html", id=id, fname=fname, lname=lname, year=year, gender=gender, cours=cours, form=form) 

@app.route('/courses/update/<string:id>', methods=['GET', 'POST'])
def updateST(id):
    form = StForm()
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
    
@app.route('/courses/deleted/<string:id>', methods=['GET', 'POST'])
def deleteST(id):
    name_to_delete = Courses.query.get_or_404(id)
    id = None
    name = None
    form = StForm()

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