import hashlib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DBconnect import moh
from ListRequest import ListText
from ListRequest import Listpassword

dbConnect=moh()

def create_Login():
    login=Tk()
    login.title('Login page')
    
    Label(login, text="Login").grid(row=0,column=0,padx=10,pady=10)
    Login=ttk.Entry(login,width=20,font=('Arial',12))
    Login.grid(row=0,column=1,columnspan=20,padx=5,pady=5)
    ttk.Label(login, text="Password").grid(row=1,column=0,padx=10,pady=10)
    password=ttk.Entry(login,width=20,font=('Arial',12))
    password.grid(row=1,column=1,columnspan=20,padx=5,pady=5)
    bulogin=ttk.Button(login,text='Login')
    bulogin.grid(row=3,column=3,columnspan=50)
    
  
    

    def showpassword():
     MD5 = hashlib.md5(password.get().encode())
     request=Listpassword()
     
     request.comparepassword(Login.get(),MD5.hexdigest())

    bulogin.config(command=showpassword)

def show_data():
    request=ListText()
    request.showdata()
      
def create_Signup():
    signup=Tk()
    signup.title('signup page')
    ttk.Label(signup,text='Name').grid(row=0,column=0,padx=10,pady=10)
    Name=ttk.Entry(signup,width=20,font=('Arial',12))
    Name.grid(row=0,column=1,columnspan=20,padx=5,pady=5)
    ttk.Label(signup,text='Username').grid(row=1,column=0,padx=10,pady=10)
    Username=ttk.Entry(signup,width=20,font=('Arial',12))
    Username.grid(row=1,column=1,columnspan=20,padx=5,pady=5)
    ttk.Label(signup,text='password').grid(row=2,column=0,padx=10,pady=10)
    Password=ttk.Entry(signup,width=20,font=('Arial',12))
    Password.grid(row=2,column=1,columnspan=20,padx=5,pady=5)
    
    busignup=ttk.Button(signup,text='Sign up')
    busignup.grid(row=3,column=3)
   

    def save_data():
       MD5 = hashlib.md5(Password.get().encode())
       print('Name: {}'.format(Name.get()))
       print('Username: {}'.format(Username.get()))
       print('Password: {}'.format(Password.get()))
       
       print(MD5.hexdigest())
       msg=dbConnect.Add(Name.get(),Username.get(),Password.get(),MD5.hexdigest())
       messagebox.showinfo(title='Add info',message=msg)
       signup.destroy()

    busignup.config(command=save_data)
    
    

    






root=Tk()

root.geometry("300x150")
root.title("Encryption Tool")
style=ttk.Style()
b1=ttk.Button(root,text='Login',width=20,command=create_Login).pack(padx=10,pady=10)
b2=ttk.Button(root,text='Sign up',width=20,command=create_Signup).pack(padx=10,pady=10)
b3=ttk.Button(root,text='Show Data',width=20,command=show_data).pack(padx=10,pady=10)






root.mainloop()

