from flask import *
from sqlite3 import *
from hashlib import *
import random
import yagmail
from datetime import *
from csv import *


def calc_sha256_salted(data):
    data = 'mypersonal' + str(data) + 'website'
    if isinstance(data,str):
        data = data.encode()
    return sha256(data).hexdigest()


app = Flask(__name__)
app.secret_key = 'gradaholic2024mikaeel'
##########################################################################################
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


#############################################################################################
@app.route('/register-pesonal-details',methods=['POST','GET'])
def register_personal_details():
	email = request.form.get('email')
	print('email:',email)
 	
	db = connect('db.db')
	c = db.cursor()
	c.execute('''
		SELECT * FROM Users
		WHERE email = ?
	''', (email,))
	duplicate = bool(c.fetchone())
	db.close()
	if duplicate:
		flash('Email has already been used. Login instead')
		return redirect(url_for('index'))
	else:
		return render_template('register-personal-details.html',email=email)
	


#########################################################################################
	
@app.route('/signin',methods=["POST","GET"])
def signin():
	return render_template('signin.html')



############################################################################################
@app.route('/profile',methods=["POST","GET"])
def profile():
	if request.method=="GET":
		username = session.get('username')
		return render_template('profile.html',username=username)
	
	prevpage = request.form.get('currpage')
	print('prevpage:',prevpage)
	if prevpage == 'login':
		username = request.form.get("username")
		session['username'] = username
		pw = request.form.get("pw")
		hashpw = calc_sha256_salted(pw)
		print((username,pw,hashpw))
		db = connect('db.db')
		c = db.cursor()
		c.execute('''
			SELECT * FROM Users
			WHERE username = ? AND hashedpw=?
		''',(username,hashpw))
		valid = c.fetchone()
		print('valid:',valid)
		db.close()
		print(username)
		if valid!=None:
			return render_template("profile.html",username=username)
		else:
			flash('Invalid Username/Password')
			return redirect(url_for('signin'))
		
		
	# elif prevpage == 'register-personal-details':
	username = request.form.get('username')
	name = request.form.get('name')
	pw = request.form.get('pw')
	rpw = request.form.get('rpw')
	hashpw = calc_sha256_salted(pw)
	# email = session.get('email')
	email = request.form.get('email')
	date_time=str(datetime.now())

	print((username,name,pw,email,date_time,0))
	if pw!=rpw:
		flash('Passwords do not match')
		return redirect(url_for('register_personal_details'))
	
	db = connect('db.db')
	c = db.cursor()
	c.execute('''
		SELECT * FROM USERS WHERE username=?
	''',(username,))
	duplicate = c.fetchone()
	print("duplicate: ",duplicate)
	if duplicate!=None:
		flash('Username taken')
		db.close()
		return redirect(url_for('register_personal_details'))
	
	print('hi')
	c.execute('''
		INSERT INTO Users (username,name,hashedpw,email,registration_date,admin) 
		VALUES(?,?,?,?,?,?)
	''', (username,name,hashpw,email,date_time,0))
	db.commit()
	db.close()
	return render_template('profile.html',username=username)
	

###########################################################################
@app.route('/add',methods=["POST","GET"])
def add():
	file = open('h2-subjects.csv')
	h2_subjects = []
	for subject in file:
			h2_subjects.append(subject.strip())
	session['h2_subjects'] = h2_subjects

	file = open('h2-subjects.csv')
	h1_subjects = []
	for subject in file:
			h1_subjects.append(subject.strip())
	session['h1_subjects'] = h1_subjects
	username = session.get('username')
	return render_template('add.html',username=username,h2=h2_subjects,h1=h1_subjects)

@app.route('/add-success',methods=["POST","GET"])
def addsuccess():
	year = str(datetime.now())[:4]
	message="Grades Added"
	username = session.get('username')
	examtype = request.form.get('examtype')
	h2_1 = request.form.get('h2_1_grade')
	h2_2 = request.form.get('h2_2_grade')
	h2_3 = request.form.get('h2_3_grade')
	h2_h1 = request.form.get('h2_h1')
	gp = request.form.get('gp')
	pw = request.form.get('pw')
	grades = [h2_1,h2_2,h2_3,h2_h1,gp,pw]

	sub1 = request.form.get('h2_1')
	sub2 = request.form.get('h2_2')
	sub3 = request.form.get('h2_3')
	sub4 = request.form.get('h2or1')
	sub5 = 'gp'
	sub6 = 'pw'
	subjects = [sub1,sub2,sub3,sub4,sub5,sub6]

	print(grades)
	print(subjects)
	db = connect('db.db')
	c = db.cursor()
	c.execute('''
		INSERT INTO Exams (type,year)
		VALUES (?,?)
	''', (examtype,year))
	
	c.execute('''
		SELECT id FROM Exams 
		WHERE type=? and year=?
	''',(examtype,year))
	examid = c.fetchone()[0]

	c.execute('''
		SELECT id FROM Users
		WHERE username=?
	''',(username,))
	userid = c.fetchone()[0]
	print('userid:',userid)

	for i in range(0,len(subjects)):
		c.execute('''
			INSERT INTO Paper (subject,examID)
			VALUES (?,?)
		''',(subjects[i],examid))

		c.execute('''
			SELECT id FROM Paper
			WHERE subject=?
		''',(subjects[i],))
		paperid=c.fetchone()[0]

		print('curr userid',userid)
		c.execute('''
			INSERT INTO UserGrade (grade, paperID, usersID)
			VALUES (?,?,?)
		''',(grades[i],paperid,userid))


	db.commit()
	db.close()


	
	return render_template('add.html',message=message,username=username,h2=session.get('h2_subjects'),h1=session.get('h1_subjects'))

##############################################################################
@app.route('/leaderboard',methods=['GET'])
def leaderboard():
	username = session.get('username')
	return render_template('leaderboard.html',username=username)
##############################################################################
@app.route('/notifications',methods=['GET'])
def notifications():
	username = session.get('username')
	return render_template('notifications.html',username=username)
#########################################################################
@app.route('/settings',methods=['GET'])
def settings():
	username = session.get('username')
	return render_template('settings.html',username=username)
###############################################################################
@app.route('/help', methods=["GET"])
def help():
	username = session.get('username')
	return render_template('help.html',username=username)


if __name__ == '__main__':
	app.run(debug=True,port=5055)
