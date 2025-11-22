from flask import *
from database import *


admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
    return render_template('adminhome.html')

@admin.route('/manage_overseer')
def manage_overseer():
    return render_template('overseermanage.html')

@admin.route('/manage_mate')
def manage_mate():
    return render_template('matemanage.html')



@admin.route('/overseer_registration',methods=["get","post"])
def overseer_registration():  
    if 'reg' in request.form:
        firstname=request.form['fname']
        lastname=request.form['lname']  
        dob=request.form['dob']
        gender=request.form['gender']
        phone=request.form['phone']
        email=request.form['email']
        house=request.form['house']
        post=request.form['post']
        district=request.form['district']
        panchayat=request.form['panchayat']
       

        
        username=request.form['uname']
        password=request.form['pword']
        
     

        qry1="insert into login values(null,'%s','%s','overseer')"%(username,password)
        res1=insert(qry1)

        qry2="insert into mate values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',null,null,null,null,'overseer')"%(res1,firstname,lastname,dob,gender,phone,email,house,post,district,panchayat)
        res2=insert(qry2)
        return "<script>alert('registration done');window.location.href='overseer_registration'</script>"

    return render_template("overseer.html")

@admin.route('/mate_registration',methods=["get","post"])
def mate_registration():  
    if 'reg' in request.form:
        firstname=request.form['fname']
        lastname=request.form['lname']  
        dob=request.form['dob']
        gender=request.form['gender']
        phone=request.form['phone']
        email=request.form['email']
        house=request.form['house']
        post=request.form['post']
        district=request.form['district']
        panchayat=request.form['panchayat']
        ward=request.form['ward']
        username=request.form['uname']
        password=request.form['pword']
        qry1="insert into login values(null,'%s','%s','mate')"%(username,password)
        res1=insert(qry1)

        qry2="insert into mate values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','free','pending','0','mate')"%(res1,firstname,lastname,dob,gender,phone,email,house,post,district,panchayat,ward)
        insert(qry2)
        return "<script>alert('registration done');window.location.href='mate_registration'</script>"

 
    return render_template("mate.html")

@admin.route('/view_complaint',methods=['get','post'])
def view_complaint():
    data={}
    qry="select * from mate_complaint where reply='pending' or s_response='pending' "
    res=select(qry)
    data['com']=res
    qry3="select * from mate_complaint where reply!='pending' and s_response !='pending' "
    data['all']=select(qry3)

    
    if 'action' in request.args:
        action=request.args['action']   
        id=request.args['id']
        if action=='update':
            qry1="select * from mate_complaint where complaint_id='%s' "%(id)
            res1=select(qry1)
            if res1:
                data['rply']=res1

                if 'submit' in request.form:
                    reply=request.form['upd']
                   
                    
                    
                    qry2="update mate_complaint set reply='%s',reply_date=curdate() where complaint_id='%s'"%(reply,id)
                    update(qry2)
                   
                    return "<script>alert('replied succesfully');window.location.href='view_complaint'</script>"



    


    return render_template('view_complaints.html',data=data)


@admin.route('/mate_comdetails',methods=['get','post'])
def mate_comdetails():
    data={}
    var={}
    var2={}
    id=request.args['id']
    mate_id=request.args['mate_id']
    qry1="select * from mate_complaint where complaint_id='%s' "%(id)
    res1=select(qry1)
    if res1:
       data['comdetails']=res1
       qry2="select * from mate where officer_id='%s' "%(mate_id)
       res2=select(qry2)
    if res2:
       var['mate']=res2
       
    
        
    
   
    return render_template('mate_comdetails.html',data=data,var=var,var2=var2)

@admin.route('/send_complaint',methods=['get','post'])
def send_complaint():
    data={}
    id=request.args['id']

    qry1="select * from mate_complaint where complaint_id='%s'"%(id)
    res1=select(qry1)  
    data['response']=res1
  
    if 'submit' in request.form:
         response=request.form['response']
         qry2="update mate_complaint set s_response='%s',sr_date=curdate() where complaint_id='%s'"%(response,id)
         update(qry2)
         #return redirect(url_for('admin.view_complaint'))
         return "<script>alert('replied succesfully');window.location.href='view_complaint'</script>"
         




    return render_template('send_complaint.html',data=data)

@admin.route('/work_details',methods=['get','post'])
def work_details():

    return render_template('work_home.html')

