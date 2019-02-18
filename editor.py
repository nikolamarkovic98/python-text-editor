from Tkinter import *
import tkFileDialog
import os
import ctypes

class Editor:
    def __init__(self, main_window, text_box, menubar, providedFile=None):
        # editor file object, keeps track of open file
        self.f = {
            '_file': None,
            'filename': 'Untitled',
            'load_text': ''
        }

        self.main_window = main_window
        self.text_box = text_box
        self.menubar = menubar
        self.providedFile = providedFile
        self.initMenuAndStuff()
        
        # i open files in reading mode, when saving I close them and open file for writing
        if providedFile != None:
            self.f['_file'] = open(providedFile, 'r')
            self.f['filename'] = self.f['_file'].name
            self.f['load_text'] = self.f['_file'].read()

        # load text and set title of main_window
        self.text_box.insert('1.0', self.f['load_text'])
        self.main_window.title(self.f['filename'] + ' - Harmor')
        
        self.main_window.mainloop()

    def openFile(self):
        # when opening file I should actually first check if there isnt like already opened
        # file, and if there is, close it and then open a new one
        file_path = tkFileDialog.askopenfilename()
        if file_path != ():
            self.f['_file'] = open(file_path, 'r')
            self.f['filename'] = self.f['_file'].name
            self.f['load_text'] = self.f['_file'].read()
            self.text_box.insert('1.0', self.f['load_text'])
            self.main_window.title(self.f['filename'] + ' - Harmor')

    def saveNewFileOnX(self, window):
        # this function is called when saving a new file
        file_path = tkFileDialog.asksaveasfilename()
        if file_path != ():
            self.f['_file'] = open(file_path, 'w')
            self.f['_file'].write(self.text_box.get('1.0', 'end-1c'))
            self.f['_file'].close()
            self.closeWindows(window)

    def saveProvidedFileOnX(self, window):
        # function we are going to save file with if the file was provided
        self.f['_file'].close()
        self.f['_file'] = open(self.providedFile, 'w')
        self.f['_file'].write(self.text_box.get('1.0', 'end-1c'))
        self.f['_file'].close()
        self.closeWindows(window)

    def saveFile(self):
        if self.f['_file'] != None:
            file_path = self.f['_file'].name
            self.f['_file'].close()
            self.f['_file'] = open(file_path, 'w')
            self.f['load_text'] = self.text_box.get('1.0', 'end-1c')
            self.f['_file'].write(self.text_box.get('1.0', 'end-1c'))
        else:
            self.saveFileAs()

    def saveFileAs(self):
        file_path = tkFileDialog.asksaveasfilename()
        if file_path != ():
            if self.providedFile != None:
                self.f['_file'].close()
            self.f['_file'] = open(file_path, 'w')
            self.f['filename'] = self.f['_file'].name
            self.f['_file'].write(self.text_box.get('1.0', 'end-1c'))
            self.f['load_text'] = self.text_box.get('1.0', 'end-1c')
            self.main_window.title(self.f['filename'] + ' - Harmor')

    def askForSaveAndClose(self):
        window = Tk()
        window.title('Harmor')
        Label(window, text='Do you want to save changes to file?').grid(row=0, columnspan=3)
        if self.providedFile != None:
            Button(window, text='Save', command=lambda: self.saveProvidedFileOnX(window)).grid(row=1, column=2)
        else:
            Button(window, text='Save', command=lambda: self.saveNewFileOnX(window)).grid(row=1, column=2)
        Button(window, text='Don\'t save', command=lambda: self.closeWindows(window)).grid(row=1, column=0)
        Button(window, text='Cancel', command=window.destroy).grid(row=1, column=1)

    def closeWindows(self, window):
        # just close all the windows
        window.destroy()
        self.main_window.destroy()

    def newFile(self):
        # pretty much just clears text_box
        if(self.text_box.get('1.0', 'end-1c') == self.f['load_text']):
            self.text_box.delete('1.0', 'end')
            # reset editor's file object
            self.f['_file'] = None
            self.f['filename'] = 'Untitled'
            self.f['load_text'] = ''
            self.text_box.insert('1.0', self.f['load_text'])
            self.main_window.title(self.f['filename'] + ' - Harmor')
        else:
            window = Tk()
            window.title('Harmor')
            Label(window, text='Do you want to save changes to file?').grid(row=0, columnspan=3)
            if self.providedFile != None:
                Button(window, text='Save', command=lambda: self.saveProvidedFileOnX(window)).grid(row=1, column=2)
            else:
                Button(window, text='Save', command=lambda: self.saveNewFileOnX(window)).grid(row=1, column=2)
            Button(window, text='Don\'t save', command=lambda: self.closeWindows(window)).grid(row=1, column=0)
            Button(window, text='Cancel', command=window.destroy).grid(row=1, column=1)

    def initMenuAndStuff(self):
        self.main_window.protocol('WM_DELETE_WINDOW', self.closeEditor)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label='New File', command=self.newFile)
        filemenu.add_separator()
        filemenu.add_command(label='Open File', command=self.openFile)
        filemenu.add_separator()
        filemenu.add_command(label='Save As', command=self.saveFileAs)
        filemenu.add_command(label='Save', command=self.saveFile)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.closeEditor)
        self.menubar.add_cascade(label='File', menu=filemenu)

    def closeEditor(self):
        # if the text is same as original text, just close the program, if not ask for saving
        # by default tkinter text widget has \n at the end
        if(self.text_box.get('1.0', 'end-1c') == self.f['load_text']):
            self.main_window.destroy()
        else:
            self.askForSaveAndClose()

main_window = Tk()
menubar = Menu(main_window, cursor='clock')
main_window.config(menu=menubar)
text_box = Text(main_window, width=80, height=32)
text_box.pack(fill='both', expand=True)

# so if the second argument is provided (os.sys.argv) 
# i will assume it is a text file and try to open it in constructor

if len(os.sys.argv) == 2:
    editor = Editor(main_window, text_box, menubar, os.sys.argv[1])
else:
    editor = Editor(main_window, text_box, menubar)