# Import key libraries
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser

showStatusbar=True
showToolbar=True
fontFamily="Arial"
fontSize=12
textChanged = False
url = ""

# Class for main menu
class MainMenu(Menu):
    def __init__(self, parent, *args, **kwargs):
        Menu.__init__(self, parent, *args, **kwargs)
        self.parent=parent

        ############## File Menu #################
        self.new_icon=PhotoImage(file='icons/new.png')
        self.open_icon=PhotoImage(file='icons/open.png')
        self.save_icon=PhotoImage(file='icons/save_icon.png')
        self.exit_icon=PhotoImage(file='icons/exit.png')


        self.file = Menu(self, tearoff=0)
        self.file.add_command(label='New', image=self.new_icon, compound=LEFT, accelerator="Ctrl+N", command=self.parent.newFile) #
        self.file.add_command(label='Open', image=self.open_icon, compound=LEFT, accelerator="Ctrl+O") #
        self.file.add_command(label='Save', image=self.save_icon, compound=LEFT, accelerator="Ctrl+S")
        self.file.add_command(label='Save as', accelerator="Ctrl+Alt+S")
        self.file.add_command(label='Exit', image=self.exit_icon, compound=LEFT) # accelerator="Ctrl+O"

        ############## Edit Menu #################
        self.edit=Menu(self, tearoff=0)
        self.edit.add_command(label='Copy',accelerator="Ctrl+C")
        self.edit.add_command(label='Paste',accelerator="Ctrl+V")
        self.edit.add_command(label='Cut',accelerator="Ctrl+X")
        self.edit.add_command(label='Clear All',accelerator="Ctrl+Alt+C")
        self.edit.add_command(label='Find',accelerator="Ctrl+F")

        ############## View Menu #################
        global showStatusbar
        global showToolbar
        self.view=Menu(self, tearoff=0)
        self.view.add_checkbutton(onvalue=True, offvalue=False, label="Tool Bar", variable=showToolbar)
        self.view.add_checkbutton(onvalue=True, offvalue=False, label="Status Bar", variable=showStatusbar)

        ############## Theme Menu #################
        self.themes=Menu(self, tearoff=0)
        self.color_list = {
            'Default':'#000000.#FFFFFF', # first one is font color and second one is background color
            'Tomato':'#ffff00.#ff6347',
            'LimeGreen':'#fffff0.#32cd32',
            'Magenta':'#fffafa.#ff00ff',
            'RoyalBlue':'#ffffbb.#4169e1',
            'MediumBlue':'#d1e7e0.#0000cd',
            'Dracula':'#ffffff.#000000'
        }

        self.theme_choice=StringVar()
        for i in sorted(self.color_list):
            self.themes.add_radiobutton(label=i, variable=self.theme_choice)

        #### Create Menu
        self.add_cascade(label='File', menu=self.file)
        self.add_cascade(label='Edit', menu=self.edit)
        self.add_cascade(label='View', menu=self.view)
        self.add_cascade(label='Templates', menu=self.themes)

# Class for Text editor
class TextEditor(Text):
    def __init__(self, parent, *args, **kwargs):
        Text.__init__(self, parent, *args, **kwargs)
        self.parent=parent
        self.config(wrap='word')
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=FLAT)
        xscrollbar=Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        yscrollbar=Scrollbar(self, orient=VERTICAL)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar.config(command=self.xview)
        yscrollbar.config(command=self.yview)

# Class for status bar
class StatusBar(Label):
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=BOTTOM)
        self.config(text='Status Bar')

# Class for tool bar
class ToolBar(Label):
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=TOP, fill=X)

        #################################################################
        # Combo Box for font size
        self.cbFont=ttk.Combobox(self)
        self.cbFont.pack(side=LEFT, padx=(5, 10))

        # Combo Box for font size
        self.cbFontSize = ttk.Combobox(self)
        self.cbFontSize.pack(side=LEFT)

        ################################################################
        self.boldIcon = PhotoImage(file='icons/bold.png')
        btnBold = Button(self, image=self.boldIcon, command=self.parent.changeBold)
        btnBold.pack(side=LEFT, padx=5)

        ################################################################
        self.italicIcon = PhotoImage(file='icons/italic.png')
        btnItalic = Button(self, image=self.italicIcon, command=self.parent.changeItalic)
        btnItalic.pack(side=LEFT, padx=5)

        ################################################################
        self.underlineIcon = PhotoImage(file='icons/under_line.png')
        btnUnderline = Button(self, image=self.underlineIcon, command=self.parent.changeUnderline)
        btnUnderline.pack(side=LEFT, padx=5)

        ################################################################
        self.fontcolorIcon = PhotoImage(file='icons/color.png')
        btnfontColor = Button(self, image=self.fontcolorIcon, command=self.parent.changeFontColor)
        btnfontColor.pack(side=LEFT, padx=5)

        ################################################################
        self.alignLeftIcon = PhotoImage(file='icons/alignleft.png')
        btnalignLeft = Button(self, image=self.alignLeftIcon, command=self.parent.alignLeft)
        btnalignLeft.pack(side=LEFT, padx=5)

        ################################################################
        self.alignCenterIcon = PhotoImage(file='icons/aligncenter.png')
        btnalignCenter = Button(self, image=self.alignCenterIcon, command=self.parent.alignCenter)
        btnalignCenter.pack(side=LEFT, padx=5)

        ################################################################
        self.alignRightIcon = PhotoImage(file='icons/alignright.png')
        btnalignRight = Button(self, image=self.alignRightIcon, command=self.parent.alignRight)
        btnalignRight.pack(side=LEFT, padx=5)

        ################################################################

        fonts = font.families()
        fontList = []
        fontSizeList = []

        for i in range(8,80):
            fontSizeList.append(i)
        for i in fonts:
            fontList.append(i)

        self.fontVar = StringVar()
        self.cbFont.config(values=fontList, textvariable=self.fontVar)
        self.cbFont.current(0)
        self.cbFontSize.config(values=fontSizeList)
        self.cbFontSize.current(4)

        # Create a binding function for font combo box
        self.cbFont.bind(sequence="<<ComboboxSelected>>", func=self.parent.getFont)

        # Create a binding function for font size combo box
        self.cbFontSize.bind(sequence="<<ComboboxSelected>>", func=self.parent.getFontSize)



