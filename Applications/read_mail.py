import imaplib as imap
import email as imap_email


def recieve_mail():
    days = {"Sun":"Sunday", "Mon":"Monday", "Tue":"Tuesday", "Wed":"Wednesday", "Thu":"Thursday", "Thur":"Thursday", "Fri":"Friday","Sat":"Saturday"}
    try:
        mail_obj = imap.IMAP4_SSL('imap.gmail.com','993')
        statement = "Connecting to your Mail Server"
        print(statement)    

        # mail_obj.login(email_id, email_pass)
        mail_obj.select("Inbox")

        status, msgnums = mail_obj.search(None, "unseen")
        mails = msgnums[0].split()

        if len(mails)<1:
            statement = "You have no new mail in your inbox"
            print(statement)
            

        elif len(mails)>= 1:
        
            if len(mails) == 1:
                statement = "You have a new mail in your inbox"
                print(statement)
                

            if len(mails) > 1:
                statement = f"You have {len(mails)} unread messages"
                print(statement)
                

            for mail in range(0,len(mails)):
                if len(mails)==1:
                    statement = "Reading mail"
                else:
                    statement = f"Reading mail {mail+1}...."

                print(statement)
                
                rc, data = mail_obj.fetch(mails[mail], "(RFC822)")
                message = imap_email.message_from_bytes(data[0][1])
                
                parts = message.get('From')
                parts = parts.replace("<","")
                parts = parts.replace(">","")
                sender = parts
                parts = parts.split(" ")
                 
                sender = sender.replace(parts[-1],"")

                statement = f"Mail from : {sender}"
                print(statement)
                

                statement = f"Mail from Email ID : {parts[-1]}"
                print(statement)
                

                statement = f"Date of mail : {message.get('Date')}"
                part = message.get('Date').split(" ")
                day = part[0].replace(",","")
                statement = statement.replace(day, days[day])
                statement = statement.replace(part[-1],"")
                print(statement)
                
                subject = message.get('Subject')

                if subject == '':
                    statement = "No Subject Found For This Email"
                else:
                    statement = f"Subject : {subject}"
                print(statement)
                
                statement = "Message in Mail :"
                print(statement,end=" ")
                
                for msg_data in message.walk():
                    if msg_data.get_content_type() == "text/plain":
                        mailbody = msg_data.as_string().replace("Content-Type: text/plain; charset=\"UTF-8\"","")
                        print(mailbody)
                        

            mail_obj.close()

    except:
        statement = "Not able to connect to mail server"