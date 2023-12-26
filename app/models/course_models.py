from flask import current_app

class Courses(object):

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def add(cls, id, name, collegeid):
        cursor = current_app.mysql.cursor()

        sql = "INSERT INTO courses (id, name, collegeid) VALUES (%s,%s,%s)" 

        cursor.execute(sql, (id,name,collegeid,))
        current_app.mysql.commit()

    @classmethod
    def all(cls):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * from courses"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def one(cls, id):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM courses WHERE name=(%s) LIMIT 1"
        cursor.execute(sql, (id,))
        result = cursor.fetchall()
        if result != None:
            return False
        else:
            return True
        
    @classmethod
    def one_id(cls, id):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM courses WHERE id=(%s) LIMIT 1"
        cursor.execute(sql, (id,))
        result = cursor.fetchall()

        return result
    
    @classmethod
    def update(cls, id, name, cid, uid):
        cursor = current_app.mysql.cursor()

        sql = "UPDATE courses SET id=(%s), name=(%s), collegeid=(%s) WHERE id=(%s)"
        cursor.execute(sql, (id, name, cid, uid,))
        current_app.mysql.commit()
    
    @classmethod
    def search(cls, tag):
            cursor = current_app.mysql.cursor()
            sql = "SELECT * FROM courses WHERE id LIKE (%s) OR name LIKE (%s)"
            cursor.execute(sql, (tag,tag,))
            result = cursor.fetchall()
            return result

    @classmethod
    def delete(cls, id):
        try:
            cursor = current_app.mysql.cursor()
            sql = "DELETE FROM courses WHERE id=(%s)"
            cursor.execute(sql, (id,))
            current_app.mysql.commit()
            return True
        except:
            return False

        