# Class for main application
class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent=parent
        self.pack(fill=BOTH, expand=True)

        # Create an instance of the menu
        self.main_menu = MainMenu(self)

        # Create an instance of tool bar
        self.toolbar = ToolBar(self)

        # Create an instance of text editor
        self.TextEditor=TextEditor(self)
        # Setting focus
        self.TextEditor.focus()

        # Create an instance of status bar
        self.statusbar = StatusBar(self)

        # Parent Menu Configuration
        self.parent.config(menu=self.main_menu)

        # Initialise font family and font size
        self.TextEditor.configure(font=('Arial 12'))

        # Binding function for text changed
        self.TextEditor.bind('<<Modified>>', self.changed)

    # Function - new file
    def newFile(self, *args):
        global url
        try:
            url=""
            self.TextEditor.delete(1.0, END)
        except:
            pass

    # Function - Text changed
    def changed(self, *args):
        global textChanged
        flag = self.TextEditor.edit_modified()
        textChanged = True
        print(flag)
        if flag:
            words=len(self.TextEditor.get(1.0, 'end-1c').split())
            letters=len(self.TextEditor.get(1.0, 'end-1c'))
            self.statusbar.config(text="Characters "+str(letters)+ " Words: " + str(words))

        self.TextEditor.edit_modified(False)

    # Function - To get font
    def getFont(self, *args):
        global fontFamily
        fontFamily = self.toolbar.cbFont.get()
        self.TextEditor.configure(font=(fontFamily, fontSize))
        # print('Font family - ', fontFamily)

    # Function - To get font size
    def getFontSize(self, *args):
        global fontSize
        fontSize = self.toolbar.cbFontSize.get()
        self.TextEditor.configure(font=(fontFamily, fontSize))
        # print('Font Size - ', fontSize)

    # Function - Make text bold
    def changeBold(self, *args):
        text_pro = font.Font(font=self.TextEditor['font'])
        print(text_pro.actual()['weight'])

        if text_pro.actual()['weight'] == 'normal':
            self.TextEditor.configure(font=(fontFamily, fontSize, 'bold'))
        elif text_pro.actual()['weight'] == 'bold':
            self.TextEditor.configure(font= (fontFamily, fontSize, 'normal'))

    # Function - Make Italic
    def changeItalic(self, *args):
        text_pro = font.Font(font=self.TextEditor['font'])
        print(text_pro.actual())

        if text_pro.actual()['slant'] == 'roman':
            self.TextEditor.configure(font=(fontFamily, fontSize, 'italic'))
        elif text_pro.actual()['slant'] == 'italic':
            self.TextEditor.configure(font= (fontFamily, fontSize, 'roman'))

    # Function - Make Underline
    def changeUnderline(self, *args):
        text_pro = font.Font(font=self.TextEditor['font'])
        print(text_pro.actual())

        if text_pro.actual()['underline'] == 0:
            self.TextEditor.configure(font=(fontFamily, fontSize, 'underline'))
        elif text_pro.actual()['underline'] == 1:
            self.TextEditor.configure(font= (fontFamily, fontSize, 'normal'))

    # Function - Change Font Color
    def changeFontColor(self, *args):
        color = colorchooser.askcolor()
        print(color)
        self.TextEditor.configure(fg=color[1])

    # Function - align left
    def alignLeft(self, *args):
        content = self.TextEditor.get(1.0, 'end')
        self.TextEditor.tag_config('left',justify=LEFT)
        self.TextEditor.delete(1.0, END)
        self.TextEditor.insert(INSERT, content, 'left')

    ## Function - align center
    def alignCenter(self, *args):
        content = self.TextEditor.get(1.0, 'end')
        self.TextEditor.tag_config('center',justify=CENTER)
        self.TextEditor.delete(1.0, END)
        self.TextEditor.insert(INSERT, content, 'center')

    ## Function - align right
    def alignRight(self, *args):
        content = self.TextEditor.get(1.0, 'end')
        self.TextEditor.tag_config('right',justify=RIGHT)
        self.TextEditor.delete(1.0, END)
        self.TextEditor.insert(INSERT, content, 'right')




if __name__ == "__main__":
    root=Tk()
    root.title("Text Editor")
    MainApplication(root).pack(side=TOP, fill=BOTH, expand=True)
    root.iconbitmap('icons/icon.ico')
    root.geometry("1250x850")
    root.mainloop()
