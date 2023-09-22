
from faulthandler import disable
from re import I
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DBconnect import moh
from DBconnect import Contacttab
from DBconnect import AESCipher

dbconnect=moh()

class ListText():
    def showdata(self):

        root=Tk()
        root.title('Hash Table')
        tv=ttk.Treeview(root)
        tv.pack()
       
        tv.heading('#0',text='ID')
        tv.configure(column=('#Name','#Username','#Password','#Passwordhash'))
        tv.heading('#Name',anchor=CENTER,text='Name')
        tv.heading('#Username',anchor=CENTER,text='Username')
        tv.heading('#Password',anchor=CENTER,text='Password')
        tv.heading('#Passwordhash',anchor=CENTER,text='Passwordhash')
        cursor=dbconnect.ListRequest()
        
        for row in cursor:
            tv.insert('','end','{}'.format(row['ID']),text=row['ID'])
            tv.set('{}'.format(row['ID']),'#Name',row['Name'])
            tv.set('{}'.format(row['ID']),'#Username',row['Username'])
            tv.set('{}'.format(row['ID']),'#Password',row['Password'])
            tv.set('{}'.format(row['ID']),'#Passwordhash',row['Passwordhash'])
        
        def selected():
          selected_item=tv.selection()[0]
          tv.delete(selected_item)
          dbconnect.Delete_item(selected_item)

        sel_btn = ttk.Button(root, text="Delete item", command=selected)
        sel_btn.pack()

        
          