@admin.route('/estimated_works',methods=['get','post'])
def estimated_works():
    data={}
    qry1="select * from work where status='pending' ORDER BY work_id"
    res1=select(qry1)
    if res1:
       data['work']=res1
       if 'action' in request.args:
           action=request.args['action']
           id=request.args['id']
           if action=='update':
               qry2="select * from work where work_id='%s'"%(id)
               res2=select(qry2)
               if res2:
                  data['approve']=res2
                  if 'submit' in request.form:
                      approval=request.form['ar']
                      
                      qry3="update work set status='%s' where work_id='%s'"%(approval,id)
                      update(qry3)
                      
                      if approval=='approved':
                          qry4="update work set start_date=curdate() where work_id='%s'"%(id)
                          update(qry4)
                      return "<script>alert('work status updated successfully');window.location.href='estimated_works'</script>"
                          
                     # return redirect(url_for('admin.estimated_works'))
                      
    qry5="select * from work where status='approved' ORDER BY work_id"
    data['approved']=select(qry5)
                 

              
               
           


    return render_template('estimated_works.html',data=data)


@admin.route('/work_progress',methods=['get','post'])
def work_progress():
    data={}
    qry1="select * from work"
    res1=select(qry1)
    if res1:
        data['attend']=res1
    return render_template('work_progress.html',data=data)

@admin.route('/duty_report',methods=['get','post'])
def duty_report():
    
    
    return render_template('duty_report.html')

@admin.route('/completed_works',methods=['get','post'])
def completed_works():
    data={}
    qry1="select * from work where progress='100' "
    data['com_works']=select(qry1)
    # qry1="select * from work where progress='100' and wage_status='approved'"
    # data['wage_approved']=select(qry1)


    return render_template('completed_works.html',data=data)

@admin.route('/attendance_report',methods=['get','post'])
def attendance_report():
    data={}
    id=request.args['id']
    qry1="select count(distinct(date)),work_id from work_report where work_id='%s'"%(id)
    
    data['att']=select(qry1)

    qry2="select * from work_report where work_id='%s' order by card_no"%(id)
    

    data['card']=select(qry2)
    
  
   
    return render_template('attendance_report.html',data=data)

@admin.route('/wage_estimation',methods=['get','post'])
def wage_estimation():
    data={}
    id=request.args['id']
 
    
    

    qry1="select  count(report_id) from work_report where work_id='%s' and status='50'"%(id)
    count=select(qry1)

    if count:

        
        half_day=int(count[0]['count(report_id)'])
        total_wage_half=half_day*173


    qry2="select  count(report_id) from work_report where work_id='%s' and status='100'"%(id)
    count2=select(qry2)

    if count2:
        full_day=int( count2[0]['count(report_id)'])
        total_wage_full=full_day*346

    total_amount=int(total_wage_half)+int(total_wage_full)

    a="select * from wage where work_id='%s'"%(id)
    wk=select(a)
    data['est']=select(a)

    if not wk:

        if total_amount:
            qry3="insert into wage values(null,'%s','%s','pending','pending','pending')"%(id,total_amount)
            insert(qry3)
            
         
    
    qry4="select * from wage where work_id='%s'"%(id)
    data['est']=select(qry4)

   

    return render_template('wage_estimation.html',data=data)

@admin.route('/wage_approval',methods=['get','post'])
def wage_approval():
    data={}
    
    if 'action' in request.args:
        action=request.args['action']
        wage_id=request.args['wage_id']
        work_id=request.args['work_id']
        if action=='update':
            qry1="select * from wage where wage_id='%s'"%(wage_id)
            res1=select(qry1)
            if res1:
                data['wage']=res1
                if 'submit' in request.form:
                    description=request.form['description']
                    status=request.form['ar']
                    
                    qry2="update wage set description='%s',status='%s' where wage_id='%s'"%(description,status,wage_id)
                    res2=update(qry2)
                    if res2:
                        qry4="update work set wage_status='approved' where work_id='%s'"%(work_id)
                        update(qry4)
                    
                  
                    return "<script>alert('DONE');window.location.href='completed_works'</script>"
                  
                    #return redirect(url_for('admin.completed_works'))
                   
              
                    
 

    return render_template('wage_estimation.html',data=data)

# @admin.route('/work_progress_details',methods=['get','post'])
# def work_progress_details():
    
    
#     return render_template('work_details.html')

@admin.route('/work_progress_details',methods=['get','post'])
def work_progress_details():
    data={}
    qry1="select * from work where progress!=100 and status='approved'"
    res1=select(qry1)
    data['owp']=res1
    
    return render_template('ow_progress.html',data=data)

