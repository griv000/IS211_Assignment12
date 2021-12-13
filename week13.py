import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, session, g, redirect, url_for, abort, render_template


app = Flask(__name__) 
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hw13.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        if request.form['username'] != "admin":
            error = 'Invalid username'
            session['logged_in'] = False
        elif request.form['password'] != "password":
            error = 'Invalid password'
            session['logged_in'] = False
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html',error=error)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if session['logged_in'] != True:
            error="You are not logged in"
            return redirect('/login',error=error)
    else:
        db = get_db()
        cur = db.execute('Select * from tblStudent ORDER BY StudentLastName ASC, StudentFirstName ASC')
        students  = cur.fetchall()
        cur = db.execute('Select * from tblQuiz ORDER BY QuizDate')
        quizzes = cur.fetchall()
        return render_template('dashboard.html',students=students,quizzes=quizzes)


@app.route('/student/add',methods=['GET','POST'])
def add_student():
    if session['logged_in'] != True:
        error="You are not logged in"
        return redirect('/login',error=error)
    elif request.method == 'GET':
        return render_template('addstudent.html')
    elif request.method == 'POST':
        MyError=""
        try:
            db = get_db()
            FN = request.form["FirstName"]
            LN = request.form["LastName"]
            db.execute('insert into tblStudent (StudentFirstName,StudentLastName) values (?,?)',(FN,LN))
            db.commit()
            return redirect('/dashboard')
        except Error as e:
            MyError = e
            return render_template('addstudent.html',error=MyError)


@app.route('/quiz/add',methods=['GET','POST'])
def add_quiz():
    if session['logged_in'] != True:
        error="You are not logged in"
        return redirect('/login',error=error)
    elif request.method == 'GET':
        return render_template('addquiz.html')
    elif request.method == 'POST':
        MyError=""
        try:
            db = get_db()
            QS = request.form["QuizSubject"]
            QQ = request.form["QuizNumQues"]
            QD = request.form["QuizDate"]
            db.execute('insert into tblQuiz (QuizSubject,QuizNumQues,QuizDate) values (?,?,?)',(QS,QQ,QD))
            db.commit()
            return redirect('/dashboard')
        except Error as e:
            MyError = e
            return render_template('addquiz.html',error=MyError)


@app.route('/results/add',methods=['GET','POST'])
def add_quiz_results():
    if session['logged_in'] != True:
        error="You are not logged in"
        return redirect('/login',error=error)
    elif request.method == 'GET':
        db = get_db()
        cur = db.execute('Select * from tblStudent')
        students  = cur.fetchall()
        cur = db.execute('Select * from tblQuiz')
        quizzes = cur.fetchall()
        return render_template('addresult.html',students=students,quizzes=quizzes)
    elif request.method == 'POST':
        MyError=""
        try:
            db = get_db()
            sID = request.form["StudentID"]
            qID = request.form["QuizID"]
            Score = request.form["QuizScore"]
            db.execute('insert into tblResults (StudentID,QuizID,Score) values (?,?,?)',(sID,qID,Score))
            db.commit()
            return redirect('/dashboard')
        except Error as e:
            MyError = e
            return render_template('addresult.html',error=MyError)


@app.route('/student/<id>',methods=['GET','POST'])
def display_results(id):
    if session['logged_in'] != True:
            error="You are not logged in"
            return redirect('/login',error=error)
    else:
        db = get_db()
        SQLString = """SELECT a.StudentID, a.StudentFirstName, a.StudentLastName, 
        b.QuizSubject, b.QuizDate, c.Score
        FROM tblStudent AS a 
        INNER JOIN tblResults AS c ON a.StudentID = c.StudentID 
        INNER JOIN tblQuiz AS b ON b.QuizID = c.QuizID
        WHERE a.StudentID = """ + str(id)
        cur = db.execute(SQLString)
        studentscores  = cur.fetchall()
        try:
            studentscores[0]
            return render_template('studentresults.html',studentscores=studentscores)
        except IndexError:
            error="Student Record Not Found"
            return render_template('studentresults.html',error=error)


if __name__ == '__main__':
    app.run(debug=True)