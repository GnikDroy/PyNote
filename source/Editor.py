import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
from datetime import datetime

class Editor(tk.Tk):
	
	
	
	def __init__(self):
	
		#This function is necessary to start tk
		tk.Tk.__init__(self)
		
		#This is the keywords reserved for python (Used for highligting).
		self.word_list=['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','print']
		
		#This calls exit_editor when the cross button is pressed.
		self.protocol("WM_DELETE_WINDOW", self.exit_editor)
		
		#These are instance variables that are required for the program to run.
		self.filename=""
		self.saved=False
		
		#This calls selectall function when <control>+a is pressed.
		self.bind_class("Text","<Control-a>", self.selectall)	
		
		#This initializes all the gui elements
		self.initialize()
		self.footer_update()
		
		
		
		
	def initialize(self):
		self.create_menu()
		self.create_mainFrame()	
		self.render_mainFrame()
	
	
	def render_mainFrame(self):	
		
		#Call grid on all the contents to show in the gui
		
		self.main_text.grid(column=0,row=0,sticky="NSEW")
		self.main_scroll_bar.grid(column=1,row=0,sticky="NS")
		self.footer.grid(column=0,row=1,columnspan=2,sticky="E")
		self.grid_rowconfigure(0,weight=1)	
		self.grid_columnconfigure(0,weight=1)
		
		
		
		#Set focus to the main_text element.(The main white text box)
		
		self.main_text.focus_set()
	
	
	def create_menu(self):
		
		#Creating the Menu objects
		
		self.main_menu=tk.Menu(self)
		self.config(menu=self.main_menu) #This set the main_menu for the program as main_menu.
		self.file_menu=tk.Menu(self,tearoff=0)
		self.edit_menu=tk.Menu(self,tearoff=0)
		self.highlight_menu=tk.Menu(self,tearoff=0)
		self.tools_menu=tk.Menu(self,tearoff=0)
		self.help_menu=tk.Menu(self,tearoff=0)

		#For main menu
		
		self.main_menu.add_cascade(label="File", menu=self.file_menu)
		self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
		self.main_menu.add_cascade(label="Highlight", menu=self.highlight_menu)
		self.main_menu.add_cascade(label="Tools", menu=self.tools_menu)
		self.main_menu.add_cascade(label="Help", menu=self.help_menu)
				
		#For file menu
		
		self.file_menu.add_command(label="New",command=self.new_file,accelerator="Ctrl+N")
		self.file_menu.add_command(label="Open",command=self.open_file,accelerator="Ctrl+O")	
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Save",command=self.save_file,accelerator="Ctrl+S")
		self.file_menu.add_command(label="Save As",command=self.save_file_as)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Quit",command=self.exit_editor,accelerator="Ctrl+Q")
		
		
		
		#For edit menu
		
		self.edit_menu.add_command(label="Copy",command=self.copy_selection,accelerator="Ctrl+C")
		self.edit_menu.add_command(label="Cut",command=self.cut_selection,accelerator="Ctrl+X")
		self.edit_menu.add_command(label="Paste",command=self.paste_selection)
		self.edit_menu.add_command(label="Select All",command=lambda: self.main_text.tag_add("sel","1.0","end"),accelerator="Ctrl+A")
		self.edit_menu.add_separator()
		self.edit_menu.add_command(label="Undo",command=self.undo_action)
		self.edit_menu.add_command(label="Redo",command=self.redo_action,accelerator="Ctrl+Y")
		
		
		
		#For highlight menu
		
		self.highlight_menu.add_command(label="Highlight Syntax (.py)",command=self.syntax_highlight)
		
		
		
		#For tools menu
		
		self.tools_menu.add_command(label="Add Date/Time",command=lambda:self.main_text.insert("insert",str(datetime.now()).split(".")[0]))
		
		
		
		#For help menu
		
		self.help_menu.add_command(label="About",command=self.about)
		
		
		
		
	def create_mainFrame(self):
		#Magic numbers are present here
		
		self.main_text_height=40
		self.main_text_width=120
		
		
		
		#Declaring all string Vars here.
		
		self.footer_text=tk.StringVar()
		
		
		
		#Declaring all widget objects here
		
		self.main_text=tk.Text(self,height=self.main_text_height,width=self.main_text_width)
		self.main_scroll_bar=ttk.Scrollbar(self,command=self.main_text.yview)
		self.main_text.configure(yscrollcommand=self.main_scroll_bar.set,undo=True,maxundo=-1,autoseparators=True)
		self.main_text.config(maxundo=20,padx=5,pady=5)
		self.footer=ttk.Label(self,textvariable=self.footer_text)		
		
		
		#Set font tags here which will be later used to highlight the keywords.
		
		self.main_text.tag_config("keyword",foreground="blue")
		
		
		
		#Set the bindings here For shortcuts
		
		self.main_text.bind("<Control-s>",self.save_file)
		self.main_text.bind("<Control-o>",self.open_file)
		self.main_text.bind("<Control-n>",self.new_file)
		self.main_text.bind("<Control-q>",self.exit_editor)
		
		
		
		#This updates the line number and column number every time the cursor is moved.
		
		self.main_text.bind("<KeyRelease>",self.footer_update)
		self.main_text.bind("<ButtonRelease-1>",self.footer_update)
		
		
		
		#Setting the initial footer text here.
		
		self.footer_text.set("Line: 1\tCol: 0")	
			
		
		
		
		
	def new_file(self,event=None):
		if self.filename=="" and self.main_text.get("1.0", 'end-1c')=="":
			pass
		else:
			if tkMessageBox.askyesno("Save File?","Save current file?")==True:
				self.save_file()
			else:
				self.main_text.delete(1.0,tk.END)								
			
	def open_file(self,event=None):
		file_options = {}
		file_options["defaultextension"] = ".txt"
		file_options["filetypes"] = [("All Files", ".*"), ("Text Files", ".txt"),("Python Files",".py")]
		file_options["initialdir"] = "/"
		file_options['title'] = "Open File"
		filename=tkFileDialog.askopenfilename(**file_options)
		if filename!=() and filename!="" and filename!=None:
			try:
				self.filename=filename
				self.title="Editor -"+filename
				file_descriptor=open(filename)
				self.main_text.delete(1.0,tk.END)
				self.main_text.insert(1.0,file_descriptor.read())
				file_descriptor.close()
				self.saved=True
			except:
				tkMessageBox.showerror("Unable to open file","Unable to open file")
	
	def save_file(self,event=None):
		if self.filename=="":
			return self.save_file_as()
		else:
			try:
				self.saved=True
				file_descriptor=open(self.filename,"w")
				file_descriptor.write(self.main_text.get(1.0, 'end-1c'))
				file_descriptor.close()
				return True
			except:
				tkMessageBox.showerror("Unable to save","Unable to Save")
				return False
	
	def save_file_as(self):
		file_options = {}
		file_options["defaultextension"] = ".txt"
		file_options["filetypes"] = [("All Files", ".*"), ("Text Files", ".txt"),("Python Files",".py")]
		file_options["initialdir"] = "/"
		file_options['title'] = "Save file"
		filename=tkFileDialog.asksaveasfilename(**file_options)
		if filename!=() and filename!="":
			try:
				file_descriptor=open(filename,"w")
				file_descriptor.write(self.main_text.get("1.0", 'end-1c'))
				file_descriptor.close()
				if self.filename=="":
					self.filename=filename
					self.saved=True
				return True
			except :
				tkMessageBox.showerror("Unable to save","Unable to Save")
				return False
		else:
			return False
	
	def selectall(self, event):
		event.widget.tag_add("sel","1.0","end")

	def copy_selection(self,event=None):
		try:
			self.main_text.clipboard_clear()
			text=self.main_text.get("sel.first","sel.last")
			if text!="" and text!=None:
				self.main_text.clipboard_append(text)
		except:
			pass
				
	def paste_selection(self,event=None):
		try:
			text=self.main_text.selection_get(selection="CLIPBOARD")
			self.main_text.insert("insert",text)
		except:
			pass #These are for TCl errors.
			
	def cut_selection(self,event=None):
		try:
			self.copy_selection()
			self.main_text.delete("sel.first","sel.last")
		except:
			pass #This is for TCL errors.
			
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
	
	def about(self):
		tkMessageBox.showinfo(title="About",message="A cross-platform text-editor written in Python.\n\nDeveloper:Gnik Droy\ngnikdroy@gmail.com\n\nAll Rights Reserved.")

	def no_of_lines(self):
		return str(self.main_text.index("insert")).split(".")[0]
	
	def no_of_col(self):
		return str(self.main_text.index("insert")).split(".")[1]

	def footer_update(self,event=None):
		self.saved=False
		if len(self.filename)<=80:
			self.footer_text.set(self.filename+"\t\t\tLine: "+self.no_of_lines()+"\t"+"Col: "+self.no_of_col())
		else:
			tmp_filename="..."+self.filename[len(self.filename)-80:len(self.filename)]
			self.footer_text.set(tmp_filename+"\t\t\tLine: "+self.no_of_lines()+"\t"+"Col: "+self.no_of_col())

	def syntax_highlight(self,event=None):
		if event!=None:
			if str(event.char)!=" ":	#Only check after false so that it is faster 
				return False
				
		text=self.main_text.get(1.0, 'end-1c')
		self.main_text.delete(1.0,tk.END)
		sentences=text.split("\n")
		
		sentence_count=0
		for sentence in sentences:
			sentence_count+=1
			words=sentence.split(" ")
				
			word_count=0
			for word in words:
				word_count+=1
				if word in self.word_list:
					self.main_text.insert('end',word,("keyword"))
				else:
					self.main_text.insert('end',word)
				if word_count!=len(words):  #Don't insert a space if it is the last word.
					self.main_text.insert('end'," ")
			if sentence_count!=len(sentences): #Don't insert a new line if it is the last sentence.
				self.main_text.insert('end',"\n")
			
	def exit_editor(self,event=None):
		if self.saved==True:
			self.destroy()
		else:
			if tkMessageBox.askyesno("Exit?","Save file before exit?")==True:
				if self.save_file():
					self.destroy()
			else:
				self.destroy()
		
if __name__=="__main__":
	application = Editor()
	application.minsize(200,100)
	application.title("Editor")
	application.mainloop()
