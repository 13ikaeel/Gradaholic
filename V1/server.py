from flask import *
from sqlite3 import *
from hashlib import *
import random
import yagmail


def calc_sha256_salted(data):
    data = 'mypersonal' + str(data) + 'website'
    if isinstance(data,str):
        data = data.encode()
    return sha256(data).hexdigest()


app = Flask(__name__)
app.secret_key = 'essaywebsite2024mikaeel'

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


@app.route('/register-pesonal-details',methods=['POST'])
def register_personal_details():
	email = request.form.get('email')
 	
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
		redirect(url_for('index'))
	else:
		return render_template('register-personal-details.html',email=email)
	

@app.route('/login',methods=["GET","POST"])
def login():
	return render_template('login.html')


@app.route('/about-us', methods=["GET","POST"])
def about_us():
	return render_template('about_us.html')


@app.route('/contact-us', methods=["GET","POST"])
def contact_us():
	return render_template("contact_us.html")


@app.route('/contact/contact-success', methods=['POST'])
def contact_success():
	print('contact success')
	return


@app.route('/profile',methods=["GET","POST"])
def profile():
	prevpage = request.form.get('currpage')

	if prevpage == 'login':
		username = request.form.get("username")
		pw = request.form.get("pw")
		hashpw = calc_sha256_salted('pw')
		db = db.connect('db.db')
		c = db.cursor()
		c.execute('''
			SELECT * FROM Users
			WHERE username = ? AND hashedpw=?
		'''(username,hashpw))
		valid = c.fetchone()
		db.close()
		if valid:
			return render_template("profile.html")
		else:
			flash('Invalid Username/Password')
			return redirect(url_for('login'))
		
	# elif prevpage == 'register-personal-details':
	else:
		pw = request.form.get('pw')
		cfm_pw = request.form.get('cfm_pw')
		if pw!=cfm_pw:
			flash('Passwords do not match')
			return redirect(url_for('register_personal_details'))
		username = request.form.get('username')
		hashpw = calc_sha256_salted(pw)
		email = request.form.get('email')
		print([username,hashpw,email,0,0])
		db = connect('db.db')
		c = db.cursor()
		c.execute('''
			SELECT * FROM USERS WHERE username=?
		''',(username,))
		duplicate = c.fetchone()
		if duplicate:
			flash('Username taken')
			db.close()
			return redirect(url_for('register_personal_details'))
		c.execute('''
			INSERT INTO Users (username,hashedpw,email,rp,admin) 
			VALUES(?,?,?,?,?)
		''', (username,hashpw,email,0,0))
		db.close()
		return render_template('profile.html',username=username, RP=0)
	





if __name__ == '__main__':
	app.run(debug=False,port=5055)