class Listpassword():
    def comparepassword(self,Login,password):
       
        cursor=dbconnect.Comparepassword(password) 
        for row in cursor: 
            s=row['Name']
            Query=Contacttab()
            f=row['Username']
            h=row['Password']
            g=row['Passwordhash']       
            if(Login==f and password==g):
             msg="Welcome {}".format(s)
             messagebox.showinfo(title="Info",message=msg)
             win=Tk()
             win.title('{} page'.format(s))
            
             win.geometry("500x300")
             b1=ttk.Button(win,text='view database')
             b1.pack(padx=10,pady=10)
             def view_database():
                 with open('file1.txt') as a:
                     file1 = a.read()
                 with open('file2.txt') as b:
                     file2 = b.read()   
                 complexfiles=file1+file2
                 complexfiles=complexfiles[0:24]
                 global number
                 number=0
                 choice=input('plz enter table: ')
                 win=Tk()
                 win.title('VIEW DATA')
                 win.geometry("1200x600")
                 atree=ttk.Treeview(win)        
                 Columns=[]
                 values=[] 
                 Data=[]
                 a=count=0
                 data=Query.viewData(choice)
                 for column in data.description:
                     Columns.append(column[0])
                
                 Aes=AESCipher(complexfiles) 
                 conn = sqlite3.connect('Database.sqlite3')
                 cursor=conn.execute("CREATE TEMPORARY TABLE Temp AS SELECT * FROM "+choice+";")
                 cursor=conn.execute("ALTER TABLE Temp DROP COLUMN ID;")
                 cursor=conn.execute("SELECT * FROM Temp")
                 records=cursor.fetchall()
                 for row in records:
                     values.append(row)
                     
                 atree['columns']=(Columns)
                 atree.column('#0', width=0, stretch=NO)
                 atree.heading('#0', text='', anchor=W)
                 a=0
                 while(a<len(Columns)):
                     atree.column(Columns[a], anchor=W,width=140)
                     atree.heading(Columns[a], text=Columns[a], anchor=CENTER)
                     a+=1
                 while(count<len(values)):
                     j=0
                     alist=list(values[count])
                     while(j<len(alist)):
                         Data.append(Aes.decrypt(alist[j]))
                         j+=1
                     atree.insert(parent='',index='end',id=number,text='',values=(Data))
                     Data.clear()
                     number+=1
                     count+=1
                 atree.pack(pady=20)

                 entry_box_frame = LabelFrame(win, text="Contact Details")
                 entry_box_frame.pack(fill="x", pady=20)
                 my_data=[]
                 for x in range(len(Columns)):
                     name_label = Label(entry_box_frame, text=Columns[x]).grid(row=x, column=0, padx=10)
                     name_entry= Entry(entry_box_frame, width=15)
                     name_entry.grid(row=x, column=1)   
                     my_data.append(name_entry)   
                     
                 button_frame = LabelFrame(win, text="Controls")
                 button_frame.pack(fill="x", pady=20)
                    
                 new_contact_button = Button(button_frame, text="Add New Records" )
                 new_contact_button.pack(side=LEFT, padx=10, pady=10) 
                     
                 edit_contact_button = Button(button_frame, text="Update Records ")
                 edit_contact_button.pack(side=LEFT, padx=10, pady=10) 
                     
                 delete_contact_button = Button(button_frame, text="Delete Records")  
                 delete_contact_button.pack(side=LEFT, padx=10, pady=10)
                     

                 def insert_record():
                    
                     mylist=[] 
                     global number
                     for entries in my_data:
                         mylist.append(entries.get())
                         
                         
                     atree.insert(parent='',index='end',id=number,text='',values=(mylist))
                     number+=1
                        
                     Query.insert_Record(choice,Columns,mylist,len(Columns))
                     [widget.delete(0, END) for widget in entry_box_frame.winfo_children() if isinstance(widget, Entry)]

                 def delete_record():
                     selected_item=atree.selection()[0]
                     atree.delete(selected_item)
                     Query.Delete_item(choice,int(selected_item)+1)
                     
                     
                     
                 def update_record():
                     selected_item=atree.selection()[0]
                     mylist=[] 
                     global item
                     for entries in my_data:
                         mylist.append(entries.get())
                     atree.delete(selected_item)
                     atree.insert(parent='',index=selected_item,id=selected_item,text='',values=(mylist))
                     Query.Update_item(choice,Columns,mylist,int(selected_item)+1,len(Columns))
                     [widget.delete(0, END) for widget in entry_box_frame.winfo_children() if isinstance(widget, Entry)]
                 
                 new_contact_button.configure(command=insert_record)
                 delete_contact_button.configure(command=delete_record)
                 edit_contact_button.configure(command=update_record)

                 win.mainloop()   

             b1.configure(command=view_database)
             if(f=='admin'):
                 b2=ttk.Button(win,text="Generate Key")
                 b2.pack(padx=10,pady=10)
                 def Generate_Key():
                     window=Tk()
                   
                     window.geometry("300x100")
                     window.title('Generate Key page')
                     #label_file_explorer = Label(window,width=20,text='No file chosen',font=('Arial',12))
                     #label_file_explorer.grid(row=0,column=1,padx=30,pady=15)
                     #BuBrowse=ttk.Button(window,text='Browse')
                     #BuBrowse.grid(row=0,column=3)
                     l1=ttk.Label(window,text='Key').grid(row=1,column=0,padx=15,pady=5)
                     e2=ttk.Entry(window,width=20,font=('Arial',12))
                     e2.grid(row=1,column=1,padx=0,pady=5)
                     bu=ttk.Button(window,text='Generate key')
                     bu.grid(row=2,column=1)


        
                     def Generate_key():
                         Query.Split_Key(e2.get())
                         
                         
                     #def Browse():
                         #filename = filedialog.askopenfilename(initialdir = "C:\\Users\\Al-mousawi\\Desktop\\python\\project",title = "Select a Database",filetypes = (("SQLITE3 File","*.sqlite3*"),("ALL FILES","*.*")))
                         #path=os.path.normpath(os.path.basename(filename))
                         #label_file_explorer.configure(text=path)
                     #BuBrowse.configure(command=Browse)
                     
                     bu.configure(command=Generate_key)  
                 b2.configure(command=Generate_Key)
                 #b3=ttk.Button(win,text='Decryption Database')
                 #b3.pack()
             b4=ttk.Button(win,text="Insert database")
             b4.pack(padx=10,pady=10)
             def InsertDatabase():
                 b5=ttk.Button(win,text="insert_column")
                 b5.pack()
                 b6=ttk.Button(win,text="insert_data")
                 b6.pack()
                 def insert_column():
                     global count
                     count=0
                     c=Tk()
                     c.title('insert column')
                     c.geometry('500x600')
                 
                     tree=ttk.Treeview(c)
                     tree['columns']=('Column Name', 'Data Type', 'Allow Null')
                     tree.column('#0', width=0, stretch=NO)
                     tree.column('Column Name', anchor=W,width=140)
                     tree.column('Data Type', anchor=CENTER,width=100)
                     tree.column('Allow Null', anchor=W,width=140)
                     tree.heading('#0', text='', anchor=W)
                     tree.heading('Column Name', text='Column Name', anchor=W)
                     tree.heading('Data Type', text='Data Type', anchor=CENTER)
                     tree.heading('Allow Null', text='Allow Null', anchor=CENTER)
                     add_frame=Frame(c)
                     add_frame.pack(pady=20)
                   

                     t1=Label(add_frame,text='Table Name').grid(row=1,column=1) 
                     c1=Label(add_frame,text="Column Name").grid(row=3,column=0)
                     D1=Label(add_frame,text="Data Type").grid(row=3,column=1)
                     A1=Label(add_frame,text="Allow Null").grid(row=3,column=2)

                     menu=StringVar(add_frame,'None')
                     
                     global tabname

                     tabname=ttk.Entry(add_frame)
                     tabname.grid(row=2,column=1)
                     ColumnName=ttk.Entry(add_frame)
                     ColumnName.grid(row=4,column=0)
                     DataType=OptionMenu(add_frame,menu,"Varchar(255)","AutoNumber","Text","nchar","bit",'int','Currency','Byte')
                     DataType.grid(row=4,column=1)
                     DataType.config(width=10)
                     boolvar = BooleanVar(add_frame)               
                     AllowNull =Checkbutton(add_frame,variable=boolvar)
                     AllowNull.grid(row=4,column=2) 
                     global Columns 
                     global type
                     Columns=[]
                     type=[]
                     

             
                     def Addrecord():
                         if len(ColumnName.get())==0:
                             messagebox.showinfo(title='Error',message="Column Name Should not be empty")
                         else:
                             global count, InputtedData
                            
                             InputtedData=[ColumnName.get(),menu.get(),boolvar.get()] 
                             Columns.append(ColumnName.get())
                             type.append(menu.get())
                             
                            
                             tree.insert(parent='',index='end',id=count,text='',values=(InputtedData))
                             count+=1            
                             ColumnName.delete(0,END)
                     
                     
                     def Removerecord():
                          d=tree.selection()[0]
                          tree.delete(d)
                          
                     def Saverecord():
                         Query.Adddata(tabname.get(),Columns,type,count)

                     add_record=Button(c,text='Add record',command=Addrecord)
                     add_record.pack(pady=5)

                     remove_record=Button(c,text='Remove record',command=Removerecord)
                     remove_record.pack(pady=5)

                     remove_record=Button(c,text='Save record',command=Saverecord)
                     remove_record.pack(pady=5)

                     tree.pack(pady=20)
                     c.mainloop()
                 b5.configure(command=insert_column)
                
                 def Insert_Data():
                     global item
                     item=0
                     i=0
                     v=Tk()
                     v.title('Insert Data')
                     v.geometry('500x600')
                  
                     atre=ttk.Treeview(v)
                     atre['columns']=(Columns)
                     atre.column('#0', width=0, stretch=NO)
                     atre.heading('#0', text='', anchor=W)
                     while(i<count):
                          atre.column(Columns[i], anchor=W,width=140)
                          atre.heading(Columns[i], text=Columns[i], anchor=CENTER)
                          i+=1
                     atre.pack(pady=20)
                    
                     entry_box_frame = LabelFrame(v, text="Contact Details")
                     entry_box_frame.pack(fill="x", pady=20)
                  
                     my_entries=[]
                     
                     for x in range(count):
                         name_label = Label(entry_box_frame, text=Columns[x]).grid(row=x, column=0, padx=10)
                         name_entry= Entry(entry_box_frame, width=15)
                         name_entry.grid(row=x, column=1)
                         my_entries.append(name_entry)     
                        

                     button_frame = LabelFrame(v, text="Controls")
                     button_frame.pack(fill="x", pady=20)
              
                     
                     new_contact_button = Button(button_frame, text="Add New Records" )
                     new_contact_button.pack(side=LEFT, padx=10, pady=10) 
 
                     edit_contact_button = Button(button_frame, text="Update Records ")
                     edit_contact_button.pack(side=LEFT, padx=10, pady=10) 
 
                     delete_contact_button = Button(button_frame, text="Delete Records")
                     delete_contact_button.pack(side=LEFT, padx=10, pady=10)
                   
                     def insert_record():
                         mylist=[] 
                         global item       
                         for entries in my_entries:
                             mylist.append(entries.get())
                         atre.insert(parent='',index='end',id=item,text='',values=(mylist))
                         item=item+1
                         Query.insert_Record(tabname.get(),Columns,mylist,count)
                         [widget.delete(0, END) for widget in entry_box_frame.winfo_children() if isinstance(widget, Entry)]

                     def delete_record():
                         selected_item=atre.selection()[0]
                         print(selected_item)
                         atre.delete(selected_item)
                         Query.Delete_item(tabname.get(),int(selected_item)+1)


                     def update_record():
                         selected_item=atre.selection()[0]
                         mylist=[] 
                         global item       
                         for entries in my_entries:
                             mylist.append(entries.get())
                         atre.delete(selected_item)
                         atre.insert(parent='',index=selected_item,id=selected_item,text='',values=(mylist))
                         Query.Update_item(tabname.get(),Columns,mylist,int(selected_item)+1,count)
                         

                     new_contact_button.configure(command=insert_record)
                     delete_contact_button.configure(command=delete_record)
                     edit_contact_button.configure(command=update_record)
                     v.mainloop()
                     
                 b6.configure(command=Insert_Data)                   
            
             b4.configure(command=InsertDatabase)
             

            elif(Login!=f or password!=g):
             msg="Invaild username/password"
             messagebox.showinfo(title="Info",message=msg)


  