from flask import Blueprint, render_template, flash, request
from app.models.course_models import Courses
from app.forms.course_forms import CrForm

course_bp = Blueprint('course',__name__, url_prefix='/courses')

#Course Table
@course_bp.route('/', methods=['GET', 'POST'])    
def course():

    cour = Courses.all()
    if cour != None:
      cours = Courses.all()
    else:
      cours=" "
      cour=" "
      flash("No Courses")
    
    return render_template("Courses.html", cours=cours, cour=cour)
#Course functions
#Add
@course_bp.route('/add/', methods=['GET', 'POST'])
def addCR():
    id = None
    name = None
    collg = None
    form = CrForm()

    if form.validate_on_submit():
        cors=Courses.one(form.name.data)
        if cors == False:
            try:
                cors = Courses.add(id=form.id.data,name=form.name.data,collegeid=form.collg.data)

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
@course_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def updateCR(id):
    uid=id
    form = CrForm()

    name_to_update=Courses.one_id(uid)

    if request.method == "POST":
        up_id = request.form['id']
        up_name = request.form['name']
        up_cid = request.form['collg']
        try:
            Courses.update(id=up_id, name=up_name, cid=up_cid, uid=uid)

            uid=up_id
            name_to_update=Courses.one_id(uid)

            flash("Course Updated Successfully!")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateCR.html", form=form, name_to_update=name_to_update, uid=uid)
#Delete    
@course_bp.route('/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCR(id):
    uid=id
    form = CrForm()

    try:
        Courses.delete(id=uid)
        flash("Course Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 