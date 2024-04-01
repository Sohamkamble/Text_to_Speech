import pyttsx3
import gtts
from playsound import playsound  # Object is not callable error will occur if method name is same as module, so import playsound from module playsound AND not only import playsound
from tkinter import *
from tkinter import scrolledtext, filedialog
from PIL import ImageTk, Image
import os, random
import PyPDF2

# gTTS Module Conversion
global myjob
def googlecon():
    global myjob
    readtext=TextBox.get(1.0,"end-1c")
    myjob=gtts.gTTS(text=readtext, lang='en', tld="co.in")
    myjob.save('gsample.mp3')
    playsound("gsample.mp3")

# pyttsx3 conversion
def pyttsx3con(Rate,Volume,Gender):
    readtext=TextBox.get(1.0,"end-1c")
    engine=pyttsx3.init()
    engine.setProperty("rate",Rate.get())
    engine.setProperty("volume",float(Volume.get())/100)  # Range 0-1   NOTE: Convert DoubleVar() i.e Volme.get()     to float() i.e float(Volume.get())    
    VOICE=engine.getProperty("voices")
    engine.setProperty("voice",VOICE[Gender.get()].id)     
    engine.say(readtext)
    engine.save_to_file(readtext,"pysample.mp3")
    engine.runAndWait()
    


# Reading Text
def MainConversion():
    global mode, rateScale,volSpin,sharedVar, LogText
    if (mode.get()==1):
        try:
            LogText.insert(END,"Please Wait, Converting Online...\n\n","msgon")
            LogText.tag_config("msgon", font="consolas 15 bold", foreground='#FF0000')
            LogText.yview(END)
            LogText.update()
            googlecon()

        except:
            LogText.insert(END,"Internet not connected, Converting Offline...\n\n","msgoff1")
            LogText.tag_config("msgoff1", font="consolas 15 bold", foreground="#FF1493")
            LogText.yview(END)
            LogText.update()
            pyttsx3con(rateScale,volSpin,sharedVar)
    if (mode.get()==2):
        LogText.insert(END,"Converting in Offline   Mode\n\n","msgoff2")
        LogText.tag_config("msgoff2", font="consolas 15 bold", foreground="#FF1493")
        LogText.yview(END)
        LogText.update()
        pyttsx3con(rateScale,volSpin,sharedVar)

    
''' Reading Text  
def Read():
    readtext=TextBox.get(1.0,"end-1c")          # Here 1.0 refers 1st line(index) 0th character i.e first character and end-1c refers 1 character after end character
'''
# Saving Audio 
def Save():
    global myjob
    file=filedialog.asksaveasfilename(defaultextension='.mp3',filetypes=[("Audio File",".mp3")])
    gTTS_File=r"C:\Users\s2kso\Desktop\Texttospeech\gsample.mp3"   
    pyttsx3_File=r"C:\Users\s2kso\Desktop\Texttospeech\pysample.mp3"
    if (mode.get()==1):                               
        try:
            if os.path.getsize(gTTS_File)==0:
                os.remove(gTTS_File)
                audfile=open(gTTS_File,"rb")
            else:
                audfile=open(gTTS_File,"rb")
                LogText.insert(END,"gTTS File Saved\nSuccessfully\n","msg")
                LogText.tag_config("msg", font="helvetica 17 bold", foreground='green')
                LogText.yview(END)
                LogText.update()
        except:
            try:
                audfile=open(pyttsx3_File,"rb")
                LogText.insert(END,"gTTS File not created,   Saving pyttsx3 File\n","msg")
                LogText.tag_config("msg", font="helvetica 17 bold", foreground='red')
                LogText.yview(END)
                LogText.update()
            except:
                pass

    if (mode.get()==2):  
        try:
            audfile=open(pyttsx3_File,"rb")
            LogText.insert(END,"pyttsx3 File Saved\nSuccessfully\n","msg")
            LogText.tag_config("msg", font="helvetica 17 bold", foreground='green')
            LogText.yview(END)
            LogText.update()
        except:
            pass



        
    try:
        c=audfile.read()
        audfile.close()
        writeaud2file=open(file,"wb")
        writeaud2file.write(c)
        writeaud2file.close()
    except:
        LogText.insert(END,"ERROR IN SAVING FILE\n","msg")
        LogText.tag_config("msg", font="helvetica 20 bold", foreground='red')
        LogText.yview(END)
        LogText.update()

