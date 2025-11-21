from flask import *
from database import *
import os
import cloudinary
import cloudinary.uploader
cloudinary.config(
       cloud_name=os.getenv('cloud_name'),
  api_key=os.getenv('api_key'),
  api_secret=os.getenv('api_secret')
)


api=Blueprint('api',__name__)

@api.route('/worker_reg')
def worker_reg():
    data={}
    # print("123456789")

    c_no=request.args['c_no']
    fname=request.args['fname']
    lname=request.args['lname']
    dob=request.args['dob']
    gender=request.args['gender']
    phone=request.args['phone']
    email=request.args['email']
    house=request.args['house']
    post=request.args['post']
    district=request.args['district']
    panchayat=request.args['panchayat']
    ward=request.args['ward']
    village=request.args['village']
    aadhaar=request.args['aadhaar']
    ration_no=request.args['ration_no']
   
    
    username=request.args['username']
    password=request.args['password']

    # qry2="insert into login values(null,'%s','%s','worker')" %(username,password)
    # login=insert(qry2)

    
    qry1="insert into member_request values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','not_sneeded','%s','%s','%s','pending','registration')" %(c_no,fname,lname,dob,gender,phone,email,house,post,district,panchayat,ward,village,aadhaar,ration_no,username,password)
    worker_id=insert(qry1)
    

    # qry3="insert into work_card values(null,'%s','%s','%s','pending','pending','%s','%s')"%(worker_id,ward,c_no,ration_no,ration_img)
    # res=insert(qry3)


    if worker_id:
        data['status']='success'
    else:
        data['status']='failed'

    return str(data)


@api.route('/android_login')
def android_login():
    data={}
    username=request.args['username']
    password=request.args['password']
    qry="select * from login where username='%s' and password='%s' " %(username,password)
    res1=select(qry)

    mate=""
    wor=""

    if res1:
        lid=res1[0]['login_id']

    if res1[0]['user_type']=='mate':
        v="select * from login inner join mate using(login_id) where login_id='%s'"%(lid)
        mate=select(v)
    
    if res1[0]['user_type']=='worker':
        v="select * from login inner join worker using(login_id) where login_id='%s'"%(lid)
        wor=select(v)

    if mate:
        data['status']='success'
      
        data['data']=mate
    elif wor:
        data['status']='success'
      
        data['data']=wor
    else:
        data['status']='fail'

    return str(data)




@api.route('/view_mate_profile')
def view_mate_profile():
    data={}
    login_id=request.args['loginid']
  
    qry="select * from mate where login_id='%s'" %(login_id)
    res=select(qry)


    if res:
        data['status']='success'
        data['data']=res
       
    else:
        data['data']='failed'
    data['method']='view'
   

    return str(data)



@api.route('/edit_mate')
def edit_mate():
    data={}
    login_id=request.args['login_id']
    fname=request.args['fname']
    lname=request.args['lname']
    dob=request.args['dob']
    gender=request.args['gender']
    phone=request.args['phone']
    email=request.args['email']
    house=request.args['house']
    post=request.args['post']
    district=request.args['district']
    panchayat=request.args['panchayat']
    ward=request.args['ward']



  
    qry="update mate set first_name='%s',last_name='%s',dob='%s',gender='%s',phone='%s',email='%s',house='%s',post='%s',district='%s',panchayat='%s',ward='%s' where login_id='%s'" %(fname,lname,dob,gender,phone,email,house,post,district,panchayat,ward,login_id)
    res=update(qry)


    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'

    return str(data)





@api.route('/manage_workers')
def manage_workers():
    data={}
    ward=request.args['ward']
    print('no card no')
   
  
    qry="select * from work_card where ward='%s'" %(ward)
    res=select(qry)


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)








@api.route('/job_requests')
def job_requests():
    data={}
    ward=request.args['ward']

  
    qry="select * from job_request where ward='%s' and status='pending' order by date" %(ward)
    res=select(qry)
  



    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)



@api.route('/assigned_duties')
def assigned_duties():
    data={}
    mate_id=request.args['mate_id']

   
    qry="select * from work where mate_id='%s' and progress!='100'" %(mate_id)
    res=select(qry)
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)



