from flask import Flask, render_template, url_for, request, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "ssis"
app.config['MYSQL_PASSWORD'] = "1234"
app.config['MYSQL_DB'] = "ssis"
app.config['SECRET_KEY'] = 'secret'

mysql = MySQL(app)

#class Colleges(db.Model):
#    __tablename__ = "Colleges"
#    id = db.Column(db.String(10), primary_key = True, nullable = False)
#    name = db.Column(db.String(200), nullable = False)
#    conn_course = db.relationship('Courses', cascade = "all,delete", backref = "courses")

#    def __repr__(self):
#        return '<College %r>' % self.id
    
#class Courses(db.Model):
#    __tablename__ = "Courses"
#    id = db.Column(db.String(10), primary_key = True, nullable = False)
#    name = db.Column(db.String(200), nullable = False)
#    #College reference
#    collegeid = db.Column(db.String(10), db.ForeignKey('Colleges.id'))
#    conn_student = db.relationship('Students', cascade = "all,delete", backref = "students")

#    def __repr__(self):
#        return '<Course %r>' % self.id
    
#class Students(db.Model):
#    __tablename__ = "Students"
#    id = db.Column(db.String(10), primary_key = True, nullable = False)
#    firstname = db.Column(db.String(200), nullable = False)
#    lastname = db.Column(db.String(200), nullable = False)
#    year = db.Column(db.Integer, nullable = False)
#    gender = db.Column(db.String(200), nullable = False)
    #Course reference
#    courseid = db.Column(db.String(10), db.ForeignKey('Courses.id'))

#    def __repr__(self):
#        return '<Student %r>' % self.id

#Search Form All    
class SearchAllForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    typs = SelectField(u'Fields', choices=[('cl', 'Colleges'),('cr', 'Courses'),('st', 'Students')])
    submit = SubmitField("Submit")

#Search Forms    
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

@app.route('/')
def index():
    return render_template("Home.html")
#College Table
@app.route('/colleges/', methods=['GET', 'POST'])    
def college():
    curr = mysql.connection.cursor()

    colg = curr.execute("SELECT * FROM colleges")
    if colg > 0:
      colgs = curr.fetchall()
    else:
      colgs=" "
      colg=" "
      flash("No Colleges")

    curr.close()
    
    return render_template("College.html", colgs=colgs, colg=colg)
#Course Table
@app.route('/courses/', methods=['GET', 'POST'])    
def course():
    curr = mysql.connection.cursor()

    cour = curr.execute("SELECT * FROM courses")
    if cour > 0:
      cours = curr.fetchall()
    else:
      cours=" "
      cour=" "
      flash("No Courses")

    curr.close()
    
    return render_template("Courses.html", cours=cours, cour=cour)
#Student Table
@app.route('/students/', methods=['GET', 'POST'])    
def student():
    curr = mysql.connection.cursor()

    stud = curr.execute("SELECT * FROM students")
    if stud > 0:
      studs = curr.fetchall()
    else:
      studs=" "
      stud=" "
      flash("No Students")

    curr.close()
    
    return render_template("Students.html", studs=studs, stud=stud)       
#College funtions
#Add
@app.route('/colleges/add/', methods=['GET', 'POST'])
def addCL():
    id = None
    name = None
    form = ClForm()

    curr = mysql.connection.cursor()

    if form.validate_on_submit():
        colgs=curr.execute("SELECT * FROM colleges WHERE name=(%s) LIMIT 1", [form.name.data])
        #Colleges.query.filter_by(name=form.name.data).first()
        if colgs == False:
            try:
                curr.execute("INSERT INTO colleges (id, name) VALUES (%s,%s)", [form.id.data,form.name.data])
                #Colleges(id = form.id.data, name = form.name.data)
                #db.session.add(coll)
                #db.session.commit()

                mysql.connection.commit()
                curr.close()
                
                flash("College Added Successfully!")
            except:
                flash("That College Code is already in use!")
        else:
            flash("That College Name is already in use!")
        id = form.id.data
        form.id.data = ''
        name = form.name.data
        form.name.data = ''
        flash("Add another College?")        
    return render_template("AddCL.html", id=id, name=name, form=form) 
