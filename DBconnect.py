import base64
import hashlib
from Crypto.Cipher import AES
import hashlib
import sqlite3
class moh:
        def __init__(self):
            self._db=sqlite3.connect('Hashtable.sqlite3')
            self._db.row_factory=sqlite3.Row
            self._db.execute('create table if not exists Text(ID integer primary key autoincrement, Name text, Username text, Password text,Passwordhash text)')
            self._db.commit()

        def Add(self,Name,Username,Password,Passwordhash):
                self._db.execute('insert into Text(Name,Username,Password,Passwordhash) values(?,?,?,?)',(Name,Username,Password,Passwordhash))
                self._db.commit()
                return 'request is submitted'

        def ListRequest(self):
            cursor=self._db.execute('select * from Text')
            return cursor

        def Comparepassword(self,password):
            
            cursor=self._db.execute('SELECT * FROM Text WHERE Passwordhash= "{}"'.format(password))
            return cursor
            
        def Delete_item(self,ID):
            self._db.execute('Delete from Text where ID={}'.format(ID))
            self._db.commit()
            print('your item is deleted')


class Contacttab:
    def __init__(self):
        self._Data = sqlite3.connect('Database.sqlite3')
        self._Data.row_factory=sqlite3.Row
        self._Data.commit()
        with open('file1.txt') as a:
            file1 = a.read()
        with open('file2.txt') as b:
            file2 = b.read()  
        global complexfiles
        complexfiles=file1+file2
        complexfiles=complexfiles[0:24]
    
        print('Database is created')
    
    
    def Adddata(self,tablename,col,type,count): 
        i=0
        self._Data.execute("create table if not exists  "+tablename+"(ID integer primary key autoincrement, "+col[i]+" "+type[i]+")")
        i+=1
        self._Data.commit() 
        if (count>1):
            while(i<count):
                self._Data.execute("ALTER TABLE "+tablename+" ADD "+col[i]+" "+type[i]+"")
                i+=1
        self._Data.commit()
        print ('request is submitted')


    def insert_Record(self,tablename,col,values,count):
        Aes=AESCipher(complexfiles)
        i=0
        self._Data.execute("INSERT INTO "+tablename+"("+col[i]+") VALUES (?)",[Aes.encrypt(values[i])])
        self._Data.commit()
        i+=1
        if (count>1):
            while(i<count):
            
                self._Data.execute("UPDATE "+tablename+" SET "+col[i]+" = '"+Aes.encrypt(values[i])+"' WHERE "+col[0]+" = '"+Aes.encrypt(values[0])+"';")
                self._Data.commit()
                i+=1 
        print ('Records are saved')

    def Delete_item(self,tablename,ID):
        self._Data.execute('Delete from '+tablename+' where ID={}'.format(ID))
        self._Data.commit()
        print('your item is deleted')

    def Update_item(self,tablename,col,values,ID,count): 
        Aes=AESCipher(complexfiles)
        for i in range(count):
            self._Data.execute("UPDATE "+tablename+" SET "+col[i]+" = '"+Aes.encrypt(values[i])+"' WHERE ID = "+str(ID)+";")
            self._Data.commit()
        print('your item is updated')

  

    def Split_Key(self,Label):
        MD5 = hashlib.md5(Label.encode())
        print(MD5.hexdigest())
        s1=MD5.hexdigest()[0:16]
        s2=MD5.hexdigest()[16:32]
        '''
        msg = EmailMessage()
        msg.set_content(s2)
        msg['Subject'] = 'Python'
        msg['From'] = "mousawi.mohannad@gmail.com"
        msg['To'] = "mousawi.mohannad@gmail.com"
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login('mousawi.mohannad@gmail.com','lexoeclibzujwewf')
        server.send_message(msg)
        server.quit()
        print('your message is sent')
        '''
        a=open('file1.txt', 'w')
        a.write(s1)
        b=open('file2.txt', 'w')
        b.write(s2)
        print('Your key is splitted')


    def viewData(self,tablename):
        cursor=self._Data.execute("CREATE TEMPORARY TABLE Temp  AS SELECT * FROM {};".format(tablename))
        cursor=self._Data.execute("ALTER TABLE Temp DROP COLUMN ID;")
        cursor=self._Data.execute("SELECT * FROM Temp")
        return cursor

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = key.encode()
      

    def encrypt(self, raw):
        raw = self._pad(raw) 
        cipher = AES.new(self.key, AES.MODE_ECB)
        return (base64.b64encode(cipher.encrypt(raw.encode()))).decode()
       
        

    def decrypt(self, enc):
        enc = base64.b64decode(enc)  
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc).decode('utf-8'))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]