@api.route('/mate_previous_works')
def mate_previous_works():
    data={}
    mate_id=request.args['mate_id']
 
   
    qry="select * from work where mate_id='%s' and progress='100'" %(mate_id)
    res=select(qry)
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)

@api.route('/work_requirements')
def work_requirements():
    data={}
    mate_id=request.args['mate_id']

   
    qry="select * from work where mate_id='%s' and progress!='100'" %(mate_id)
    res=select(qry)
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)


@api.route('/view_complaints')
def view_complaints():
    data={}
    mate_id=request.args['mate_id']

   

    qry="select * from mate_complaint where mate_id='%s' " %(mate_id)
    res=select(qry)
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)

@api.route('/details_of_workers')
def details_of_workers():
    data={}
    card=request.args['card_no']
   
 

   

    qry="select * from worker where card_no='%s' " %(card)
    res=select(qry)
    
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
    data['method']='view'
    

    return str(data)





@api.route('/uploaded_requirements')
def uploaded_requirements():
    data={}
    work_id=request.args['work_id']
   
 

   

    qry="select * from mate_feedback where work_id='%s' " %(work_id)
    res=select(qry)
    
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
        data['data']='empty'
    data['method']='view'
    

    return str(data)


@api.route('/update_requirements')
def update_requirements():
    data={}
    shelter=request.args['shelter']
    tools=request.args['tool']
    babies=request.args['babies']
    des=request.args['des']
    f_id=request.args['f_id']
  
 
   
    mate=request.args['mate']
   
    work_id=request.args['work_id']
        
   
 

   
    if f_id=='null':
         
      
    
        qry1="insert into mate_feedback values(null,'%s','%s','%s','%s','%s','%s',curdate(),'pending')"%(work_id,mate,shelter,tools,babies,des)
        res=insert(qry1)
        
      
    elif f_id:
        
         qry="update mate_feedback set shelter='%s',tools='%s',babies='%s',description='%s',date=curdate() where feedback_id='%s' " %(shelter,tools,babies,des,f_id)
         res=update(qry)
  


    if res:
        data['status']='success'
        data['data']=res
   
    else:
        data['status']='failed'
        data['data']='empty'
    data['method']='view'
    

    return str(data)




@api.route('/approve_job')
def approve_job():
    data={}
    
    jr_id=request.args['jr_id']
    qry="update job_request set status='assigned' where jr_id='%s' "%(jr_id)
    res=update(qry)
    if res:
        work_id=request.args['work_id']
        card_no=request.args['card_no']
        qry1="insert into assign_workers values(null,'%s','%s',curdate(),'pending')"%(work_id,card_no)
        res2=insert(qry1)

        if res2:
           data['status']='done'
          
   
        else:
           data['status']='failed'
        
    data['method']='view'
    

    return str(data)


@api.route('/morning_attendance')
def morning_attendance():
    data={}
    
    work_id=request.args['work_id']
    print(work_id,"?????????????????????????")
    qry2="select * from assign_workers where work_id='%s'"%(work_id)
    res=select(qry2)
   
    
    if res:
           data['status']='success'
           data['morning']=res
          
   
    else:
           data['status']='failed'
           data['morning']='empty'
    data['method']='view'
    

    return str(data)

@api.route('/present')
def present():
    data={}
    
    aw_id=request.args['aw_id']
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry6="select * from assign_workers where date!=curdate() and aw_id='%s' "%(aw_id)
    temp=select(qry6)
    print(temp)

    if temp:

                qry1="insert into work_report values(null,'%s','%s','present','pending',null,curdate(),'pending','pending','pending')"%(work_id,card_no)
                res=insert(qry1)
                if res:
                    qry2="update assign_workers set date=curdate() where aw_id='%s'"%(aw_id)
                    update(qry2)
    else:
        qry7="update work_report set m_attendance='present' where card_no='%s' and date=curdate()  and work_id='%s'"%(card_no,work_id)
        res=update(qry7)


    if res:
           data['status']='p'
           qry1="update work_card set work_days=work_days+1 where card_no='%s'"%(card_no)
           update(qry1)
  
    data['method']='view'
    

    return str(data)

