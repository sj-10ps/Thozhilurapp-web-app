from flask import *
from database import *
import stripe
import os
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

stripe.api_key=STRIPE_API_KEY  



payment=Blueprint('payment',__name__)

@payment.route('/payment_home')
def payment_home():
    return render_template('payment_home.html')



@payment.route('/Wage')
def Wage():
    data={}
    qry1="select work.description,wage.total,wage.date,work.ward,wage.wage_id from wage inner join work using(work_id) where wage.status='approved' "
    res1=select(qry1)
    qry2="select work.description,wage.total,wage.date,work.ward from wage inner join work using(work_id) where wage.status='paid' "
    res2=select(qry2)
    if res1:
       data['data']=res1
    if res2:
       data['paid']=res2
    return render_template('wages.html',data=data)




@payment.route('/payment_page',methods=['get','post'])
def payment_page():
    # Extract the ward, amount, and bank account from the URL parameters
    ward = request.args['ward']
    amt = request.args['amt']
    wage_id=request.args['id']
    print(wage_id)

    
    qry1="select * from ward_payment where ward='%s'"%(ward)
    res1=select(qry1)
    bank_account=res1[0]['bank_no']

    if 'submit' in request.form:
        qry2="update wage set status='paid' where wage_id='%s'"%(wage_id)
        ress=update(qry2)
        if ress:
             return "<script>alert('Status Updated');window.location.href='Wage'</script>"

        
        

    # Render the payment page with the extracted data
    return render_template('payment_page.html', ward=ward, amt=amt, bank_account=bank_account)

@payment.route('/insurance')
def insurance():
    data={}
    qry1="select * from insurance where status='pending'"
    data['granted']=select(qry1)
    qry2="select * from insurance where status='paid'"
    data['paid']=select(qry2)
   
    return render_template('insurances.html',data=data)



@payment.route('/insurance_payment',methods=['get','post'])
def insurance_payment():
    # Extract the ward, amount, and bank account from the URL parameters
    card_no = request.args['card']
    amt = request.args['amt']
    insurance_id=request.args['id']
  

    
    qry1="select * from work_card where card_no='%s'"%(card_no)
    res1=select(qry1)
    bank_account=res1[0]['bank_no']

    if 'submit' in request.form:
        qry2="update insurance set status='paid' where insurance_id='%s'"%(insurance_id)
        ress=update(qry2)
        if ress:
             return "<script>alert('Status Updated');window.location.href='insurance'</script>"

        
        

    # Render the payment page with the extracted data
    return render_template('insurance_payment_page.html', card=card_no, amount=amt, bank_account=bank_account)


       
  









@payment.route('/payment_logout',methods=['get','post'])
def payment_logout():
    
    if 'confirm' in request.form:
        return redirect(url_for('public.home'))
            
            
    elif 'cancel' in request.form:
         return redirect(url_for('payment.payment_home'))             
         
    
   
       
    return render_template('logout.html')