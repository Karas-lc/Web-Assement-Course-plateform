from flask import render_template, flash, redirect, request, url_for, session, jsonify

from appdir import app, db
from appdir.forms import RegisterForm, LoginForm, NewCourseForm, CourseRegisterForm
from appdir.models import User, Course


@app.route('/', endpoint='main', methods=["GET", "POST"])
def main():
    session.clear()
    return render_template("auth/main.html")


@app.route("/auth/login", endpoint='login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    # clear up the session
    if form.validate_on_submit():
        # get the login's information, then the system check if the password, id is right or no
        ID = form.id.data
        password = form.password.data
        user = User.query.filter_by(id=ID).first()
        if user is not None:
            pas = user.passwords
            username = user.name
            if password == pas:
                session['userID'] = ID
                session['username'] = username
                session['password'] = password
                return redirect(url_for('home'))
            else:
                flash('Please check your information and try again!')
                return redirect(url_for('login'))
        else:
            flash('Please check your information and try again!')
            return redirect(url_for('login'))
    return render_template("auth/login.html", form = form)


@app.route("/auth/register", endpoint='register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print(form)
        # get the user's typed in information
        ID = form.id.data
        username = form.name.data
        password = form.password.data
        repassword = form.repassword.data
        email = form.email.data
        # if the userid is not in the database and the password and repassword is the same, put those information
        #   to the database and turn to the login page
        userthis = User.query.filter_by(id=ID).first()
        if userthis is not None:
            flash('The userid is already exited!')
            return redirect(url_for('register'))
        else:
            if password == repassword:
                user = User(id=ID,
                            name=username,
                            passwords=password,
                            email=email)
                db.session.add(user)
                db.session.commit()
                flash('Register successfully!')
                return redirect(url_for('login'))
    return render_template("auth/register.html", form = form)

@app.route("/details/<id>", methods=["GET", "POST"])
def details(id):
    # get the information of the selected course and show it to users
    data = Course.query.filter_by(id=id).first()
    print(data)
    return render_template("courses/course_details.html", data=data)

@app.route("/index/home", methods=["GET", "POST"])
def home():
    # show some registered courses to the user.
    course = Course.query.all()
    userid = session.get('userID')
    instant_data = []
    for item in course:
        students_id = item.StudentID.split(',')
        for j in students_id:
            if userid == j:
                instant_data.append(item)
        if userid == item.TeacherID:
            instant_data.append(item)
    return render_template("index/home.html", data=instant_data)

@app.route("/index/discussion", methods=["GET", "POST"])
def discussion():
    # let the user to get into the discussion page
    # user can get informations from others in the discussion page
    return render_template("index/discussion.html")

@app.route("/index/course", methods=["GET", "POST"])
def course():
    # this page will show all of the couses. If this user registered one course, he can get into the details page
    # to get more information; if this user have not registered it, he need to registed to it first
    courses = Course.query.all()

    students_ids_list = []
    for i in courses:
        students_ids_list.append(i.StudentID.split(','))

    return render_template("index/course.html", courses=courses, students_ids_list=students_ids_list)


@app.route("/courses/new_course", endpoint= 'new_course',methods=["GET", "POST"])
def new_course():
    form = NewCourseForm()
    # teachers with id's first letter"T" can add a new course
    couses = Course.query.all()
    couses_name_b = []
    for i in couses:
        couses_name_b.append(i.name)
    print(form.semester_year.data)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        course_name = form.name.data
        if course_name in couses_name_b:
            flash('Already has this name!')
            return redirect(url_for('new_course'))
        else:
            course_id = Course.query.count()
            course_key = form.key.data
            teacher_id = session.get('userID')
            course_name = form.name.data
            introduction = form.Introduction.data
            semester_year = ''
            if form.semester_year.data == '1':
                semester_year = "2021-2022"
            elif form.semester_year.data == '2':
                semester_year = "2022-2023"
            elif form.semester_year.data == '3':
                semester_year = "2023-2024"
            semester_term = form.semester_term.data
            semester = semester_year + " | "+ semester_term
            course = Course(id = course_id,
                            name= course_name,
                            key=course_key,
                            TeacherID= teacher_id,
                            StudentID="",
                            introduction=introduction,
                            semester=semester
                            )
            db.session.add(course)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("courses/new_course.html", form = form)


@app.route("/courses/course_register/<id>", methods=["GET", "POST"])
def course_register(id):
    # this page is the courses registering page, students put the right key to it and then their id will be added
    # up to this course's name list
    form = CourseRegisterForm()
    print()
    if form.validate_on_submit():
        key = form.key.data
        userid = session.get('userID')
        course = Course.query.filter_by(id=id).first()
        if key == course.key:
            student_id = course.StudentID
            s = student_id.split(',')
            s.append(userid)
            str = ','.join(s)
            print(str)
            Course.query.filter_by(id=id).update({'StudentID':str})
            db.session.commit()
            return redirect(url_for('course'))
        if key != course.key:
            flash('wrong keys!')
            return redirect(url_for('course'))
    return render_template("courses/course_register.html", form=form)


@app.route("/courses/my_courses", methods=["GET", "POST"])
def my_course():
    courses = Course.query.all()
    students_ids_list = []
    for item in courses:
        students_ids_list.append(item.StudentID.split(','))

    return render_template("courses/my_courses.html", courses=courses,students_ids_list=students_ids_list)

@app.route('/send_message', methods=['GET'])
def send_message():
    global message_get
    message_get = request.args['message']
    print("收到前端发过来的信息：%s" % message_get)
    print("收到数据的类型为：" + str(type(message_get)))
    return "Success!"

@app.route('/change_to_json', methods=['GET'])
def change_to_json():
    global message_get
    courses = Course.query.filter_by(semester=message_get).all()
    message_json = {}
    a = 0
    for item in courses:
        message_json[a] = [item.id, item.name, item.semester]
        a += 1
    for i in message_json:
        print(message_json[i])
    return jsonify(message_json)

@app.route('/send_message_home', methods=['GET'])
def send_message_home():
    global message_get1
    message_get1 = request.args['message']
    print(message_get1)
    return "Success!"

@app.route('/change_to_json_home', methods=['GET'])
def change_to_json_home():
    global message_get1
    courses = Course.query.filter_by(semester=message_get1).all()
    message_json = {}
    a = 0
    for item in courses:
        students_id = item.StudentID.split(',')
        for i in students_id:
            if i == session['userID']:
                message_json[a] = [item.id, item.name, item.semester]
                a += 1
    print(message_json)
    return jsonify(message_json)