@admin.route('/ow_details',methods=['get','post'])
def ow_details():
    data={}
    id=request.args['id']
    qry1="select * from mate_feedback where work_id='%s'"%(id)
    data['owd']=select(qry1)
    return render_template('ow_progress.html',data=data)

@admin.route('/reply_response',methods=['get','post'])
def reply_response():
    data={}
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        if action=='update':
           qry1="select * from mate_feedback where feedback_id='%s'"%(id)
           data['reply'] =select(qry1)
           if 'submit' in request.form:
               reply=request.form['reply']
               qry2="update mate_feedback set reply='%s' where feedback_id='%s'"%(reply,id)
               update(qry2)
               #return redirect(url_for('admin.ow_progress'))
               return "<script>alert('replied succesfully');window.location.href='ow_progress'</script>"
               

    
    return render_template('ow_progress.html',data=data)

@admin.route('/accident_report',methods=['get','post'])
def accident_report():
    data={}
    qry1="select * from accident_report where a_status='pending'"
    data['acci']=select(qry1)
    qry2="select * from accident_report where a_status='approved' or a_status='insurance_approved'"
    data['approved']=select(qry2)
    




    return render_template('accident_report.html',data=data)

@admin.route('/accident_status',methods=['get','post'])
def accident_status():
    data={}
    id=request.args['id']
    # qry2="select * from accident_report where accident_id='%s'"%(id)
    # data['acca']=select(qry2)
    if 'action' in request.args:
        action=request.args['action']
        if action=='update':
            qry3="update accident_report set a_status='approved' where accident_id='%s'"%(id)
            update(qry3)
            return "<script>alert('status updated');window.location.href='accident_report'</script>"
        else:
            qry4="update accident_report set a_status='rejected' where accident_id='%s'"%(id)
            update(qry4)
            return "<script>alert('no data');window.location.href='accident_report'</script>"

    return render_template('accident_report.html',data=data)
    
@admin.route('/insurance_details',methods=['get','post'])
def insurance_details():
    data={}
    qry1="select * from accident_report where a_status='approved'  "
    res1=select(qry1)
    
    data['view']=res1
    qry2="select * from insurance where status='pending' "
    res2=select(qry2)
    
    data['grant']=res2

    qry3="select * from insurance where status='paid' "
    res3=select(qry3)
    
    data['paid']=res3

    
    

    return render_template('insurance_details.html',data=data)

# @admin.route('/granted_insurances',methods=['get','post'])
# def granted_insurances():
#     data={}
#     qry1="select * from accident_report where a_status='insurance_approved' "
#     res1=select(qry1)
    
#     data['grant']=res1
    

#     return render_template('insurance_details.html',data=data)

@admin.route('/grant_insurance',methods=['get','post'])
def grant_insurance():
    data={}
  
   
               
    
    if 'submit' in request.form:
         
                 amount=request.form['amt']
                 policy=request.form['policy']
                 description=request.form['description']
                #  date=request.form['date']           
                 c_id=request.args['c_id']
                 a_id=request.args['a_id']
                 w_name=request.args['w_name']

                 qry1="insert into insurance values(null,'%s','%s',curdate(),'%s','%s','%s','pending')" %(w_name,c_id,amount,policy,description)
                 res2=insert(qry1)
                 data['temp']=res2
                 if res2:
                    qry2="update accident_report set a_status='insurance_approved' where accident_id='%s'"%(a_id)
                    update(qry2)
         
        

         
                 return "<script>alert('Done succesfully');window.location.href='insurance_details'</script>"
  
       

  
    return render_template('insurance_details.html',data=data)

@admin.route('/worker_details',methods=['get','post'])
def worker_details():
    

    return render_template('worker_details.html')

@admin.route('/view_wc',methods=['get','post'])
def view_wc():
    data={}
    qry1="select * from worker order by ward"
    data['workers']=select(qry1)
    qry2="select * from work_card"
    data['card']=select(qry2)

    return render_template('view_wc.html',data=data)

@admin.route('/request_add',methods=['get','post'])
def request_add():
    data={}
    qry1="select * from member_request where status='pending' and reg_type='new' "
    data['req']=select(qry1)
    qry3="select * from member_request where status='approved' and reg_type='new' "
    data['approved']=select(qry3)
    

    return render_template('member_request.html',data=data)

