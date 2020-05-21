import msbot
import apiVulcan
import json
import mysql.connector
import threading
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="users"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT COUNT(*) FROM users")

def checkNewGrades():
    ovr_start = time.time()
    for x in range(mycursor.fetchone()[0]):
        y=x+1
        print('Odswiezanie ucznia '+str(y))
        mycursor.execute("SELECT `certificate` FROM `users` WHERE id="+str(y))
        clientCertificate = mycursor.fetchall()
        clientCertificateL = []
        for index in range(len(clientCertificate)):
            clientCertificateL.append(str(clientCertificate[index][0]))
        clientCertificate = clientCertificateL[0]
        clientCertificate = clientCertificate[:-1]
        clientCertificate = clientCertificate[2:]
        clientCertificate = clientCertificate.replace("'",'"')
        clientCertificate = json.loads(clientCertificate)
        mycursor.execute("SELECT `last_gradeID` FROM `users` WHERE id="+str(y))
        sqlLastGrade = mycursor.fetchall()
        sqlLastGradeL = []
        for index in range(len(sqlLastGrade)):
            sqlLastGradeL.append(sqlLastGrade[index][0])
        sqlLastGrade = sqlLastGradeL[0]
        lastGradeL = apiVulcan.getLastGrade(clientCertificate)
        if(lastGradeL[0]==sqlLastGrade):
            print('Ocena taka sama')
        else:
            print("Ocena inna")
            lastGradeV = lastGradeL[1]
            mycursor.execute("SELECT `recipient_id` FROM `users` WHERE id="+str(y))
            recipientG = mycursor.fetchall()
            recipientGL = []
            for index in range(len(recipientG)):
                recipientGL.append(recipientG[index][0])
            recipientG = recipientGL[0]
            print('Wysylanie wiadomosci')
            msbot.sendMessage(recipientG,"Nowa ocena!\n"+str(lastGradeV))
            insert="""UPDATE users SET last_gradeID = %s, last_gradeDATA= %s WHERE recipient_id = %s"""
            mycursor.execute(insert, (lastGradeL[0],lastGradeV,recipientG,))
            mydb.commit()
    ovr_end = time.time()
    print("Calosc trwała "+str(round(ovr_end-ovr_start,3))+"s")

checkNewGrades()