@api.route('/absent')
def absent():
    data={}
    
    aw_id=request.args['aw_id']
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry6="select * from assign_workers where date!=curdate() and aw_id='%s' "%(aw_id)
    temp=select(qry6)
    print(temp)

    if temp:

                qry1="insert into work_report values(null,'%s','%s','absent','pending',null,curdate(),'pending','pending','pending')"%(work_id,card_no)
                res=insert(qry1)
                if res:
                    qry2="update assign_workers set date=curdate() where aw_id='%s'"%(aw_id)
                    update(qry2)
    else:
        qry7="update work_report set m_attendance='absent' where card_no='%s' and date=curdate()  and work_id='%s'"%(card_no,work_id)
        res=update(qry7)


    if res:
           data['status']='p'
          
           

         
    data['method']='view'
    

    return str(data)


@api.route('/evening_attendance')
def evening_attendance():
    data={}
    
    work_id=request.args['work_id']
  
    qry2="select * from assign_workers where work_id='%s'  "%(work_id)
    res=select(qry2)
   
    
    if res:
           data['status']='success'
           data['morning']=res
           
           
          
   
    else:
           data['status']='failed'
           data['morning']='empty'
    data['method']='view'

    

    return str(data)


@api.route('/a_present')
def a_present():
    data={}
    
    aw_id=request.args['aw_id']
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry1="update work_report set a_attendance='present' where card_no='%s' and date=curdate() and work_id='%s' "%(card_no,work_id)
  
    res=update(qry1)


          

    if res:
           data['status']='p'
           qry5="select * from assign_workers where work_id='%s' and card_no='%s' date=curdate() "%(work_id,card_no)
           temp=select(qry5)
           att=temp[0]['m_attendance']
           if att=='absent':
               qry10="update work_card set work_days=work_days+1 where card_no='%s'"%(card_no)
               update(qry10)
             
    data['method']='view'
    

    return str(data)

@api.route('/a_absent')
def a_absent():
    data={}
    
    aw_id=request.args['aw_id']
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry1="update work_report set a_attendance='absent' where card_no='%s' and date=curdate() and work_id='%s' "%(card_no,work_id)
  
    res=update(qry1)


    if res:
           data['status']='p'
             
    data['method']='view'
    

    return str(data)



@api.route('/work_status')
def work_status():
    data={}
    
    work_id=request.args['work_id']
  
    qry2="select * from assign_workers where work_id='%s' and date=curdate() "%(work_id)
    res=select(qry2)
   
    
    if res:
           data['status']='success'
           data['morning']=res
           print(data['morning'])
          
   
    else:
           data['status']='failed'
         
    data['method']='view'
    

    return str(data)


@api.route('/full_status')
def full_status():
    data={}
   
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry1="update work_report set status='100' where card_no='%s' and date=curdate() and work_id='%s' "%(card_no,work_id)
  
    res=update(qry1)
   



          

    if res:
           data['status']='p'
             
    data['method']='view'
    

    return str(data)

@api.route('/half_status')
def half_status():
    data={}
   
    card_no=request.args['card_no']
    work_id=request.args['work_id']
   
    qry1="update work_report set status='50' where card_no='%s' and date=curdate() and work_id='%s' "%(card_no,work_id)
    
    res=update(qry1)


          

    if res:
           data['status']='p'
             
    data['method']='view'
       
    return str(data)



@api.route('/attendance_reported')
def attendance_reported():
    data={}
   

    work_id=request.args['work_id']
   
    qry1="select * from work_report where work_id='%s' "%(work_id)
  
    res=select(qry1)


          

    if res:
           data['status']='success'
           data['data']=res
    else:
        data['status']='failed'
             
    data['method']='view'
       
    return str(data)
    

@api.route('/mate_attendancehistory')
def mate_attendancehistory():
    data={}
   

    work_id=request.args['work_id']
   
    qry1="select * from work_report where work_id='%s' "%(work_id)
  
    res=select(qry1)


          

    if res:
           data['status']='success'
           data['data']=res
    else:
        data['status']='failed'
             
    data['method']='view'
       
    return str(data)
    

