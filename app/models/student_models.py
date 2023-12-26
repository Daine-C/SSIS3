from flask import current_app

class Students(object):

    def __init__(self, id=None, firstname=None, lastname=None, year=None, gender=None, courseid=None, profilepic=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.year = year
        self.gender = gender
        self.courseid = courseid
        self.profilepic = profilepic

    @classmethod
    def add(cls, id, firstname, lastname, year, gender, courseid):
        cursor = current_app.mysql.cursor()

        sql = "INSERT INTO students (id, firstname, lastname, year, gender, courseid) VALUES (%s,%s,%s,%s,%s,%s)" 

        cursor.execute(sql, (id, firstname, lastname, year, gender, courseid,))
        current_app.mysql.commit()

    @classmethod
    def all(cls):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM students CROSS JOIN courses ON students.courseid=courses.id ORDER BY students.id"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def one(cls, firstname, lastname):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM students WHERE firstname=(%s) AND lastname=(%s) LIMIT 1"
        cursor.execute(sql, (firstname,lastname,))
        result = cursor.fetchall()
        if result != None:
            return False
        else:
            return True
        
    @classmethod
    def one_id(cls, id):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM students WHERE id=(%s) LIMIT 1"
        cursor.execute(sql, (id,))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def update(cls, id, firstname, lastname, year, gender, courseid, uid):
        cursor = current_app.mysql.cursor()

        sql = "UPDATE students SET id=(%s), firstname=(%s), lastname=(%s), year=(%s), gender=(%s), courseid=(%s) WHERE id=(%s)"
        cursor.execute(sql, (id, firstname, lastname, year, gender, courseid, uid,))
        current_app.mysql.commit()

    @classmethod
    def profile_pic(cls, secure_url, id):
        cursor = current_app.mysql.cursor()

        sql = "UPDATE students SET profilepic=(%s) WHERE id=(%s)"
        cursor.execute(sql, (secure_url, id,))
        current_app.mysql.commit()
    
    @classmethod
    def search(cls, tag):
        cursor = current_app.mysql.cursor()
        sql = """SELECT * FROM students CROSS JOIN courses 
                ON students.courseid=courses.id WHERE students.id LIKE (%s) 
                OR firstname LIKE (%s) OR lastname LIKE (%s) OR year LIKE (%s) 
                OR courseid LIKE (%s) OR collegeid LIKE (%s)"""
        cursor.execute(sql, (tag,tag,tag,tag,tag,tag,))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def search_year(cls, tag):
        cursor = current_app.mysql.cursor()
        sql = "SELECT * FROM students WHERE year LIKE (%s)"
        cursor.execute(sql, (tag,))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def search_gender(cls, tag):
        cursor = current_app.mysql.cursor()
        sql = "SELECT * FROM students WHERE gender LIKE (%s)"
        cursor.execute(sql, (tag,))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def search_all(cls, tag):
        cursor = current_app.mysql.cursor()
        sql = """SELECT * FROM students CROSS JOIN courses 
                    ON students.courseid=courses.id CROSS JOIN colleges ON courses.collegeid=colleges.id
                    WHERE students.id LIKE (%s) OR courseid LIKE (%s) OR collegeid LIKE (%s) OR courses.name LIKE (%s) 
                    OR colleges.name LIKE (%s) OR firstname LIKE (%s) OR lastname LIKE (%s) OR year LIKE (%s) OR gender LIKE (%s)"""
        cursor.execute(sql, (tag,tag,tag,tag,tag,tag,tag,tag,tag,))
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls, id):
        try:
            cursor = current_app.mysql.cursor()
            sql = "DELETE FROM students WHERE id=(%s)"
            cursor.execute(sql, (id,))
            current_app.mysql.commit()
            return True
        except:
            return False

        