# Saving Text
def SaveText():
    fileName=filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[("Text File",".txt")])
    TextFile=open(fileName,"w")
    TextFile.write(str(TextBox.get(1.0,END)))
    TextFile.close()

# Opening Files
def Open():
    global TextBox
    files=[('Text Files','*.txt'),('PDF Files','*.pdf')]
    #doc=filedialog.askopenfile(mode="r",filetypes=files,defaultextension=files)
    doc=filedialog.askopenfilename(initialdir='/',filetypes=files)
    if (doc[-4:]) in (".txt",".TXT",".Txt"):
        file=open(doc,"r")
        content=file.read()
        file.close()
        TextBox.delete('1.0',END)
        TextBox.insert('1.0',content)
        TextBox.yview(END)
    if (doc[-4:]) in (".pdf",".PDF",".Pdf"):
        file = PyPDF2.PdfFileReader(doc)
        TextBox.delete('1.0',END)
        for i in range(file.numPages):
            TextBox.insert(END,f"Reading Page {i+1}\n")
            TextBox.insert(END, str(file.getPage(i).extractText()))
        TextBox.yview(END)

# Creating Tk() variable and title,geometry and background
root=Tk()
root.title("T2S")
root.geometry('1205x720+155+30')
bg=ImageTk.PhotoImage(Image.open(f"C:\\Users\\s2kso\\Desktop\\Projects\\Texttospeech\\260- Gradient Download By ST\\Gradient Pack By Sudip Talk{random.randint(0,2)}{random.randint(0,6)}{random.randint(0,9)}.jpg"))
canvas1=Canvas(root,width=1200, height=720)
canvas1.pack(fill="both", expand=TRUE)
canvas1.create_image(0,0,image=bg, anchor="nw")

# Creating Textbox of ScrolledText
global TextBox
TextBox=scrolledtext.ScrolledText(root,height=15,width=99, padx=10, pady=10, font="comicsans 15",undo=TRUE)
TextBox.place(x=40,y=20) 

# Creating Read, Clear, Save and Open Button
readButton=Button(root, text="READ TEXT", font="comicsans 12 bold", relief=RIDGE,padx=5, pady=3, command=MainConversion)
readButton.place(x=122, y=395)

clearButton=Button(root, text="CLEAR TEXT", font="comicsans 12 bold", relief=RIDGE,padx=5, pady=3,command=lambda :TextBox.delete('1.0',END))
clearButton.place(x=401,y=395)

saveButton=Button(root, text="SAVE AUDIO", font="comicsans 12 bold",padx=5, pady=3, relief=RIDGE, command=Save)
saveButton.place(x=680, y=395)

openFileButton=Button(root,text="OPEN FILE", font="comicsans 12 bold",padx=5, pady=3, relief=RIDGE, command=lambda :Open())
openFileButton.place(x=959,y=395)         

# Creating Setting and log label and LogTextbox
setting=Label(root, text="SETTINGS (For Offline Conversion only)",font="comicsans 15 bold",relief=FLAT)
setting.place(x=340, y=475)
Log=Label(root, text="Logs",font="comicsans 15 bold",relief=FLAT)
Log.place(x=992, y=475)
global LogText
LogText=scrolledtext.ScrolledText(root,height=5, width=24, padx=7,pady=7,font="comicsans 15")
LogText.place(x=870,y=523)

