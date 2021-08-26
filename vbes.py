import speech_recognition as sr 
from gtts import gTTS
import os
from time import sleep
from playsound import playsound
import smtplib
import imaplib
import email
from bs4 import BeautifulSoup


class VoiceBasedEmail :

    def recognizeSpeech(self):
        print('Speak :')
        reco = sr.Recognizer()
        with sr.Microphone() as source :
            speech = reco.record(source,duration=5)
        try :
            text = reco.recognize_google(speech)
            return text 
        except sr.UnknownValueError :
            return "unable to recognize your speech !"
        except sr.RequestError as re :
            return "can not connect to google speech recognition services."

    def textToSpeech(self,text1):   
        tts = gTTS(text=text1, lang='en')
        ttsname=("name.mp3")
        tts.save(ttsname)
        playsound(ttsname)
        os.remove(ttsname)

    def sendMail(self,choice,body):
        recipients = {1 : 'vtu11305@veltech.edu.in' , 3 : 'vtu13534@veltech.edu.in', 5 : 'vtu14621@veltech.edu.in'} 
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()  
        server.starttls() #security connection
        server.login('forminorproject.veltech@gmail.com','minorproject@2021')
        message = """From: forminorproject.veltech@gmail.com
                     To: {}
                     Subject: E-mail sent from Voice-based Email System

                     {}
                  """.format(recipients[choice],body)
        print(message)
        server.sendmail('forminorproject.veltech@gmail.com',recipients[choice],message)
        print('mail sent successfully')
        server.close()

    def readMail(self):
        contents = []
        mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
        unm = ('forminorproject.veltech@gmail.com')
        psw = ('minorproject@2021')
        mail.login(unm,psw)  #login
        stat, total = mail.select('Inbox')
        result, data = mail.uid('search',None, "ALL")
        
        inbox_item_list = data[0].split()
        new = inbox_item_list[-1]
        old = inbox_item_list[0]
        result2, email_data = mail.uid('fetch', new, '(RFC822)') #fetch
        raw_email = email_data[0][1].decode("utf-8") #decode
        email_message = email.message_from_string(raw_email)
        contents.append(email_message['From'])
        contents.append(email_message['Subject'])
        
        stat, total1 = mail.select('Inbox')
        stat, data1 = mail.fetch(total1[0], "(UID BODY[TEXT])")
        msg = data1[0][1]
        soup = BeautifulSoup(msg, "html.parser")
        elements = soup.find_all("div")
        contents.append(elements[0].get_text())
        return contents
        

mailObj = VoiceBasedEmail()
welcomeText = '''Welcome to Voice Based E-mail System. 
                please select your action :
                1. Read mail
                2. Send mail\n\n
                Speak your choice :'''
mailObj.textToSpeech(welcomeText)
choice = mailObj.recognizeSpeech()
print(choice)
if choice.lower() == 'read' :
    contents = mailObj.readMail()
    print(contents[0])
    print(contents[1])
    print(contents[2])
    mailObj.textToSpeech("from : {}".format(contents[0]))
    sleep(0.5)
    mailObj.textToSpeech("subject : {}".format(contents[1]))
    sleep(0.5)
    mailObj.textToSpeech("body : {}".format(contents[2]))
elif choice.lower() == 'send'  :
    mailObj.textToSpeech('''To whom you want to send mail ?
                                for Aditya, say 1,
                                for Smit, say 3,
                                for Laksh, say 5
                                Speak up your choice !!!''')

    choice = mailObj.recognizeSpeech()                            
    mailObj.textToSpeech('you said {}'.format(choice))
    choices = {'one' : 1 , 'One' : 1 , 'won' : 1 , '1' : 1, '3' : 3 , 'three' : 3 , 'Three' : 3 , 'free' : 3, 'five' : 5 , 'Five' : 5 , '5' : 5}
    if choice in choices :
        mailObj.textToSpeech('what is your mail body ? ')
        body = mailObj.recognizeSpeech()
        mailObj.sendMail(choices[choice],body)
    else :
        mailObj.textToSpeech('Sorry, please re-run the project')
        
else :
    mailObj.textToSpeech('sorry ! did not get you. please re-run the project')



    









