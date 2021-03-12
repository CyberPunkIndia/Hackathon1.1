from flask import Flask,\
	render_template,\
	url_for,\
	redirect,\
	request,\
	session
from datetime import timedelta,datetime
import json,hashlib


user_json = json.load(open("json/user.json"))
question_json = json.load(open("json/questions.json"))

user_data = [user_json,question_json,"Guest"]

app = Flask("Help desk")
app.secret_key = "DAJ7824RHEW742ORWIUYEH2OWIUERS"
app.permanent_session_lifetime = timedelta(days=5)


@app.route("/",methods =["GET","POST"])
def index():
	global user_data
	if 'user' in session:
		user_data[-1] = session['user']
	if request.method == "POST":
		if user_data[-1] == "Guest":
			return redirect(url_for('login'))
		else:
			question = request.form["question"]
			return redirect(url_for('asknow',uid = question))

	return render_template("index.html",usr_dat = user_data)

app.add_template_global(lambda : redirect(url_for('index')), name='index')

@app.route("/login/",methods =["GET","POST"])
def login():
	if 'user' in session:
		return redirect(url_for('profile'))
	global user_data
	formed ,usrd = None,None
	try:
		formed = request.form["question"]
		usrd = request.form["usermail"]
	except:
		pass
	if request.method == "POST":
		if not formed:
			try:
				usr = hashlib.sha1(request.form["usermail"].encode()).hexdigest()
				passwd = request.form["password"]
			except:
				return render_template("login.html",usr_dat = user_data)
			if usr in user_data[0] and passwd == user_data[0][usr]["password"]:
				user_data[-1] = usr 
				session['user'] = usr 
				return redirect(url_for("profile"))
			return redirect(url_for("index"))
			user_data[-1] = "Guest"
		else:
			return redirect(url_for('login'))

	return render_template("login.html",usr_dat = user_data)

@app.route("/logout")
def logout():
	user_data[-1] = "Guest"
	session.pop('user',None)
	return redirect(url_for('index'))


@app.route("/Profile/",methods=["GET","POST"])
def profile():
	global user_data
	if user_data[-1] == "Guest":
		return redirect(url_for('login', _method = 'POST',usr_dat = user_data))
	return render_template("profile.html",usr_dat= user_data)

@app.route("/signup/",methods =["GET","POST"])
def signup():
	global user_data
	if request.method == "POST":
		user_name = request.form["user_name"]
		passwd = request.form["passwd"]
		email = request.form["email"]
		mob = request.form['mob']
		zender =request.form['zender'] 
		branch = request.form["branch"]
		user_type = request.form['proffesion']
		user_has = hashlib.sha1(email.encode()).hexdigest()
		if branch == 'falsed' or user_type == 'falsed':
			return redirect(url_for('signup'))
		user_data[0][user_has] = {
		"user_type" : user_type,
		"user_name" : user_name,
		"email" : email,
		"branch" : branch,
		"zender" : zender,
		"password" : passwd,
		"question_asked" : [],
		"notification" : []
		}
		file = open("json/user.json",'w')
		json.dump(user_data[0],file)
		file.close()
		user_data[0] = json.load(open('json/user.json'))
		if user_type == 'student':
			return redirect(url_for("index",usr_dat=user_data))
		else:
			return redirect(url_for('dashboard',usr_dat = user_data))
	return render_template("create_account.html",usr_dat =  user_data)


@app.route('/asknow/<uid>')
def asknow(uid):
	global user_data
	if request.method == 'POST':
		question = request.form['question']
	else:
		question = uid
	uid = hashlib.sha1(uid.encode()).hexdigest()
	user_data[1][uid] = {
	"branch" : user_data[0][user_data[-1]]["branch"],
	"asked_by" : user_data[-1],
	"answered_by" : "",
	"qnstime" : str(datetime.today()),
	"anstime" : "",
	"question" :question,
	"answer" : ""
	}
	for ids in user_data[0]:
		if user_data[0][ids]['user_type'] == "HOD" and user_data[0][ids]['branch'] == user_data[0][user_data[-1]]["branch"]:
			user_data[0][ids]['notification'].append(uid)
			user_data[0][user_data[-1]]['question_asked'].append(question)
			break
	file = open('json/questions.json','w')
	json.dump(user_data[1],file)
	file.close()
	return redirect(url_for('profile'))

@app.route("/Dashboard",methods =["GET","POST"])
def dashboard():
	return render_template("dashboard.html",usr_dat=user_data )

@app.route("/answer/<qid>")
def answer(qid):
	global user_data
	return render_template('answer.html',qid = qid,usr_dat = user_data)


@app.route("/ComputerScience/")
def ComputerScience():
	return render_template("ComputerScience.html",usr_dat=user_data)

@app.route("/InformationTechnology/")
def InformationTechnology():
	return render_template("InformationTechnology.html",usr_dat=user_data)


@app.route("/CivilEngineering/")
def CivilEngineering():
	return render_template("CivilEngineering.html",usr_dat=user_data)


@app.route("/MechanicalEngineering/")
def MechanicalEngineering():
	return render_template("MechanicalEngineering.html",usr_dat=user_data)

@app.route("/ElectricalEngineering/")
def ElectricalEngineering():
	return render_template("ElectricalEngineering.html",usr_dat=user_data)

@app.route("/Electronics/")
def Electronics():
	return render_template("Electronics.html",usr_dat = user_data)

@app.route("/Question/<hashid>")
def Question(hashid):
	global user_data
	return render_template("QuestionView.html",qid = hashid,usr_dat = user_data)

@app.route("/notify/<qid>/<usrid>")
def notify():
	global user_data
	user_data[0][usrid]['notification'].append(qid)
	global user_json,question_json
	user_json.close()
	user_json = json.load(open("json/user.json","w"))
	json.dump(user_data[0],user_json)
	user_json.close()
	user_data[0] = json.load("json/user.json")
	return redirect(url_for("Dashboard"))




if __name__ == '__main__':
	app.run(debug = False)