# Creating Voice, Volume, Type Label
voiceRateLabel=Label(root, text="SET VOICE RATE", font="comicsans 12 bold", relief=RIDGE,padx=5, pady=3)
voiceRateLabel.place(x=122,y=525)
setVolumeLabel=Label(root, text="  SET VOLUME  ", font="comicsans 12 bold",padx=5, pady=3, relief=RIDGE)
setVolumeLabel.place(x=401, y=525)
voiceTypeLabel=Label(root,text="VOICE TYPE", font="comicsans 12 bold",padx=5, pady=3, relief=RIDGE)
voiceTypeLabel.place(x=680,y=525) 

# Creating Voice, Volume, Type options
global rateScale, volSpin
rateScale=Scale(root, from_=100, to=250, orient=HORIZONTAL, length=140, sliderlength=10, sliderrelief=FLAT,fg="green",font="consolas 15 bold")
rateScale.place(x=122,y=580)
rateScale.set(150)
volSpinValue=StringVar(root)
volSpin=Spinbox(root, values=(00,10,20,30,40,50,60,70,80,90,100), fg="green",justify="center",width=9,font="consolas 18 bold", textvariable=volSpinValue)
volSpin.place(x=401,y=580)
volSpinValue.set('70')

global sharedVar
sharedVar=IntVar(None,0)
r1=Radiobutton(root,text="Male",font="consolas 11 bold",padx=13,value=0,variable=sharedVar)
r1.place(x=680,y=580)
r2=Radiobutton(root,text="Female",font="consolas 11 bold",padx=5,value=1,variable=sharedVar)
r2.place(x=680,y=600)

# Creating Button and Labels List for hovering Effect
# Changing Button Color
def hover(widget):
    widget.bind("<Enter>", func=lambda e: widget.config(background="yellow"))
    widget.bind("<Leave>", func=lambda e: widget.config(background="white"))
widgets=[readButton,clearButton,saveButton,openFileButton,rateScale,volSpin,r1,r2]
for item in widgets:
    hover(item)

# Creating Menubar
menubar=Menu(root)

# Creating File Menu
filemenu=Menu(menubar,tearoff=0,borderwidth=25)
filemenu.add_command(label="      Open File",command=Open)
filemenu.add_command(label="      Save Audio",command=Save)
filemenu.add_command(label="      Save Text",command=SaveText)
filemenu.add_separator()
filemenu.add_command(label="      Quit",accelerator="\t\t\t\t", command=root.destroy)
# NOTE NOTE ::: filemenu.config("consolas", 10) will give bwlow error
# TypeError: Misc.configure() takes from 1 to 2 positional arguments but 3 were given, HERE YOU have to specify the name of that argument
# SOLUTION ==>  filemenu.config(font="consolas 10")     
menubar.add_cascade(label="File", menu=filemenu)

# Creating Edit Menu
editmenu=Menu(menubar,tearoff=0)
editmenu.add_command(label="Read Text",command=MainConversion)
editmenu.add_command(label="Clear Text",command= lambda: TextBox.delete('1.0',END)) 
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator="Ctrl+X", command= lambda: TextBox.event_generate(("<<Cut>>")))
editmenu.add_command(label="Copy", accelerator="Ctrl+C",command= lambda: TextBox.event_generate(("<<Copy>>")))
editmenu.add_command(label="Paste", accelerator="Ctrl+V",command= lambda: TextBox.event_generate(("<<Paste>>")))
editmenu.add_separator()
editmenu.add_command(label="Conversion Mode",command=lambda:print(rateScale.get()))
global mode
mode=IntVar(None,1)
er1=editmenu.add_radiobutton(label="Online(gTTS)",value=1,variable=mode)
er2=editmenu.add_radiobutton(label="Offline(pyttsx3)",value=2,variable=mode)
menubar.add_cascade(label="Edit",menu=editmenu)



root.config(menu=menubar)
root.mainloop()

# Removing sample files
if (os.path.exists('gsample.mp3')):
        os.remove("gsample.mp3")
if (os.path.exists('pysample.mp3')):
        os.remove("pysample.mp3")