@admin.route('/member_approval',methods=['get','post'])
def member_approval():
        data={}
        id=request.args['req_id']
        card_no=request.args['card_no']
       
    
        qry1="select * from member_request where request_id='%s' and reg_type='new'"%(id)
        data['app']=select(qry1)
       
        qry2="select card_no,ration_no,ration_image  from work_card where card_no='%s'"%(card_no)
        res=select(qry2)
        
        if res:
            data['app1']=res
        else:
             qry7="update member_request set status='rejected' where request_id='%s'"%(id)
             update(qry7)
             return "<script>alert('Card Doesnt Exist');window.location.href='request_add'</script>"

            

        
        
        if 'submit' in request.form:
            status=request.form['approval']

            card_no=data['app'][0]['card_no']
            status=data['app'][0]['status']
            first_name=data['app'][0]['first_name']
            last_name=data['app'][0]['last_name']
            dob=data['app'][0]['dob']
            gender=data['app'][0]['gender']
            phone=data['app'][0]['phone']
            email=data['app'][0]['email']
           
            house=data['app'][0]['house']
            post=data['app'][0]['post']
            district=data['app'][0]['district']
           
            panchayat=data['app'][0]['panchayat']
            ward=data['app'][0]['ward']
            village=data['app'][0]['village']
            aadhaar=data['app'][0]['aadhaar']
            ration_number=data['app'][0]['ration_no']
            
           
            username=data['app'][0]['username']
            password=data['app'][0]['password']
            
            if status!='approved': 
                    qry4="insert into login values(null,'%s','%s','worker')"%(username,password)
                    login=insert(qry4)        
                    qry3="insert into worker values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(card_no,first_name,last_name,dob,gender,phone,email,house,post,district,panchayat,ward,village,aadhaar,ration_number,login)
                    worker=insert(qry3)
                    qry10="select * from work_card where card_no='%s'"%(card_no)
                    existing=select(qry10)
                    if existing:
                        print("already existing")
                    else:
                         qry11="insert into work_card values(null,'%s','%s','%s','0',CURDATE(),'%s','pending')"%(worker,ward,card_no,ration_number)
                         insert(qry11)
                    
                    
            qry5="update member_request set status='approved' where request_id='%s'"%(id)
            res1=update(qry5)
                    
                  
            return "<script>alert('Done succesfully');window.location.href='request_add'</script>"

                
    

        return render_template('worker_approval.html',data=data)

@admin.route('/mate_details',methods=['get','post'])
def mate_details():
    data={}
    qry1="select * from mate where user_type='mate' order by ward"
    data['mate']=select(qry1)
    if 'action' in request.args:
        action=request.args['action']
        officer_id=request.args['mate_id']
        if action=='delete':
            qry3="delete from mate where officer_id='%s'"%(officer_id)
            delete(qry3)
            return "<script>alert('deleted successfully');window.location.href='mate_details'</script>"
      
    return render_template('mate_details.html',data=data)

@admin.route('/overseer_details',methods=['get','post'])
def overseer_details():
    data={}
    qry1="select * from mate where user_type='overseer'"
    data['overseer']=select(qry1)
    if 'action' in request.args:
        action=request.args['action']
        officer_id=request.args['overseer_id']
        if action=='delete':
            qry3="delete from mate where officer_id='%s'"%(officer_id)
            delete(qry3)
           
            return "<script>alert('deleted successfully');window.location.href='overseer_details'</script>"
       

    return render_template('overseer_details.html',data=data)
    

@admin.route('/work_wage_estimation' ,methods=['get','post'])
def work_wage_estimation():
    data={}
    qry1="select * from work where progress!=100 and status='approved'"
    data['pending']=select(qry1)
   
       

    return render_template('work_wage_estimation.html',data=data)

