
import datetime
import face_recognition
import os
from datetime import datetime
import cv2
import numpy as np 
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt 
from matplotlib import *
from matplotlib.figure import Figure
import mysql.connector
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import sqlite3
import record_display

path = 'images'
images = []
personName = []
mylist = os.listdir(path)
date_now=datetime.now()
today = date_now.date()


for cu_img in mylist:
    current_img=cv2.imread(f'{path}/{cu_img}')  #all images are stored here
    images.append(current_img)
    personName.append(os.path.splitext(cu_img)[0])
print(personName)

def faceEncodings(images):   #uses HOG transformation for encoding
        encodeList=[]  #create encoding for every face
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList    
encodeListKnown=(faceEncodings(images))
print("All encodings are complete..")



def take_attendence():
    global name
    cap = cv2.VideoCapture(0)   #default camera is 0 if external its 1
    while True:
        ret,frame=cap.read()
        faces = cv2.resize(frame,(0,0),None,0.25,0.25)
        faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
        #find faces in current frame...
        # and ecode the found faces in frame....
        facescurrentFrame = face_recognition.face_locations(faces)
        encodescurrentFrames =  face_recognition.face_encodings(faces,facescurrentFrame)
        
        
                    
        for encodeFace , faceloc in zip(encodescurrentFrames,facescurrentFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            facedis=face_recognition.face_distance(encodeListKnown,encodeFace)
            #if distance between faces is less then the face matches...
            #we find the min distance
            matchindex=np.argmin(facedis)#return the min index...
            if matches[matchindex]:
                name = personName[matchindex].upper()
                #print(name)
                #build a rectange around face..
                y1,x2,y2,x1=faceloc
                y1,x2,y2,x1 = 4*y1,4*x2,4*y2,4*x1
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                attendence(name)
                record_display.display_attendence(name)
        cv2.imshow("camera",frame)
        if cv2.waitKey(1)== 13:
            break
        
        
    cap.release()
    cv2.destroyAllWindows() 
        

def attendence(name):
    #These can be used when we use csv to store attendence...
    # with open('attendence.csv','r+') as f:
    #     mydatalist=f.readlines()
    #     namelist = []
    #     for line in mydatalist:
    #         entry = line.split(',')
    #         namelist.append(entry[0])

    #     if name not in namelist:
    #         time_now = datetime.now()
    #         tstr= time_now.strftime('%H:%M:%S')
    #         dstr= time_now.strftime('%d/%m/%Y')
    #         f.writelines(f'{name},{tstr},{dstr}')
    #         f.writelines(f'\n')
    #auth_plugin is must and should...
    
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vvit",
    auth_plugin='mysql_native_password')
    mycursor = db.cursor()
    sql=f"insert ignore into vvit.attendence values (1,'20bq1a05e7','{name}');" 
    mycursor.execute(sql)
    db.commit()
    

   

        

def show_attendence():
    return
def setting():
    return 
def graph():
    fig1 = Figure(figsize = (4, 4),dpi = 50)
    x=np.array([2,5,8,12,3,4,1])
    plot1 = fig1.add_subplot(111)
    plot1.plot(x)
    # fig2=Figure(figsize=(4,4),dpi=50)
    # y=np.array([1,2,3,4,5,6,7])
    # plot2 = fig2.add_subplot(112)
    # plot2.bar(y)
    # adding graph1 to canvas...
    canvas = FigureCanvasTkAgg(fig1,master = root)                   
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=1,padx=10)
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
    canvas.get_tk_widget().grid(row=1,column=1,padx=10)
    #adding graph2 to canvas...
    #canvas = FigureCanvasTkAgg(fig2,master = root)                   
    #canvas.draw()
    #canvas.get_tk_widget().grid(row=2,column=1,padx=10)
    #toolbar = NavigationToolbar2Tk(canvas,root)
    #toolbar.update()
    #canvas.get_tk_widget().grid(row=2,column=1,padx=10)


#creating GUI...

root = Tk()
root.title("Attendence System")
root.geometry('1530x790+0+0')

clg_name= Label(root,text="VVIT",font = ('courier', 15, 'bold'))
clg_name.grid(row=0,column=0,pady=10)


#functions for placeholders...

def click(*args):
    search.delete(0,'end')
def leave(*args):
    search.delete(0,'end')
    search.insert(0,'search for student')
    root.focus()
search = ttk.Entry(root,font = ('courier', 13, 'bold'))
search.insert(0,"search for student")
search.bind("<Button-1>",click)
search.bind("<Leave>",leave)
search.grid(row=0,column=1,pady=10)

frame_left = Frame(root)
frame_left.grid(row=1,column=0)

attendence_but = Button(frame_left,text="Take Attendence",command=take_attendence,font = ('courier', 15, 'bold'),height=1,width=15)
attendence_but.pack(padx=13,pady=10)

db = Button(frame_left,text="DataBase",command=show_attendence,font = ('courier', 15, 'bold'),height=1,width=15)
db.pack(padx=13,pady=10)

s = Button(frame_left,text="summary" ,command=graph,font = ('courier', 15, 'bold'),height=1,width=15)
s.pack(padx=13,pady=10)

#creating mysql connection to store attendence...
#canvas = Canvas(root)
#canvas.create_line(15,20,15,300)
#canvas.grid(row=1,column=1)
#graph1 = Text(root,height=12,width=30)
#graph1.grid(row=1,column=1)


root.mainloop()



