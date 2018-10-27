import Tkinter as tk
import ttk
import os
import tkFont
import tkFileDialog
import tkMessageBox
import threading
from datetime import datetime

class Editor(tk.Tk):

    def __init__(self):

        #This function is necessary to start tk
        tk.Tk.__init__(self)
        self.name="Py Notepad"
        self.get_keywords("keywords.ini")
        self.keywords=[]
        #This calls exit_editor when the cross button is pressed.
        self.protocol("WM_DELETE_WINDOW", self.exit_editor)

        #These are instance variables that are required for the program to run.
        self.filename=""
        self.saved=False
        self.actively_highlighting=False
        #This calls selectall function when <control>+a is pressed.
        self.bind_class("Text","<Control-a>", self.selectall)

        #This initializes all the gui elements
        self.initialize()
        self.footer_update()
    
    def get_keywords(self,filename):
        self.languages={}
        f=open(filename)
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not line2: break
            language={
                      "name":line1.split(",")[0].strip(),
                      "keywords":[x.strip() for x in line2.split(",")],
            }
            self.languages[line1.split(",")[1].strip()]=language
            lineextra=f.readline()
    
    def external_commands(self,command_type,event=None):
        if self.filename=="":
            self.save_file_as()
            return
        def comp(filename):
            if not os.path.isfile(os.getcwd()+"/buildscripts/"+os.path.splitext(filename)[1].lower()[1:]+command_type+".sh"):
                os.system("gnome-terminal -- buildscripts/error.sh")
                return
            os.system("gnome-terminal --  buildscripts/"+os.path.splitext(filename)[1].lower()[1:]+command_type+".sh "+filename)
        th=threading.Thread(target=comp,args=(self.filename,))
        th.deamon=True
        th.start()

    def execute(self,even=None):
        self.external_commands("execute")
        
    def build(self,event=None):
        self.external_commands("build")
        
    def compile(self,event=None):
        self.external_commands("compile")
        
    def initialize(self):
        self.create_menu()
        self.create_mainFrame()
        self.render_mainFrame()
        # Uncomment below to use alternative highlighter.....
        # Don't forget to disable previous higlighter
        #self.highlighter=Highlighter(self.main_text)


    def render_mainFrame(self):

        #Call grid on all the contents to show in the gui
        self.linenumbers.grid(column=0,row=0,sticky="NSEW")
        self.main_text.grid(column=1,row=0,sticky="NSEW")
        self.main_scroll_bar.grid(column=2,row=0,sticky="NS")
        self.footer.grid(column=0,row=1,columnspan=2,sticky="E")

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=0)
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=0)

        #Set focus to the main_text element.(The main white text box)

        self.main_text.focus_set()

    def toggle_linenumber_view(self):
        if not self.linenumber_view.get():
            self.linenumbers.grid_remove()
        else:
            self.linenumbers.grid()
            
    
    def toggle_highlight_view(self,event=None):
        if not event is None:
            self.highlight_view.set(not self.highlight_view.get())
        if not self.highlight_view.get():
            self.main_text.bind('<KeyRelease>',lambda _:self.highlight_current_line())
            self.main_text.bind("<KeyRelease>",self.footer_update,add="+")
            start="1.0"
            end="end"
            self.main_text.tag_remove("keyword",start,end)
            self.main_text.tag_remove("symbol",start,end)
            self.main_text.tag_remove("number",start,end)
            self.main_text.tag_remove("string",start,end)
            self.main_text.tag_remove("comment",start,end)
        else:
            self.main_text.bind("<KeyRelease>",self.syntax_highlight,add="+")
            self.syntax_highlight()

    def toggle_footer_view(self):
        if not self.footer_view.get():
            self.footer.grid_remove()
        else:
            self.footer.grid()


    def create_menu(self):

        #Creating the Menu objects

        self.main_menu=tk.Menu(self)
        self.config(menu=self.main_menu) #This set the main_menu for the program as main_menu.
        self.file_menu=tk.Menu(self,tearoff=0)
        self.edit_menu=tk.Menu(self,tearoff=0)
        self.view_menu=tk.Menu(self,tearoff=0)
        self.tools_menu=tk.Menu(self,tearoff=0)
        self.help_menu=tk.Menu(self,tearoff=0)

        #setting styles for menus
        self.main_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)
        self.file_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)
        self.edit_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)
        self.view_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)
        self.tools_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)
        self.help_menu.config(bg="#313131",fg="white",activebackground="#4d4d4d",activeforeground="white",activeborderwidth=0,border=0)

        #For main menu

        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.main_menu.add_cascade(label="View", menu=self.view_menu)
        self.main_menu.add_cascade(label="Tools", menu=self.tools_menu)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)

        #For file menu

        self.file_menu.add_command(label="New",command=self.new_file,accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open",command=self.open_file,accelerator="Ctrl+O")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save",command=self.save_file,accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As",command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit",command=self.exit_editor)



        #For edit menu

        self.edit_menu.add_command(label="Copy",command=lambda:self.focus_get().event_generate('<<Copy>>'),accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Cut",command=lambda:self.focus_get().event_generate('<<Cut>>'),accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste",command=lambda:self.focus_get().event_generate('<<Paste>>'),accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Select All",command=lambda: self.main_text.tag_add("sel","1.0","end"),accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo",command=self.undo_action,accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo",command=self.redo_action,accelerator="Ctrl+Y")



        #For view menu
        self.highlight_view=tk.BooleanVar()
        self.highlight_view.set(True)
        self.view_menu.add("checkbutton",variable=self.highlight_view,onvalue=True,offvalue=False
                            ,label="Highlight Syntax (.py)",command=self.toggle_highlight_view,accelerator="Ctrl+Shift+h")
        self.view_menu.add_separator()
        self.linenumber_view=tk.BooleanVar()
        self.linenumber_view.set(True)
        self.footer_view=tk.BooleanVar()
        self.footer_view.set(True)
        self.view_menu.add("checkbutton",variable=self.linenumber_view,onvalue=True,offvalue=False,label="Show/Hide Line Numbers",command=self.toggle_linenumber_view)
        self.view_menu.add("checkbutton",variable=self.footer_view,onvalue=True,offvalue=False,label="Show/Hide Footer",command=self.toggle_footer_view)



        #For tools menu

        self.tools_menu.add_command(label="Add Date/Time",command=lambda:self.main_text.insert("insert",str(datetime.now()).split(".")[0]))
        self.tools_menu.add_command(label="Execute",command=self.execute,accelerator="F5")
        self.tools_menu.add_command(label="Build",command=self.build,accelerator="F6")
        self.tools_menu.add_command(label="Compile",command=self.compile,accelerator="F8")
        
        

        #For help menu

        self.help_menu.add_command(label="About",command=self.about,accelerator="F1")




    def create_mainFrame(self):
        #Magic numbers are present here

        self.main_text_height=30
        self.main_text_width=100


        #Declaring all string Vars here.
        self.footer_text=tk.StringVar()

        #Declaring all widget objects here
        self.linenumbers = TextLineNumbers(self, width=55)
        self.linenumbers.config(bg="#191919",border=0,highlightthickness=0)
        self.main_text=CustomText(self,height=self.main_text_height,width=self.main_text_width,background="#111111",foreground="white",insertbackground="white")
        font=tkFont.Font(font=self.main_text['font'])
        self.main_text.config(border=0,highlightthickness=0,tabs=(font.measure(" "*4,)))
        self.linenumbers.attach(self.main_text)
        self.main_scroll_bar=ttk.Scrollbar(self,command=self.main_text.yview)
        self.main_text.configure(yscrollcommand=self.main_scroll_bar.set,undo=True,maxundo=-1,autoseparators=True)
        self.main_text.config(maxundo=20,padx=15,pady=10)
        self.footer=ttk.Label(self,textvariable=self.footer_text)
        self.footer.config(background="#313131",foreground="white")


        #Set font tags here which will be later used to highlight the keywords.

        self.main_text.tag_config("keyword",foreground="#5c6bce")
        self.main_text.tag_config("currentLine",background="#191919")
        self.main_text.tag_config("symbol",foreground="#f26957")
        self.main_text.tag_config("number",foreground="#dbe572")
        self.main_text.tag_config("string",foreground="#55c431")
        self.main_text.tag_config("comment",foreground="grey")




        #Set the bindings here For shortcuts

        self.main_text.bind("<Control-s>",self.save_file)
        self.main_text.bind("<Control-o>",self.open_file)
        self.main_text.bind("<Control-n>",self.new_file)
        self.main_text.bind("<Control-q>",self.exit_editor)
        self.main_text.bind("<Control-c>",self.copy_selection)
        self.main_text.bind("<Control-v>",self.paste_selection)
        self.main_text.bind("<Control-x>",self.cut_selection)
        self.main_text.bind("<Control-Shift-H>",self.toggle_highlight_view)
        self.main_text.bind("<F1>",self.about)
        self.main_text.bind("<F5>",self.execute)
        self.main_text.bind("<F6>",self.build)
        self.main_text.bind("<F8>",self.compile)

        #This updates the linenumbers
        self.main_text.bind("<<Change>>", self._on_change)
        self.main_text.bind("<Configure>", self._on_change)

        #This updates the currentlinehighlight.
        self.main_text.bind('<KeyRelease>',lambda _:self.highlight_current_line())
        self.main_text.bind('<Button-1>',lambda _:self.highlight_current_line())

        #This updates the line number and column number every time the cursor is moved.
        #Also syntax highlights
        self.main_text.bind("<KeyRelease>",self.footer_update,add="+")
        self.main_text.bind("<KeyRelease>",self.syntax_highlight,add="+")
        self.main_text.bind("<ButtonRelease-1>",self.footer_update)



        #Setting the initial footer text here.

        self.footer_text.set("Line: 1\tCol: 0")


    def _on_change(self, event):
        self.linenumbers.redraw()


    def new_file(self,event=None):
        if self.filename=="" and self.main_text.get("1.0", 'end-1c')=="":
            pass
        else:
            if self.saved:
                self.main_text.delete(1.0,tk.END)
                self.title(self.name+" - Untitiled")
                return 
                
            if tkMessageBox.askyesno("Save File?","Save current file?")==True:
                self.save_file()
            else:
                self.main_text.delete(1.0,tk.END)
                self.title(self.name+" - Untitiled")

    def open_file(self,event=None):
        file_options = {}
        file_options["defaultextension"] = ".txt"
        file_options["filetypes"]=[(value["name"],"."+key)  for key, value in self.languages.iteritems()]
        file_options["initialdir"] = os.getcwd()
        file_options['title'] = "Open File"
        filename=tkFileDialog.askopenfilename(**file_options)
        if filename!=() and filename!="" and filename!=None:
            try:
                self.filename=filename
                self.title(self.name+" - "+self.filename)
                file_descriptor=open(filename)
                self.main_text.delete(1.0,tk.END)
                self.main_text.insert(1.0,file_descriptor.read())
                self.update_keywords(filename)
                file_descriptor.close()
                if self.highlight_view.get():
                    self.syntax_highlight()
                self.saved=True
            except:
                tkMessageBox.showerror("Unable to open file","Unable to open file")
    
    def update_keywords(self,filename):
        try:
            self.keywords=self.languages[os.path.splitext(filename)[1].lower()[1:]]["keywords"]
        except:
            self.keywords=[]
        
    def save_file(self,event=None):
        if self.filename=="":
            return self.save_file_as()
        else:
            #try
            file_descriptor=open(self.filename,"w")
            file_descriptor.write(self.main_text.get(1.0, 'end-1c'))
            file_descriptor.close()
            self.saved=True
            def change_title():
                self.title(self.name+" - "+self.filename)
            self.after(250,change_title) #You need to add delay before changing title.
            return True
            """
            except:
                tkMessageBox.showerror("Unable to save","Unable to Save")
                return False
            """

    def save_file_as(self):
        file_options = {}
        file_options["defaultextension"] = ".txt"
        file_options["filetypes"]=[(value["name"],"."+key)  for key, value in self.languages.iteritems()]
        file_options["initialdir"] = os.getcwd()
        file_options['title'] = "Save file"
        filename=tkFileDialog.asksaveasfilename(**file_options)
        if filename!=() and filename!="":
            try:
                file_descriptor=open(filename,"w")
                file_descriptor.write(self.main_text.get("1.0", 'end-1c'))
                file_descriptor.close()
                if self.filename=="":
                    self.update_keywords(filename)
                    self.filename=filename
                    self.title(self.name+" - "+self.filename)
                    self.saved=True
                return True
            except:
                tkMessageBox.showerror("Unable to save","Unable to Save")
                return False
        else:
            return False

    def selectall(self, event):
        event.widget.tag_add("sel","1.0","end")

    def copy_selection(self,event=None):
        pass
        
    def paste_selection(self,event=None):
        try:
            text=self.main_text.selection_get(selection="CLIPBOARD")
            index=self.main_text.index("insert linestart")
            self.main_text.insert("insert",text)
            indexend=self.main_text.index("insert lineend")
            if self.highlight_view.get():
                self.syntax_highlight(None,index,indexend)
            return "break"
        except:
            pass #These are for TCl errors.
        
    def cut_selection(self,event=None):
        pass
        
    def undo_action(self):
        try:
            self.main_text.edit_undo()
        except:
            pass

    def redo_action(self):
        try:
            self.main_text.edit_redo()
        except:
            pass

    def about(self,event=None):
        tkMessageBox.showinfo(title="About",message="A cross-platform text-editor written in Python.\n\nDeveloper:Gnik Droy\ngnikdroy@gmail.com\n\nAll Rights Reserved.")

    def no_of_lines(self):
        return str(self.main_text.index("insert")).split(".")[0]

    def no_of_col(self):
        return str(self.main_text.index("insert")).split(".")[1]

    def footer_update(self,event=None):
        if self.saved:
            self.title("*"+self.name+" - "+self.filename)
        self.saved=False
        
        if len(self.filename)<=80:
            self.footer_text.set(self.filename+"\t\t\tLine: "+self.no_of_lines()+"\t"+"Col: "+self.no_of_col())
        else:
            tmp_filename="..."+self.filename[len(self.filename)-80:len(self.filename)]
            self.footer_text.set(tmp_filename+"\t\t\tLine: "+self.no_of_lines()+"\t"+"Col: "+self.no_of_col())

    def highlight_current_line(self):

        def delay():
            self.main_text.tag_remove("currentLine",1.0,"end")
            #Don't highlight current line while text is being selected
            self.main_text.tag_add("currentLine","insert linestart","insert lineend+1c")
            self.main_text.tag_lower("currentLine","sel")
        self.after(10,delay)

    def highlight_pattern(self,pattern, tag, start="1.0", end="end",
                          regexp=False):
        start = self.main_text.index(start)
        end = self.main_text.index(end)
        self.main_text.mark_set("searchLimit", end)
        count = tk.IntVar()
        index=start
        while True:
            index = self.main_text.search(pattern, "%s+%sc" % (index, count.get()),"searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.main_text.tag_remove("comment",index,"%s+%sc" % (index, count.get()))
            self.main_text.tag_add(tag, index, "%s+%sc" % (index, count.get()))
        self.main_text.mark_unset("searchLimit",end)

    def syntax_highlight(self,event=None,hstart=None,hend=None):
        if self.actively_highlighting:
            return
        self.actively_highlighting=True
        start="1.0"
        end="end"
        linestart="insert linestart"
        lineend="insert lineend+1c"
        if event==None:
            linestart="1.0"
            lineend="end"
        if not hstart==None:
            linestart=hstart
        if not hend==None:
            lineend=hend
        
        self.main_text.tag_remove("keyword",linestart,lineend)
        self.main_text.tag_remove("symbol",linestart,lineend)
        self.main_text.tag_remove("number",linestart,lineend)
        self.main_text.tag_remove("string",start,end)
        self.main_text.tag_remove("comment",linestart,lineend)

        parsers=[["keyword",r"\y(?:"+"|".join(self.keywords)+r")\y",linestart,lineend],
                 ["symbol",'[\+\-!@$%^&*\(\)\{\}/\[\]:;<>,\./\?\\=_\|~`]',linestart,lineend],
                 ["number",r"[?:0-9]",linestart,lineend],
                 ["comment","(?:#.*[^\"\'])",linestart,lineend],
                 ["string","(?:\".+?\")","1.0","end"],
                 ["string","(?:'.+?')","1.0","end"],
                 ["string","(?:\"\"\".*?\"\"\")","1.0","end"],
                 ["string","(?:'''.*?''')","1.0","end"]
                 ]
        for parser in parsers:
            self.highlight_pattern(parser[1],parser[0],parser[2],parser[3],regexp=True)
        self.actively_highlighting=False
        
    def exit_editor(self,event=None):
        if self.saved==True:
            self.destroy()
        else:
            choice=tkMessageBox.askquestion("Exit?","Save file before exit?",type=tkMessageBox.YESNOCANCEL,default=tkMessageBox.CANCEL)
            if choice=="yes":
                if self.save_file():
                    self.destroy()
            elif choice=="no":
                self.destroy()
            else:
                return 

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.linenumberfont=tkFont.Font(family="Helvetica", size=10, weight="normal")
        self.linenumbercol=self.linenumberfont.measure("0")
    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            x=50-self.linenumbercol*(len(linenum)+1)
            self.create_text(x,y,anchor="nw", text=linenum,fill="white",font=('Helvetica', '10'))
            i = self.textwidget.index("%s+1line" % i)


if __name__=="__main__":
    application = Editor()
    application.minsize(200,100)
    application.title("Py Notepad - Untitled")
    application.config(bg="#313131")
    application.mainloop()
