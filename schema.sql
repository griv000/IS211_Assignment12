DROP TABLE IF EXISTS tblStudent;
DROP TABLE IF EXISTS tblQuiz;
DROP TABLE IF EXISTS tblResults;

CREATE TABLE tblStudent (
    StudentID INTEGER PRIMARY KEY,
    StudentFirstName TEXT,
    StudentLastName TEXT
);

CREATE TABLE tblQuiz (
    QuizID INTEGER PRIMARY KEY,
    QuizSubject TEXT,
    QuizNumQues INTEGER,
    QuizDate DATE
);

CREATE TABLE tblResults (
    StudentID INTEGER,
    QuizID INTEGER,
    Score INTEGER
);

INSERT INTO tblStudent VALUES (1,'John','Smith');
INSERT INTO tblQuiz VALUES (1,'Python Basics',5,'2015-02-05');
INSERT INTO tblResults VALUES (1,1,85);