@api.route('/accident_reporting')
def accident_reporting():
    data={}
   

    work_id=request.args['work_id']
    card_no=request.args['card_no']
    report=request.args['report']
    name=request.args['name']
   
    qry1="insert into accident_report values(null,'%s','%s','%s','%s',curdate(),'pending')"%(work_id,name,card_no,report)
  
    res=insert(qry1)


          

    if res:
           data['status']='success'
           
    else:
        data['status']='failed'
             
   
       
    return str(data)


@api.route('/reported_accidents')
def reported_accidents():
    data={}
   

    work_id=request.args['work_id']

   
    qry1="select * from accident_report where work_id='%s'"%(work_id)
  
    res=select(qry1)


          

    if res:
           data['status']='success'
           data['data']=res
           
    else:
        data['status']='failed'
             
    data['method']='view'
       
    return str(data)



@api.route('/mate_reply_complaint')
def mate_reply_complaint():
    data={}
   

    complaint_id=request.args['complaint_id']
    reply=request.args['reply']

   
    qry1="update mate_complaint set mate_response='%s' where complaint_id='%s'"%(reply,complaint_id)
    res=update(qry1)


          

    if res:
           data['status']='success'
          
           
    else:
        data['status']='failed'
 
    return str(data)
    



@api.route('/view_workcard')
def view_workcard():
    data={}
    card_no=request.args['card_no']
  
    qry="select * from work_card where card_no='%s'" %(card_no)
    res=select(qry)


    if res:
        data['status']='success'
        data['data']=res
       
    else:
        data['data']='failed'
    data['method']='view'
   

    return str(data)

@api.route('/view_cardworkers')
def view_cardworkers():
    data={}
    card_no=request.args['card_no']
  
    qry="select * from worker where card_no='%s'" %(card_no)
    res=select(qry)


    if res:
        data['status']='success'
        data['data']=res
       
    else:
        data['data']='failed'
    data['method']='view'
   

    return str(data)

@api.route('/request_job')
def request_job():
    data={}
    card_no=request.args['card_no']
    ward=request.args['ward']
    des=request.args['des']
  
    qry="select status from job_request where card_no='%s' and status='pending'" %(card_no)
    temp=select(qry)
    if not temp:
         qry1="insert into job_request values(null,'%s','%s','%s','pending',curdate()) "%(ward,card_no,des)
         res=insert(qry1)
    else:
         data['data']='failed'

    if res:
        data['status']='success'
        data['data']=res
       
    else:
        data['data']='failed'
    data['method']='view'
   

    return str(data)


@api.route('/worker_attendance')
def worker_attendance():
    data={}
    card_no=request.args['card_no']
    print(card_no,"??????????????????????????????")
   
  
    qry="select work_report.m_attendance,work_report.a_attendance,work_report.date,work_report.status,work.description,work.image from work_report inner join work using(work_id) where card_no='%s'" %(card_no)
    res=select(qry)
   

    if res:
        data['status']='success'
        data['data']=res
       
    else:
        data['data']='failed'
    data['method']='view'
   

    return str(data)

@api.route('/update_progress')
def update_progress():
    data={}
    image=request.args['image']
    progress=request.args['progress']
    work_id=request.args['work_id']
   
   
  
    qry="update work set progress='%s',image_proof='%s' where work_id='%s' " %(progress,image,work_id)
    res=update(qry)
    if progress=='100':
         qry2="update assign_workers set status='work_completed' where work_id='%s'"%(work_id)
         update(qry2)
   

    if res:
        data['status']='success'
        
       
    else:
        data['data']='failed'
 
   

    return str(data)



@api.route('/worker_assignedduties')
def worker_assignedduties():
    data={}
    card_no=request.args['card_no']
  
   
  
    qry="select * from assign_workers where card_no='%s' and status='pending'"%(card_no)
    temp=select(qry)
    if temp:
         session['work']=temp[0]['work_id']
         p=temp[0]['work_id']
       
         qry1="select * from work where work_id='%s' "%(p)
         res=select(qry1)

    
   

    if res:
        data['status']='success'
        data['data']=res
        
       
    else:
        data['data']='failed'
    data['method']='view'
 
   

    return str(data)


