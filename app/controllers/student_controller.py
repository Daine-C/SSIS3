from flask import Blueprint, render_template, flash, request, current_app
from app.models.student_models import Students
from app.forms.student_forms import StForm
from app.forms.image_forms import ImgForm

student_bp = Blueprint('student',__name__, url_prefix='/students')

@student_bp.route('/', methods=['GET', 'POST'])    
def student():

    stud = Students.all()
    if stud != None:
      studs = Students.all()
    else:
      studs=" "
      stud=" "
      flash("No Students")
    
    return render_template("Students.html", studs=studs, stud=stud) 
#Student functions
#Add
@student_bp.route('/add/', methods=['GET', 'POST'])
def addST():
    id = None
    fname = None
    lname = None
    yr = None
    gen = None
    cour = None
    form = StForm()

    if form.validate_on_submit():

        stud=Students.one(form.firstname.data,form.lastname.data)
        #Students.query.filter_by(firstname=form.firstname.data).first()
        if stud == False:
            try:
                stud = Students.add(id=form.id.data,firstname=form.firstname.data,lastname=form.lastname.data,year=form.year.data,gender=form.gender.data,courseid=form.course.data)

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
@student_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def updateST(id):
    uid=id
    form = StForm()
    name_to_update=Students.one_id(uid)

    if request.method == "POST":
        up_id = request.form['id']
        up_fname = request.form['firstname']
        up_lname = request.form['lastname']
        up_yr = request.form['year']
        up_gen = request.form['gender']
        up_cid = request.form['course']
        try:
            Students.update(id=up_id, firstname=up_fname, lastname=up_lname, year=up_yr, gender=up_gen, courseid=up_cid, uid=uid)
            uid=up_id
            name_to_update=Students.one_id(uid)

            flash("Student Updated Successfully!")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateST.html", form=form, name_to_update=name_to_update, uid=uid)
#Delete    
@student_bp.route('/deleted/<string:id>', methods=['GET', 'POST'])
def deleteST(id):
    uid=id
    form = StForm()

    try:
        Students.delete(id=uid)
        flash("Student Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 
    