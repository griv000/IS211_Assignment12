import sqlite3 as lite

def run_sql():
    
    try:
        con = lite.connect('hw13.db')
        cur = con.cursor()
        
        MyFile = open('schema.sql','r')
        MyQuery = MyFile.read()

        cur.executescript(MyQuery)
        con.commit()
        print("Loaded Successfully")

    except lite.Error:
        if con:
            con.rollback()
        print("Error")
        quit()


    finally:
        if con:
            con.close()

if __name__ == "__main__":
    run_sql()