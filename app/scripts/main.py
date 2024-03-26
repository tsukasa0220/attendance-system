from flask import Flask, render_template, request, redirect, Response, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AttendanceDB, NameDB
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)

# SQLiteデータベースに接続
engine2 = create_engine('sqlite:///name.db')
engine1 = create_engine('sqlite:///attendance.db')

# SQLAlchemyセッションを作成
Session1 = sessionmaker(bind=engine1)
Session2 = sessionmaker(bind=engine2)

def compute_day(post, onDays):
    for onDay in onDays:
        if post == onDay:
            return 0
    return 1

def extrack_name(my_names, post):
    for my_name in my_names:
        if my_name == post.name:
            return 0
    return post.name

error = ['',0]
def error_handle(e):
    if e and error[1]:
        error[0] = e
        return ''
    elif error[0] and error[1] == 0:
        error[0] = ''
        return error[0]
    else:
        error[1] = 0
        return error[0]

# URL:(/)
@app.route('/attendance', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            subprocess.run('sh /app/scripts/getFile.sh', shell=True, check=True)
        except subprocess.CalledProcessError as e:
            error[1] = 1
            e = error_handle(e)
        return redirect('/attendance')

    session1 = Session1()
    posts = session1.query(AttendanceDB).order_by(AttendanceDB.date.desc()).all()
    onDays = []
    for post in posts:
        post = post.date.strftime('%Y-%m-%d')
        if compute_day(post, onDays):
            onDays.append(post)

    session1.close()
    errorOut = error_handle(0)
    return render_template('index.html', onDays=onDays, error=errorOut)

# URL(/date/<指定した日付>)
@app.route('/attendance/date/<currentDate_str>', methods=['GET', 'POST'])
def date(currentDate_str):
    if request.method == 'POST':
        session1 = Session1()
        session2 = Session2()
        name = request.form.get('name')

        number = session2.query(NameDB.number).filter(NameDB.name == name).scalar()
        grade = session2.query(NameDB.grade).filter(NameDB.name == name).scalar()

        currentDate = datetime.strptime(currentDate_str, "%Y-%m-%d")

        new_post = AttendanceDB(number=number, name=name, grade=grade, date=currentDate)

        session1.add(new_post)
        session1.commit()
        session1.close()

        return redirect(f'/attendance/date/{currentDate_str}')

    currentDate = datetime.strptime(currentDate_str, "%Y-%m-%d")
    session1 = Session1()
    posts = session1.query(AttendanceDB).order_by(AttendanceDB.number).filter(AttendanceDB.date >= currentDate, AttendanceDB.date < currentDate+timedelta(days=1)).all()
    session1.close()

    session2 = Session2()
    posts2 = session2.query(NameDB).order_by(NameDB.number).all()
    session2.close()

    my_names = [100]
    for post in posts:
        tmp_name = extrack_name(my_names, post)
        if tmp_name != 0:
            my_names.append(tmp_name)
    posts = session1.query(AttendanceDB).order_by(AttendanceDB.date).filter(AttendanceDB.date >= currentDate, AttendanceDB.date < currentDate+timedelta(days=1)).all()
    return render_template('date.html', posts=posts, currentDate=currentDate_str, posts2=posts2, my_names=my_names)

# URL(/user/<指定した学籍番号>)
@app.route('/attendance/user/<currentNumber>', methods=['GET', 'POST'])
def user(currentNumber):
    if request.method == 'GET':
        session1 = Session1()
        session2 = Session2()
        posts = session1.query(AttendanceDB).order_by(AttendanceDB.date.desc()).filter(AttendanceDB.number == currentNumber).all()
        lasts = session2.query(NameDB).filter(NameDB.number == currentNumber).first()
        session1.close()
        session2.close()
        return render_template('user.html', posts=posts, lasts=lasts, currentNumber=currentNumber)
    
    else:
        session2 = Session2()
        post = session2.query(NameDB).filter(NameDB.number == currentNumber).first()

        number = request.form.get('number')
        if number != '':
            post.number = number
            currentNumber = number
        name = request.form.get('name')
        if name != '':
            post.name = name
        grade = request.form.get('grade')
        if grade != '':
            post.grade = grade

        session2.commit()
        session2.close()
        return redirect(f'/attendance/user/{currentNumber}')

# URL(/delete/<指定したAttendanceDBのid>)
@app.route('/attendance/delete/<int:id>')
def delete(id):
    from_url = request.referrer
    split_url = from_url.partition('/attendance/')

    session1 = Session1()
    post = session1.query(AttendanceDB).get(id)
    session1.delete(post)
    session1.commit()
    session1.close()
    return redirect(f'/attendance/{split_url[-1]}')

# URL(/member)
@app.route('/attendance/member', methods=['GET', 'POST'])
def member():
    if request.method == 'GET':
        session2 = Session2()
        posts = session2.query(NameDB).order_by(NameDB.number).all()
        session2.close()
        return render_template('member.html', posts=posts)

    else:
        number = request.form.get('number')
        name = request.form.get('name')
        grade = request.form.get('grade')
        new_post = NameDB(number=number, name=name, grade=grade)

        session2 = Session2()
        session2.add(new_post)
        session2.commit()
        session2.close()
        return redirect('/attendance/member')

# URL(/member/delete/<指定したNameDBのid>)
@app.route('/attendance/member/delete/<int:id>')
def delete_member(id):
    session2 = Session2()
    post = session2.query(NameDB).get(id)

    session2.delete(post)
    session2.commit()
    session2.close()
    return redirect('/attendance/member')

# URL(/other)
@app.route('/attendance/other', methods=['GET', 'POST'])
def other():
    other_date = request.form.get('other')
    return redirect(f'/attendance/date/{other_date}')

# main
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)