@admin.route('/mustroll' ,methods=['get','post'])
def mustroll():
    data={}
    id=request.args['id']
    qry1="select count(distinct(date)) from work_report where work_id='%s' and must_status='pending'"%(id)
    count= select(qry1)
    if count:
        days=int(count[0]['count(distinct(date))'])
        if days==6:
            qry2="select * from work_report where work_id='%s' and must_status='pending' order by date"%(id)
            RES1=select(qry2)
            if RES1:
                data['must']=RES1
            if 'approve' in request.form:
                qry3="update work_report set must_status='approved',w_status='w_pending' where work_id='%s' "%(id)
                
                res4=update(qry3)
                if res4:
                     
                    qry10="select  count(report_id) from work_report where work_id='%s' and status='50' and  must_status='approved' and w_status='w_pending'"%(id)
                    count=select(qry10)
                    if count:
                        half_day=int(count[0]['count(report_id)'])
                        total_wage_half=half_day*173
                    qry11="select  count(report_id) from work_report where work_id='%s' and status='100'  and  must_status='approved'  and w_status='w_pending'"%(id)
                    count2=select(qry11)
                    if count2:
                        full_day=int( count2[0]['count(report_id)'])
                        total_wage_full=full_day*346
                    qry12="select  count(report_id) from work_report where work_id='%s'  and  must_status='approved' and w_status='w_pending'"%(id)
                    count5=select(qry12)
                    if count5:
                        bonus_no=int( count5[0]['count(report_id)'])
                        bonus=bonus_no*346
                        total_amount=int(total_wage_half)+int(total_wage_full)+int(bonus)
                        print(int(total_amount))
                        if total_amount:
                            qry14="insert into wage values(null,'%s','%s','pending',curdate(),'approved')"%(id,total_amount)
                            insert(qry14)
                            qry15="update work_report set w_status='w_granted' where work_id='%s' and w_status='w_pending'"%(id)
                            update(qry15)
                            return "<script>alert('mustroll wage bill approved');window.location.href='work_wage_estimation'</script>"
        
             

        elif days<=7:
             qry5="select * from work_report where work_id='%s' and must_status='pending' order by date"%(id) 
             res5=select(qry5)
             if res5:
                data['pending']=res5
       
            
        
        elif days>=7:
             qry4="select * from work_report where work_id='%s' and must_status='pending' order by date"%(id)
             res7=select(qry4)
             if res7:
                data['missed']=res7
      
           
    
    qry6="select * from work_report where work_id='%s' and must_status='approved'  and w_status='w_granted' order by date"%(id) 
    res10=select(qry6)
    if res10:
        data['completed']=res10

    return render_template('mustroll.html',data=data)


@admin.route('/worker_details_accident' ,methods=['get','post'])
def worker_details_accident():
    data={}
    id=request.args['worker_id']
    qry1="select * from work_card where card_no='%s' "%(id)
    data['worker']=select(qry1)
   
       

    return render_template('accident_report.html',data=data)

@admin.route('/admin_logout',methods=['get','post'])
def admin_logout():
    
    if 'confirm' in request.form:
        return redirect(url_for('public.home'))
            
            
    elif 'cancel' in request.form:
         return redirect(url_for('admin.admin_home'))             
         
    
   
       
    return render_template('logout.html')



@admin.route('/registration_approval',methods=['get','post'])
def registration_approval():
    data={}
    qry1="select * from member_request where status='pending' and reg_type='registration'"
    data['approval']=select(qry1)
    if 'action' in request.args:
        action=request.args['action']
        if action=='update':
            id=request.args['id']
            qry2="select * from member_request where request_id='%s'"%(id)
            data['approved']=select(qry2)
            card_no=data['approved'][0]['card_no']
           
            first_name=data['approved'][0]['first_name']
            last_name=data['approved'][0]['last_name']
            dob=data['approved'][0]['dob']
            gender=data['approved'][0]['gender']
            phone=data['approved'][0]['phone']
            email=data['approved'][0]['email']
           
            house=data['approved'][0]['house']
            post=data['approved'][0]['post']
            district=data['approved'][0]['district']
           
            panchayat=data['approved'][0]['panchayat']
            ward=data['approved'][0]['ward']
            village=data['approved'][0]['village']
            aadhaar=data['approved'][0]['aadhaar']
            ration_number=data['approved'][0]['ration_no']
            
          
            username=data['approved'][0]['username']
            password=data['approved'][0]['password']
            qry4="insert into login values(null,'%s','%s','worker')"%(username,password)
            login=insert(qry4)        
            qry3="insert into worker values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(login,card_no,first_name,last_name,dob,gender,phone,email,house,post,district,panchayat,ward,village,aadhaar,ration_number)
            worker_id=insert(qry3)
            qry10="select * from work_card where card_no='%s'"%(card_no)
            existing=select(qry10)
            if existing:
                        print("already existing")
            else:
                        qry11="insert into work_card values(null,'%s','%s','%s','0',CURDATE(),'%s','pending')"%(worker_id,ward,card_no,ration_number)
                        insert(qry11)
                    
                    
            
                    
                    
            qry5="update member_request set status='approved' where request_id='%s'"%(id)
            res1=update(qry5)
            if res1:
                 return "<script>alert('Registration Approved');window.location.href='work_wage_estimation'</script>"





    return render_template('worker_approval.html',data=data)