#Edit
@app.route('/colleges/update/<string:id>', methods=['GET', 'POST'])
def updateCL(id):
    uid=id
    form = ClForm()
    #name_to_update = Colleges.query.get_or_404(id)
    curr = mysql.connection.cursor()
    name_to_update=curr.execute("SELECT * FROM colleges WHERE id=(%s)", [uid])

    if request.method == "POST":
        up_id = request.form['id']
        up_name = request.form['name']
        try:
            curr.execute("UPDATE colleges SET id=(%s), name=(%s) WHERE id=(%s)", [up_id, up_name, uid])
            mysql.connection.commit()
            uid=up_id
            name_to_update=curr.execute("SELECT * FROM colleges WHERE id=(%s)", [uid])
            curr.close()
            flash("College Updated Successfully!")
            return render_template("UpdateCL.html", form=form, name_to_update=name_to_update, uid=uid)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCL.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateCL.html", form=form, name_to_update=name_to_update, uid=uid)
#Delete    
@app.route('/colleges/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCL(id):
    uid=id
    curr = mysql.connection.cursor()
    form = ClForm()

    try:
        curr.execute("DELETE FROM colleges WHERE id=(%s)", [uid])
        mysql.connection.commit()
        curr.close()
        flash("College Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 

#Course functions
#Add
@app.route('/courses/add/', methods=['GET', 'POST'])
def addCR():
    id = None
    name = None
    collg = None
    form = CrForm()

    curr = mysql.connection.cursor()

    if form.validate_on_submit():
        cors=curr.execute("SELECT * FROM courses WHERE name=(%s) LIMIT 1", [form.name.data])
        if cors == False:
            try:
                cors = curr.execute("INSERT INTO courses (id, name,collegeid) VALUES (%s,%s,%s)", [form.id.data,form.name.data,form.collg.data])
                #Courses(id = form.id.data, name = form.name.data, collegeid = form.collg.data)
                #db.session.add(cors)
                #db.session.commit()

                mysql.connection.commit()
                curr.close()

                flash("Course Added Successfully!")
            except:
                flash("That Course Code is already in use!")
        else:
            flash("That Course Name is already in use!")
        id = form.id.data
        form.id.data = ''
        name = form.name.data
        form.name.data = ''
        collg = form.collg.data
        form.collg.data = ''
        flash("Add another Course?")        
    return render_template("AddCR.html", id=id, name=name, collg=collg, form=form) 
#Edit
@app.route('/courses/update/<string:id>', methods=['GET', 'POST'])
def updateCR(id):
    uid=id
    form = CrForm()
    curr = mysql.connection.cursor()
    name_to_update=curr.execute("SELECT * FROM courses WHERE id=(%s)", [uid])

    if request.method == "POST":
        up_id = request.form['id']
        up_name = request.form['name']
        up_cid = request.form['collg']
        try:
            curr.execute("UPDATE courses SET id=(%s), name=(%s), collegeid=(%s) WHERE id=(%s)", [up_id, up_name, up_cid, uid])
            mysql.connection.commit()
            uid=up_id
            name_to_update=curr.execute("SELECT * FROM courses WHERE id=(%s)", [uid])
            curr.close()
            flash("Course Updated Successfully!")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
#Delete    
@app.route('/courses/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCR(id):
    uid=id
    curr = mysql.connection.cursor()
    form = CrForm()

    try:
        curr.execute("DELETE FROM courses WHERE id=(%s)", [uid])
        mysql.connection.commit()
        curr.close()
        flash("Course Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 

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

    curr = mysql.connection.cursor()

    if form.validate_on_submit():
        stud=curr.execute("SELECT * FROM students WHERE firstname=(%s) AND lastname=(%s) LIMIT 1", [form.firstname.data,form.lastname.data])
        #Students.query.filter_by(firstname=form.firstname.data).first()
        if stud == False:
            try:
                stud = curr.execute("INSERT INTO students (id, firstname, lastname, year, gender, courseid) VALUES (%s,%s,%s,%s,%s,%s)", [form.id.data,form.firstname.data,form.lastname.data,form.year.data,form.gender.data,form.course.data])
                #Students(id = form.id.data, firstname = form.firstname.data, lastname = form.lastname.data, year = form.year.data, gender = form.gender.data, courseid = form.course.data)
                #db.session.add(stud)
                #db.session.commit()

                mysql.connection.commit()
                curr.close()

                flash("Student Added Successfully!")
            except:
                flash("Error! Either the ID Number is already in use or values are in incorrect form...")
        else:
            flash("Student Name already in use!")
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
        flash("Add another Student")        
    return render_template("AddST.html", id=id, fname=fname, lname=lname, yr=yr, gen=gen, cour=cour, form=form) 
#Edit
@app.route('/students/update/<string:id>', methods=['GET', 'POST'])
def updateST(id):
    uid=id
    form = StForm()
    curr = mysql.connection.cursor()
    name_to_update=curr.execute("SELECT * FROM students WHERE id=(%s)", [uid])

    if request.method == "POST":
        up_id = request.form['id']
        up_fname = request.form['firstname']
        up_lname = request.form['lastname']
        up_yr = request.form['year']
        up_gen = request.form['gender']
        up_cid = request.form['course']
        try:
            curr.execute("UPDATE students SET id=(%s), firstname=(%s), lastname=(%s), year=(%s), gender=(%s), courseid=(%s) WHERE id=(%s)", [up_id, up_fname, up_lname, up_yr, up_gen, up_cid, uid])
            mysql.connection.commit()
            uid=up_id
            name_to_update=curr.execute("SELECT * FROM students WHERE id=(%s)", [uid])
            curr.close()
            flash("Student Updated Successfully!")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
#Delete    
@app.route('/students/deleted/<string:id>', methods=['GET', 'POST'])
def deleteST(id):
    uid=id
    curr = mysql.connection.cursor()
    form = StForm()

    try:
        curr.execute("DELETE FROM students WHERE id=(%s)", [uid])
        mysql.connection.commit()
        curr.close()
        flash("Student Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 
    
@app.context_processor
def base():
	form = SearchAllForm()
	return dict(form=form)

#Search    
@app.route('/search', methods=["POST"])
def search():
  form = SearchAllForm()
  tag = request.form['searched']
  typ = request.form['typs']
  results = None
  curr = mysql.connection.cursor()

  tag = tag+'%'

  if form.validate_on_submit:
      if typ == 'cl':
        colg = curr.execute("SELECT * FROM colleges WHERE id LIKE (%s) OR name LIKE (%s)", [tag,tag])
        if colg > 0:
         results = curr.fetchall()
        else:
         flash("Sorry, no results...")
        return render_template("Search.html",
		 form=form,
		 results = results) 
      elif typ == 'cr':
        cour = curr.execute("SELECT * FROM courses WHERE id LIKE (%s) OR name LIKE (%s)", [tag,tag])
        if cour > 0:
         results = curr.fetchall()
        else:
         flash("Sorry, no results...")
        return render_template("Search.html",
		 form=form,
		 results = results) 
      elif typ == 'st':
        stud = curr.execute("SELECT * FROM students WHERE id LIKE (%s) OR firstname LIKE (%s) OR lastname LIKE (%s)", [tag,tag,tag])
        if stud > 0:
         results = curr.fetchall()
        else:
         flash("Sorry, no results...")
        return render_template("Search.html",
		 form=form,
		 results = results) 
      else:
          return render_template('Search.html')
      

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