@api.route('/worker_mustroll')
def worker_mustroll():
    data={}
    card_no=request.args['card_no']
    work_id=request.args['work_id']
  
   
  
    qry="select * from work_report where card_no='%s' and work_id='%s'"%(card_no,work_id)
    res=select(qry)
   
    
   

    if res:
        data['status']='success'
        data['data']=res
        
       
    else:
        data['data']='failed'
    data['method']='view'
 
   

    return str(data)


@api.route('/worker_sendcomplaint')
def worker_sendcomplaint():
    data={}
    sender_id=request.args['sender_id']
    mate_id=request.args['mate_id']
    complaint=request.args['complaint']
  
   
  
    qry="insert into mate_complaint values(null,'%s','%s','%s',curdate(),'pending','pending','pending','pending','pending','pending')"%(sender_id,mate_id,complaint)
    res=insert(qry)
   

    if res:
        data['status']='success'
        data['data']=res
        
       
    else:
        data['data']='failed'
    data['method']='view'
 
   

    return str(data)



@api.route('/worker_viewcomplaint')
def worker_viewcomplaint():
    data={}
    sender_id=request.args['sender_id']
   
   
  
    qry="select * from mate_complaint where sender_id='%s'"%(sender_id)
    res=select(qry)

    if res:
        data['status']='success'
        data['data']=res
        
       
    else:
        data['data']='failed'
    data['method']='view'
 
   

    return str(data)

@api.route('/worker_wage')
def worker_wage():
    data={}
    card_no=request.args['card_no']
    qry="select * from assign_workers where card_no='%s' and status='pending'"%(card_no)
    temp=select(qry)
    if temp:
        
        p=temp[0]['work_id']
        print(p,"&&&&&&&&&&&&&&&&")
   
        qry1="select * from wage inner join work using(work_id) where work_id='%s' and wage.status='paid'"%(p)
        res=select(qry1)
    if res:
        data['status']='success'
        data['data']=res      
    else:
        data['data']='failed'
    data['method']='view'
    return str(data)


@api.route('/worker_insurance')
def worker_insurance():
    data={}
    card_no=request.args['card_no']
    qry="select * from insurance where card_no='%s' and status='granted'"%(card_no)
    res=select(qry)
   
    if res:
        data['status']='success'
        data['data']=res      
    else:
        data['data']='failed'
    data['method']='view'
    return str(data)



@api.route('/edit_wc')
def edit_wc():
    data={}
    bank=request.args['bank']
    card=request.args['card']
  



  
    qry="update work_card set bank_no='%s'  where card_no='%s'" %(bank,card)
    res=update(qry)


    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'

    return str(data)

@api.route('/newmember_req')
def newmember_req():
    data={}
    # print("123456789")

    c_no=request.args['c_no']
    fname=request.args['fname']
    lname=request.args['lname']
    dob=request.args['dob']
    gender=request.args['gender']
    phone=request.args['phone']
    email=request.args['email']
    house=request.args['house']
    post=request.args['post']
    district=request.args['district']
    panchayat=request.args['panchayat']
    ward=request.args['ward']
    village=request.args['village']
    aadhaar=request.args['aadhaar']
    ration_no=request.args['ration_no']
   
    
    username=request.args['username']
    password=request.args['password']

    # qry2="insert into login values(null,'%s','%s','worker')" %(username,password)
    # login=insert(qry2)

    
    qry1="insert into member_request values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','not_sneeded','%s','%s','%s','pending','registration')" %(c_no,fname,lname,dob,gender,phone,email,house,post,district,panchayat,ward,village,aadhaar,ration_no,username,password)
    worker_id=insert(qry1)
    

    # qry3="insert into work_card values(null,'%s','%s','%s','pending','pending','%s','%s')"%(worker_id,ward,c_no,ration_no,ration_img)
    # res=insert(qry3)


    if worker_id:
        data['status']='success'
    else:
        data['status']='failed'

    return str(data)