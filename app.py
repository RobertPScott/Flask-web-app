from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, \
    logout_user, current_user, login_required
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
id = -1
appid = -1

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80))
    password = db.Column(db.String(80))
    applocation = db.relationship('applications', backref='user')

class applications(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))
    Age = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

app.config['SECRET_KEY'] = '12345'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    user = Users.query.get(uid)
    return user


DOGS = [
  {
    'id':1,
    'name':'Max',
    'age':2,
    'location':'New York, NY',
    'sex' : 'M',
    'image': 'Max.jpg'
  },
  {
    'id':2,
    'name':'Scout',
    'age':1,
    'location':'Denver, CO',
    'sex' : 'F',
    'image': 'Scout.jpg'
  },
  {
    'id':3,
    'name':'Rex',
    'age':5,
    'location':'Charlotte, NC',
    'sex' : 'M',
    'image': 'Rex.jpg'
  },
  {
    'id':4,
    'name':'Melvin',
    'age':2,
    'location':'Colorado Springs, CO',
    'sex' : 'M',
    'image': 'Melvin.jpg'
  }
]

@app.route('/')
def hello_world():
    # login = False
    return render_template('home.html', dogs = DOGS, login=login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(userName=userName).first()

        if userName != user.userName or password != user.password:
            uniqueName = False
            return render_template('login.html', uniqueName=uniqueName, dogs = DOGS,)

        global id
        id = user.id

        login_user(user)
        login = True
        return render_template('home.html', login=login, dogs = DOGS,)

    elif request.method == 'GET':
        uniqueName = True
        return render_template('login.html', dogs = DOGS,)

@app.route('/logout')
@login_required
def logout():

    logout_user()
    login=False
    return render_template('home.html', login=login)

@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']

        tempUser = Users(userName = userName, password = password)
        user = Users.query.filter_by(userName=request.form['username']).first()

        if user != None:
            uniqueName = False
            return render_template('createUser.html', uniqueName=uniqueName, dogs = DOGS)

        db.session.add(tempUser)
        db.session.commit()
        user = Users.query.filter_by(userName = request.form['username']).first()
        global id
        id = user.id
        login_user(user)
        login = True
        return render_template('home.html', login=login, dogs = DOGS)
    elif request.method == 'GET':
        uniqueName = True
        return render_template('createUser.html', dogs = DOGS)

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        Name = request.form['Name']
        Age = request.form['Age']

        temp = applications(Name=Name, Age=Age, user_id=id)

        db.session.add(temp)
        db.session.commit()
        login = True
        return render_template('home.html', login=login)

    elif request.method == 'GET':
        return render_template('apply.html')

@app.route('/read')
@login_required
def retrieve():
    global id
    results = applications.query.filter_by(user_id=id).all()
    return render_template("read.html", results = results)

class AppStruct:
    pass

@app.route('/update/<app_id>', methods=['GET', 'POST'])
@login_required
def update(petid):
    if request.method == 'POST':
        results = applications.query.filter_by(id=appid).first()
        Name = request.form['Name']
        Age = request.form['Age']

        results.Name = Name
        results.Age = Age

        db.session.commit()
        return render_template("home.html", login=True)
    elif request.method == 'GET':
        return render_template("update.html", id=appid)



    if request.method == 'POST':
        global Appsid
        Appsid = appid
        return

@app.route('/delete/<appid>', methods=['POST'])
@login_required
def delete(appid):
    if request.method == 'POST':
        results = applications.query.filter_by(id=appid).first()
        db.session.delete(results)
        db.session.commit()
        return render_template("home.html", login=True)

@app.route('/aboutus')
def about():
    return render_template('aboutus.html')

@app.errorhandler(400)
def err404(err):
    return render_template("err.html", errNum = 401, typeErr = err, login = False)
@app.errorhandler(403)
def err404(err):
    return render_template("err.html", errNum = 403, typeErr = err, login = False)
@app.errorhandler(404)
def err404(err):
    return render_template("err.html", errNum = 404, typeErr = err, login = False)
@app.errorhandler(502)
def err404(err):
    return render_template("err.html", errNum = 502, typeErr = err, login = False)

app.app_context().push()
if __name__ == '__main__':
  # db.create_all()
  app.run(host='0.0.0.0', debug=True)
