from flask import Flask, render_template, request, flash
from mysql.connector import connect
from app.forms.search_forms import SearchForm
from app.forms.image_forms import ImgForm
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload as cloudinary_upload

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, SECRET_KEY, CLOUD_NAME, API_KEY, API_SECRET, CLOUDINARY_FOLDER
from flask_wtf.csrf import CSRFProtect

def create_app():

    app = Flask(__name__)
    
    with app.app_context():
        app.config['MYSQL_HOST']=MYSQL_HOST
        app.config['MYSQL_USER']=MYSQL_USER
        app.config['MYSQL_PASSWORD']=MYSQL_PASSWORD
        app.config['MYSQL_DATABASE']=MYSQL_DB
        app.config['SECRET_KEY']=SECRET_KEY
        
        cloudinary.config(cloud_name=CLOUD_NAME,
                    api_key=API_KEY,
                    api_secret=API_SECRET,
                    )

        CSRFProtect(app)

        app.mysql = connect(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        database=MYSQL_DB
    )    

        from app.models.college_models import Colleges
        from app.models.course_models import Courses
        from app.models.student_models import Students

        @app.route('/')
        def index():
            return render_template("Home.html")
        
        @app.route('/students/upload/<string:id>', methods=['GET', 'POST'])
        def uploadIMG(id):
            uid=id
            pfp = None
            form = ImgForm()
            image_to_update=Students.one_id(uid)

            if request.method == "POST":
                image = request.files['pfp']

                upload_result = cloudinary_upload(
                        image, folder=CLOUDINARY_FOLDER)
                secure_url = upload_result['secure_url']

                try:
                    Students.profile_pic(secure_url=secure_url, id=uid)
                    flash("Student Updated Successfully!")
                    return render_template("AddImg.html", form=form, image_to_update=image_to_update, uid=uid)
                except:
                    flash("Error! Looks like there was a problem... TwT")
                    return render_template("AddImg.html", form=form, image_to_update=image_to_update, uid=uid)
            else:
                return render_template("AddImg.html", form=form, image_to_update=image_to_update, uid=uid)

        @app.context_processor
        def base():
            form = SearchForm()
            return dict(form=form)
            
        @app.route('/search', methods=["POST"])
        def search():
            typ = None
            form = SearchForm()
            tag = request.form['searched']
            typ = request.form['typs']
            results = None

            if typ == 'gen':
                tag = tag+'%'
            else:
                tag = '%'+tag+'%'

            if form.validate_on_submit:
                if typ == 'cl':
                    results = Colleges.search(tag)
                    if results == None:
                        flash("Sorry, no results...")
                    return render_template("Search.html",form=form,results = results) 
                elif typ == 'cr':
                    results = Courses.search(tag)
                    if results == None:
                        flash("Sorry, no results...")
                    return render_template("Search.html",form=form,results = results) 
                elif typ == 'st':
                    results = Students.search(tag)
                    if results == None:
                        flash("Sorry, no results...")
                            
                    return render_template("Search.html",
                        form=form,
                        results = results) 
                elif typ == 'yr':
                    results = Students.search_year(tag)
                    if results == None:
                        flash("Sorry, no results...")
                    return render_template("Search.html",form=form,results = results)          
                elif typ == 'gen':
                    results = Students.search_gender(tag)
                    if results == None:
                        flash("Sorry, no results...")
                    return render_template("Search.html",
                        form=form,
                        results = results) 
                else:
                    results = Students.search_all(tag)
                    if results == None:
                        flash("Sorry, no results...")
                    return render_template("Search.html",
                        form=form,
                        results = results) 

        from app.controllers.college_controller import college_bp as college_blueprint
        from app.controllers.course_controller import course_bp as course_blueprint
        from app.controllers.student_controller import student_bp as student_blueprint
            
        app.register_blueprint(college_blueprint)
        app.register_blueprint(course_blueprint)
        app.register_blueprint(student_blueprint)



    return app
