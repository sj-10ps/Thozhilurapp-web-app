import uuid
from flask import *
from database import *


overseer=Blueprint('overseer',__name__)

@overseer.route('/overseer_home')
def overseer_home():
     return render_template('overseerhome.html')

@overseer.route('/geotag', methods=["get","post"])
def geotag():
     if 'submit' in request.form:
          ward=request.form['ward']
          description=request.form['des']
          lat=request.form['lat']
          image=request.files['img']

          path='static/assets/images/geotag'+str(uuid.uuid4())+image.filename
          image.save(path)


          lon=request.form['lon']
          qry1="insert into work values(null,'pending','%s','%s','%s','%s','%s','pending','pending','pending','pending','pending','pending')"%(ward,description,lat,path,lon)
          insert(qry1)
          return "<script>alert('uploaded successfully');window.location.href='geotag'</script>"

     return render_template('geotag.html')

@overseer.route('/approved_works', methods=['get','post'])
def approved_works():
     data={}
     qry1="select * from work where status='approved' and mate_id='pending'"
     data['works']=select(qry1)
     qry2="select * from work where status='approved' and mate_id!='pending'"
     data['all']=select(qry2)

  

     return render_template('approved_works.html',data=data)

@overseer.route('/assign_mate', methods=['get','post'])
def assign_mate():
     data={}
     ward=request.args['ward']
     work_id=request.args['work_id']
     
     qry1="select * from mate where ward='%s' and w_status='free'"%(ward)
     data['free']=select(qry1)
     qry2="select * from work where work_id='%s'"%(work_id)
     res1=select(qry2)
     data['try']=res1


     return render_template('assign_mate.html',data=data)

@overseer.route('/assign_to_mate', methods=['get','post'])
def assign_to_mate():
      data={}
      mate_id=request.args['mate_id']
      qry3="select * from mate where officer_id='%s'"%(mate_id)
      data['temp']=select(qry3)
      
  
      if 'action' in request.args:
          action=request.args['action']
          work_id=request.args['work_id']
          if action=='update':
              
             
              
              if 'assign' in request.form:
                   qry2="update mate set w_status='assigned',as_date=curdate() where officer_id='%s'"%(mate_id)
                   res1=update(qry2)
                   qry5="update work set mate_id='%s' where work_id='%s' "%(mate_id,work_id)

                   update(qry5)
                  
                   
                   
                   return "<script>alert('work assigned successfully');window.location.href='approved_works'</script>"

     
      return render_template('assign_mate.html',data=data)

@overseer.route('/overseer_comworks', methods=['get','post'])
def overseer_comworks():
     data={}
     qry1="select * from work where progress='100'"
     data['com_works']=select(qry1)
     if 'action' in request.args:
          id=request.args['id']
          action=request.args['action']
          if action=='update':
          #     qry2="select * from wage where work_id='%s'"%(id)
          #     data['wage']=select(qry2)
              qry4="select * from wage where work_id='%s'"%(id)
              data['wage']=select(qry4)

     return render_template('overseer_comworks.html',data=data)

@overseer.route('/overseer_wage', methods=['get','post'])
def overseer_wage():
     data={}
     
    
     id=request.args['id']  
     qry4="select * from wage where work_id='%s'"%(id)
     data['wage']=select(qry4)
     if 'submit' in request.form:
          response=request.form['response']
          qry2="update wage set response='%s' where work_id='%s'"%(response,id)
          update(qry2)
          return "<script>alert('replied successfully');window.location.href='overseer_comworks'</script>"
          

     return render_template('overseer_comworks.html',data=data)


@overseer.route('/overseer_ow_details',methods=['get','post'])
def overseer_ow_details():
    data={}
    qry5="select * from work where status='approved' and progress!='100'"
    data['works']=select(qry5)

    print(data,"++++++++++++++")
    if 'action' in request.args:
          
          action=request.args['action']
          if action=='view':
               id=request.args['id']
               qry1="select * from mate_feedback where work_id='%s'"%(id)

               data['all']=select(qry1)

               
               


#     qry1="select * from mate_feedback where reply='pending'"%(id)
#     data['all']=select(qry1)
#     id=request.args['id']
#     qry2="select * from mate_feedback where work_id='%s'"%(id)
#     data['owd']=select(qry2)
    return render_template('overseer_ow_details.html',data=data)

@overseer.route('/overseer_reply_response', methods=['get','post'])
def overseer_reply_response():
     data={}
     id=request.args['id']
     qry1="select * from mate_feedback where feedback_id='%s'"%(id)
     data['rply']=select(qry1)
     if 'submit' in request.form:
          reply=request.form['rply']
          qry3="update mate_feedback set reply='%s' where feedback_id='%s'"%(reply,id)
          update(qry3)
          return "<script>alert('replied successfully');window.location.href='overseer_ow_details'</script>"
          

     return render_template('overseer_ow_details.html',data=data)


@overseer.route('/overseer_work_report', methods=['get','post'])
def overseer_work_report():
     data={}
     qry1="select * from work where progress!='100'"
     data['ongoing']=select(qry1)

     qry2="select * from work where progress='100'"
    
     data['completed']=select(qry2)

          

     return render_template('overseer_work_report.html',data=data)


@overseer.route('/overseer_attendance_report', methods=['get','post'])
def overseer_attendance_report():
     data={}
     id=request.args['id']
     qry1="select * from work_report where work_id='%s'"%(id)

     data['report']=select(qry1)


          

     return render_template('overseer_work_report.html',data=data)

@overseer.route('/overseer_wreport', methods=['get','post'])
def overseer_wreport():
     data={}
     id=request.args['id']
     qry1="select * from work_report where work_id='%s'"%(id)

     data['com']=select(qry1)


          

     return render_template('overseer_comworks.html',data=data)




@overseer.route('/mustroll_works' ,methods=['get','post'])
def mustroll_works():
    data={}
    qry1="select * from work where progress!=100 and status='approved'"
    data['must_works']=select(qry1)
   
       

    return render_template('overseer_mustroll_works.html',data=data)


@overseer.route('/overseer_mustroll' ,methods=['get','post'])
def overseer_mustroll():
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
    return render_template('overseer_mustroll_details.html',data=data)



@overseer.route('/overseer_logout',methods=['get','post'])
def overseer_logout():
    
    if 'confirm' in request.form:
        return redirect(url_for('public.home'))
            
            
    elif 'cancel' in request.form:
         return redirect(url_for('overseer.overseer_home'))             
         
    
   
       
    return render_template('logout.html')
