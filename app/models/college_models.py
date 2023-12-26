from flask import current_app

class Colleges(object):

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def add(cls, id, name):
        cursor = current_app.mysql.cursor()

        sql = "INSERT INTO colleges (id, name) VALUES (%s,%s)" 

        cursor.execute(sql, (id,name,))
        current_app.mysql.commit()

    @classmethod
    def all(cls):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * from colleges"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def one(cls, name):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM colleges WHERE name=(%s) LIMIT 1"
        cursor.execute(sql, (name,))
        result = cursor.fetchall()

        if result != None:
            return False
        else:
            return True
        
    @classmethod
    def one_id(cls, id):
        cursor = current_app.mysql.cursor()

        sql = "SELECT * FROM colleges WHERE id=(%s) LIMIT 1"
        cursor.execute(sql, (id,))
        result = cursor.fetchall()

        return result
    
    @classmethod
    def update(cls, id, name, uid):
        cursor = current_app.mysql.cursor()

        sql = "UPDATE colleges SET id=(%s), name=(%s) WHERE id=(%s)"
        cursor.execute(sql, (id, name, uid,))
        current_app.mysql.commit()
    
    @classmethod
    def search(cls, tag):
            cursor = current_app.mysql.cursor()
            sql = "SELECT * FROM colleges WHERE id LIKE (%s) OR name LIKE (%s)"
            cursor.execute(sql, (tag,tag,))
            result = cursor.fetchall()
            return result

    @classmethod
    def delete(cls, id):
        try:
            cursor = current_app.mysql.cursor()
            sql = "DELETE FROM colleges WHERE id=(%s)"
            cursor.execute(sql, (id,))
            current_app.mysql.commit()
            return True
        except:
            return False
        
        

        
