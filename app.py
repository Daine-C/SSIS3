from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/SSIS'

db = SQLAlchemy(app)

class Colleges(db.Model):
    id = db.Column(db.String(10), primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<College %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        college_id = request.form['id']
        college_name = request.form['name']
        new_college = Colleges(id=college_id)
        name_college = Colleges(name=college_name)

        try:
            db.session.add(new_college)
            db.session.add(name_college)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error :('
        
    else:
        colgs = Colleges.query.order_by(Colleges.id).all()

        return render_template('College.html', colgs=colgs)    

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