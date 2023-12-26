from flask import Blueprint, render_template, flash, request
from app.models.college_models import Colleges
from app.forms.college_forms import ClForm


college_bp = Blueprint('college',__name__, url_prefix='/colleges')


@college_bp.route('/', methods=['GET', 'POST'])    
def college():

    colg = Colleges.all()
    if colg != None:
      colgs = Colleges.all()
    else:
      colgs=" "
      colg=" "
      flash("No Colleges")
    
    return render_template("College.html", colgs=colgs, colg=colg)

#College funtions
#Add
@college_bp.route('/add/', methods=['GET', 'POST'])
def addCL():
    id = None
    name = None
    form = ClForm()

    if form.validate_on_submit():
        colgs=Colleges.one(name=form.name.data)
        if colgs == False:
            try:
                Colleges.add(id=form.id.data,name=form.name.data)
                
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
@college_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def updateCL(id):
    uid=id
    form = ClForm()
    #name_to_update = Colleges.query.get_or_404(id)
    name_to_update=Colleges.one_id(uid)

    if request.method == "POST":
        up_id = request.form['id']
        up_name = request.form['name']
        try:
            Colleges.update(up_id, up_name, uid)

            uid=up_id
            name_to_update=Colleges.one_id(uid)
            check = Colleges.one_id(uid)
            if check == None:
                flash("College Deleted Successfully!")
            else:
                flash("College Cannot be Deleted! There are still students.")
            return render_template("Deleted.html", form=form) 
        except:
            flash("Error! Looks like there was a problem... TwT")
            return render_template("UpdateCL.html", form=form, name_to_update=name_to_update, uid=uid)
    else:
        return render_template("UpdateCL.html", form=form, name_to_update=name_to_update, uid=uid)
    
#Delete    
@college_bp.route('/deleted/<string:id>', methods=['GET', 'POST'])
def deleteCL(id):
    uid=id
    form = ClForm()

    try:
        Colleges.delete(uid)
        flash("College Deleted Successfully!")
        return render_template("Deleted.html", form=form) 
    except:
        flash("Error! Looks like there was a problem... TwT")
        return render_template("Deleted.html", form=form,) 