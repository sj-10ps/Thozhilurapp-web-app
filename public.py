from flask import *
from database import *


public=Blueprint('public',__name__)
@public.route('/')
def home():
    return render_template('home.html')

@public.route('/home')
def homepage():
    return render_template('home.html')

@public.route('/public_about')
def public_about():
    return render_template('public_about.html')

@public.route("/login", methods=["get","post"])
def login():
    if 'submit' in request.form:
        username=request.form['uname']
        password=request.form['pword']

        qry1="select * from login where username='%s' and password='%s'"%(username,password)
        res1=select(qry1)

      
        if res1:
            session['log']=res1[0]['login_id']
            if res1[0]['user_type']=='admin':
                return redirect(url_for('admin.admin_home'))
            
            
            elif res1[0]['user_type']=='overseer':
                return redirect(url_for('overseer.overseer_home'))
            
            elif res1[0]['user_type']=='payment':
                return redirect(url_for('payment.payment_home'))
            
          
            

    return render_template("login.html")





