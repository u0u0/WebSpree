#!/usr/bin/python
#-*-coding:utf-8*

#GraphicalUserInterfaceTk.py
#Role: define the class GraphicalUserInterfaceTk used for WebSpree

#Walle Cyril
#20/03/2014

##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##WebSpree
##Copyright (C) 2014 Walle Cyril
##
##WebSpree is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##WebSpree is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with WebSpree. If not, see <http://www.gnu.org/licenses/>.
##
##If you have questions concerning this license you may contact via email Walle Cyril
##by sending an email to the following adress:capocyril@hotmail.com
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import tkinter ...
try:#3.X
    import tkinter as tk
    import tkinter.ttk  as ttk
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
    import tkinter.font as tkfont
except ImportError:#2.X
    import Tkinter as tk
    import ttk as ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    import tkFont as tkfont

import webbrowser
import codecs
import os

##DATA##
from tutorial import detect_existing_tutorials,start_tutorial,verify
from file_extractor import*
##STYLES##
from tks_styles import*
##LOG##
from log_writer import log_writer
##Window##
from HTMLWindows import HTMLWindows
from CSSWindows import CSSWindows
##TOOLS##
from tks_widgets_1 import *


def _(l_string):
    #print("local language: "+l_string)
    return l_string
    

class GraphicalUserInterfaceTk(tk.Tk):
    """tkinter interface for WebSpree.

"""

#methods that changes something important --------------###############################
    
    def __init__(self,model):
        tk.Tk.__init__(self)
        self.model = model
        self.text_fields = []
        self.title(MAIN_TITLE)
        self.protocol("WM_DELETE_WINDOW", self.intercept_close)
        #self.attributes('-fullscreen', 1)#, '-topmost', 1)fullscreen #doesnt exist everywhere
        #self.geometry('1700x600+0+0')#static size is bad, it doesn t adapt
        self.configure(bd=1,bg=WINDOW_BACK_COLOR)
        self.iconbitmap(os.path.normpath(LOGO1_PATH))#problems here, icon should be insert when freezing the app not here
        bind_(self, all_=True, modifier="Control-plus", letter="", callback=self.change_size)
        bind_(self, all_=True, modifier="Control-minus", letter="", callback=self.change_size)
        bind_(self, all_=True, modifier="Control-0", letter="", callback=self.change_size)
        bind_(self, all_=True, modifier="Control", letter="w", callback=self.close_tab)
        bind_(self, all_=True, modifier="Control", letter="n", callback= self.prepare_new_file)
        bind_(self, all_=True, modifier="Control", letter="s", callback=self.model.save_html_file)
        bind_(self, all_=True, modifier="Control", letter="o", callback=self.edit_file_dialog)
        bind_(self, all_=True, modifier="Control", letter="f", callback=self.prepare_find_dialog)
        bind_(self, all_=True, modifier="Control", letter="g", callback=self.find_next)
        bind_(self, all_=True, modifier="Control", letter="h", callback=self.prepare_replace_dialog)
        bind_(self, all_=True, modifier="F3", letter="", callback=self.find_next)
        bind_(self, all_=True, modifier="Control-Shift", letter="t", callback=self.save_file_to_test_control)
        bind_(self, all_=True, modifier="Control-Shift", letter="s", callback=self._save_file_dialog)
        bind_(self, all_=True, modifier="Control-Shift", letter="a", callback=self.save_all)
        self.bind("<FocusIn>", self.app_got_focus)
        
        
        #image is ready for tkinter
        self.HTML5_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/HTML5_Badge_32.gif"))
        self.CSS3_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/CSS3_Badge_32.gif"))
        self.JS_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/js32.gif"))
        self.images = [self.HTML5_PHOTO_ICO, self.CSS3_PHOTO_ICO, self.JS_PHOTO_ICO]
        #self.plus_image = tk.PhotoImage(file=os.path.normpath("images/widgets/plus_1.gif"))
        
        self.general_frame = ttk.Frame(self,border=1)#this contains the common widgets e.g text editor
        self.special_frame = ttk.Frame(self,border=1)#this contains every specifiq widget,html,css,...

        self.general_frame.grid(row=0,column=0,sticky='nswe')
        self.special_frame.grid(row=0,column=1,sticky='nswe')
        
        self.current_font = tkfont.Font(family='helvetica', size=-15)
        mystyle = ttk.Style()
        mystyle.configure('.',font=self.current_font)

        #keep this do work around a ttk bug: growing treeviews
        self._treeviews = []
        self.adaptedwidth = int(float(self.winfo_screenwidth())/25.0)
        self.adapted_height = int(float(self.winfo_screenheight())/50.0)
        self.html_window = HTMLWindows(self.special_frame,self,model,self.adapted_height)#html frame
        self.css_window = CSSWindows(self.special_frame,self,model,self.adapted_height)#css frame
        self.js_window = tk.Frame(self.special_frame)#js frame
        self.t_frames = [self.html_window, self.css_window, self.js_window]
        
    


        tk.Label(self.js_window,text="coming pretty soon . really.").grid()
        
        
        
        content_frame = tk.Frame(self.general_frame, FRAME_STYLE_2,bg=COLOURS_A[3])
        self.html_text_tabs = ttk.Notebook(content_frame)
        self.html_text_tabs.grid(row=0,column=0,sticky='nsw',columnspan=2)
        self.html_text_tabs.bind('<<NotebookTabChanged>>',self.change_tab)
        
        
        
        self.mode = tk.IntVar(value=0)
        mode = tk.LabelFrame(self.special_frame, text=_("Mode d'édition"), relief='ridge', borderwidth=1,bg=WINDOW_BACK_COLOR)
        texts = ["HTML","CSS","JS"]
        for i in range(3):
            radiobutton_i = ttk.Radiobutton(mode,text=texts[i],image=self.images[i],compound='left',command=self.change_mod,variable=self.mode,value=i)
            radiobutton_i.grid(row=0,column=i)
        
        mode.grid(row=0,column=0,sticky='w')
        
        self.change_mod()
        
        self.insertion_tk_var = tk.BooleanVar(value=True)
        tools = tk.LabelFrame(content_frame, text=_("Outils"), relief='ridge', borderwidth=1,bg=WINDOW_BACK_COLOR)
        
        write_cursor_choice = ttk.Radiobutton(tools, text=_("Insérer au curseur"),variable=self.insertion_tk_var, value=True,command=self.switch_writing_place )
        write_cursor_choice.grid(row=0,column=0,sticky='nw')
        write_end_choice = ttk.Radiobutton(tools, text=_("Ecrire à la fin"),variable=self.insertion_tk_var, value=False, command=self.switch_writing_place)
        write_end_choice.grid(row=0,column=1,sticky='nw')
        report=HyperLink(tools,URL="https://github.com/GrosSacASac/WebSpree/issues/new",text="Feedback")
        report.grid(row=0,column=3,sticky='nw')
        tools.grid(row=1,column=0,sticky='nw')
        
        
        content_frame.grid(row=0,column=2,sticky='nsw',columnspan=1)
        self.tutorial_frame = tk.LabelFrame(tools, text=_("Tutoriel"), relief='ridge', borderwidth=1,bg="#d0c5e0")
        self.tutorial_check = ttk.Button(self.tutorial_frame, text="Check exercice", command=lambda:verify(self.model))
        self.tutorial_check.grid(row=0,column=0,sticky='')
        self.tutorial_leave = ttk.Button(self.tutorial_frame, text="Leave tutorial", command=lambda:self.lock_tutorial(False))
        self.tutorial_leave.grid(row=0,column=1,sticky='')
        
        if self.model.get_option("developper_interface"):
            future_search = tk.StringVar()
            search_global = ttk.Entry(self.special_frame,textvariable=future_search)
            future_search.set("Recherche pas encore possible")
            search_global.grid(row=0,column=1,sticky='ew')
            leave_button = ttk.Button(tools, text="Quit(instantly)",command=self._end )
            leave_button.grid(row=1,column=0,sticky='')
            test_button = ttk.Button(tools, text="Test",command=None )
            test_button.grid(row=1,column=1,sticky='')

        self.search_what = tk.StringVar(value="")
        self.replace_with = tk.StringVar(value="")
        self.find_or = tk.BooleanVar(value=True)
        self.paint_menus()
        
        #self.columnconfigure(0,weight=1)
        #self.rowconfigure(0,weight=1)
        
    def prepare_new_file(self,*event):#view
        self.Contexte = tk.Toplevel(self, bd=1, bg=WINDOW_BACK_COLOR)
        self.Contexte.title(_("Commencer"))
        self.Contexte.geometry('700x600+200+200')
        
        frame_title = tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Titre du document"))
        self.title_tk_var = tk.StringVar(value=self.model.get_option("last_html_document_title"))
        entry_1 = tk.Entry(frame_title,ENTRY_STYLE,textvariable=self.title_tk_var)
        entry_1.select_range(0, tk.END)#Select All
        entry_1.pack()
        entry_1.focus()

        
        self.new_doc_radiobutton_var = tk.IntVar(value=0)
        frame_where_to_start = tk.LabelFrame(self.Contexte, FRAME_STYLE, text=_("Document"))
        new_doc_radiobutton = ttk.Radiobutton(frame_where_to_start, text=_("Commencer un nouveau document standard"),value=0,variable=self.new_doc_radiobutton_var)
        new_doc_radiobutton.pack(anchor="w")
        new_blank_doc_radiobutton = ttk.Radiobutton(frame_where_to_start,text=_("Commencer un nouveau document vierge"), value=-1,variable=self.new_doc_radiobutton_var)
        new_blank_doc_radiobutton.pack(anchor="w")
        edit_doc_radiobutton = ttk.Radiobutton(frame_where_to_start, text=_("Modifier un document existant"),value=1,variable=self.new_doc_radiobutton_var)
        edit_doc_radiobutton.pack(anchor="w")
        
        #to do change this barbar method to control encoding properlyindex=self.model.selected_tab
        self._which_encoding_var = tk.StringVar(value="utf-8;utf-8")
        #value=self.model.current_text_html.get_encoding()+";"+self.model.current_text_html.get_w3c_encoding())
        frame_which_encoding=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Encodage(beta)"))
        for encotext,pyencodings,standardenco in ENCODINGS:
            encoding_radiobutton = ttk.Radiobutton(frame_which_encoding, text=encotext,value=pyencodings+";"+standardenco,variable=self._which_encoding_var)
            encoding_radiobutton.pack(anchor='w')

        self.indent_style_tk_var = tk.StringVar(value=self.model.get_option("indent_style"))
        self.indent_size_tk_var_2 = tk.IntVar(value=self.model.get_option("indent_size"))
        frame_indentation=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Indentation"))
        indent_style_radiobutton = ttk.Radiobutton(frame_indentation, text=_("Espaces"),value=" ",variable=self.indent_style_tk_var)
        indent_style_radiobutton.pack(anchor='w')
        indent_style_radiobutton2 = ttk.Radiobutton(frame_indentation, text=_("Tabulations"),value="\t",variable=self.indent_style_tk_var)
        indent_style_radiobutton2.pack(anchor='w')
        for i in [0,2,3,4,8]:
            indent_size_radiobutton = ttk.Radiobutton(frame_indentation, text=str(i),value=i,variable=self.indent_size_tk_var_2)
            indent_size_radiobutton.pack(anchor='w')

        frame_submit=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Valider"))
        accept_and_begin = ttk.Button(frame_submit, text=_("Confirmer[Entrée]"), command=self.confirm_new_file)
        accept_and_begin.grid(row=0,column=0)
        cancel = ttk.Button(frame_submit, text=_("Annuler[Escape]"), command=self.Contexte.destroy)
        cancel.grid(row=1,column=0)

        
        frame_title.grid(row=0,column=0,sticky='w')
        frame_where_to_start.grid(row=1,column=0,sticky='nswe')
        frame_which_encoding.grid(row=1,column=1,sticky='nswe')
        frame_indentation.grid(row=2,column=0,sticky='nswe')
        frame_submit.grid(row=2,column=1,sticky='nswe')

        
        soft_destruction(self,self.Contexte)

        
    def confirm_new_file(self,*event):#controller
        self.model.set_option("last_html_document_title",self.title_tk_var.get())
        self.model.set_option("indent_style",self.indent_style_tk_var.get())
        if self.indent_style_tk_var.get() == "\t":
            size = 1
            self.indent_size_tk_var.set(-1)
        else:
            size = self.indent_size_tk_var_2.get()
            self.indent_size_tk_var.set(size)
        self.model.set_option("indent_size",size)
            
        self.model.start_mod = self.new_doc_radiobutton_var.get()
        self.model._start_new_session()

        #this should be passe via start new session method-------
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        current_close_last = self.text_fields[tab_index][1]
        
        new_encoding_py , new_w3c_encoding = (self._which_encoding_var.get().split(";"))
        current_object.set_encoding(new_encoding_py)
        current_object.set_w3c_encoding(new_w3c_encoding)
        #this should be passe via start new session method-------
        
        if current_object.element_still_not_closed_list:
            current_close_last['state'] = 'normal'
        else:
            current_close_last['state'] = 'disabled'
        self.Contexte.destroy()
        
    def edit_file_dialog(self,*event):
        file_path = filedialog.askopenfilename(defaultextension = ".html",initialdir=self.model.guess_dir(),\
                                             filetypes = [("HyperText Mark-Up Language file", "*.html" ), ("All","*.*")])
        #to-do double check if the file exist here because it could have been deleted during the time the user chooses the file
        if file_path:
            self.model.edit_file(file_path)

    def _save_file_dialog(self,*event):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", initialdir=self.model.guess_dir(),\
                                                  filetypes=[("HyperText Mark-Up Language file", "*.html" ),\
                                                                   ("All","*.*")],\
                                                  initialfile=self.model.get_option("last_html_document_title"))
        
        return file_path and self.model._save_html_file_as(file_path)

    def save_file_to_test_control(self,*event):#Try with CTRL+Shift+T
        self.model.save_file_totest()
        
    def change_tab(self,*event):
        #mysteriously non functional# this has been fixed otherwise #comment out of date
        self.html_text_tabs.update_idletasks()
        self.model.selected_tab = self.html_text_tabs.index(self.html_text_tabs.select())
        

    def new_html_tab(self, tab_index, title):
        html_text_tab = tk.Frame(self.html_text_tabs)
        main_scrollbar  =  ttk.Scrollbar(html_text_tab)
        
        
        
        self.text_fields.append([tk.Text(html_text_tab,yscrollcommand = main_scrollbar.set,state='normal',width = self.adaptedwidth, height=((self.adapted_height * 2) - 3),undo=True),\
                                             ttk.Button(html_text_tab, text=_("Fermer la dernière balise ouverte"), command=self.confirm_close_element)])

        main_scrollbar.config(command=self.text_fields[tab_index][0].yview)
        self.text_fields[tab_index][0].grid(row=0,column=0,sticky='nsw')
        main_scrollbar.grid(row=0,column=1,sticky='ns')
        self.text_fields[tab_index][0].bind('<KeyRelease>', self.so_you_decided_to_write_html_directly)
        self.text_fields[tab_index][0].bind('<Button-3>',create_context_menu)
        self.text_fields[tab_index][0].bind('<ButtonRelease-1>',self.switch_writing_place)
        #self.text_fields[tab_index][0].bind('<Control-f>',lambda e:"break") this blocks what we want
        self.text_fields[tab_index][1].grid(row=1,column=0,sticky='nsw')
        self.text_fields[tab_index][1]['state']='disabled'
        #I = InformationBubble(parent=main_text_field,texte=_(u"éditer directement "))
        self.html_text_tabs.add(html_text_tab,text=title)
        self.html_text_tabs.select(tab_index)
        
    def tk_copy_text(self, text_to_copy, new=False):
        index = self.model.selected_tab
        if new:
            title = self.model.get_option("last_html_document_title")
            self.new_html_tab(index,title)
        current_widget = self.text_fields[index][0]
        current_widget.delete('1.0', 'end'+'-1c')
        current_widget.insert('end',text_to_copy)
        current_widget.yview("moveto","1.0")
        if new:
            current_widget.edit_reset()
            
    def close_tab(self,*event):
        def kill_tab(self,tab_index):
            del self.model.tabs_html[tab_index]
            del self.text_fields[tab_index]
            self.html_text_tabs.forget(tab_index)
            if len(self.model.tabs_html)>0:
                self.html_text_tabs.select(0)
                self.model.selected_tab = 0
            else:
#here is the way to let open at least 1 tab instead of closing the app
                self.model.start_mod = 2
                self.model._start_new_session()#open with a different name than last name used
        
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        if event[0] == "for_save":
            if not current_object.is_saved():
                answer = messagebox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de fermer l'onglet %s?" % (self.html_text_tabs.tab(tab_index,option='text'))))#True False ou None 
                if answer and not self.model.save_html_file():
                        return "cancel"
                elif answer is None:                                      # Cancel or X pressed
                    return "cancel"
            return "no_cancel"
        elif event[0]=="for_save_no_warning":
            if not current_object.is_saved() and not self.model.save_html_file():
                return "cancel"
            return "no_cancel"
        elif event[0]=="already_saved":
            kill_tab(self,tab_index,)
        else:#manual tab_closing
            try:
                if not current_object.is_saved():
                    answer = messagebox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de fermer cet onglet ?"))#True False ou None 
                    if answer:                                                      # Yes
                        if self.model.save_html_file():
                            kill_tab(self,tab_index)
                    elif answer is None: pass                                  # Cancel or X pressed
                    else :
                        kill_tab(self,tab_index)                             # Non
                else:
                    kill_tab(self,tab_index)
            except Exception:#caused when the windows creation process was interrupted because the
                #current_text_html.is_saved() attribute is created after the windows
                #solution: just le the user close the windows since nothing can be lost
                kill_tab(self,tab_index)
                
    
    def so_you_decided_to_write_html_directly(self,event):
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        current_text_field=self.text_fields[tab_index][0]
        self.switch_writing_place()
        if current_object.text!=current_text_field.get('1.0', 'end'+'-1c'):
            current_object.text = current_text_field.get('1.0', 'end'+'-1c')

    def confirm_close_element(self):
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        current_close_last = self.text_fields[tab_index][1]
        
        if current_object.element_still_not_closed_list:#there is something to close
            current_object.add_to_text(current_object.add_indent_and_line(current_object.close_element()))
            self.tk_copy_text(current_object)
        else:
            pass
        if current_object.element_still_not_closed_list:#there is still something to close
            pass
        else:
            current_close_last['state'] = 'disabled'
            
    def _start(self):
        if not self.model.get_option("license_accepted_and_read"):
            self.view_license(already_accepted=False)
            log_writer("width",self.winfo_screenwidth())
            log_writer("height",self.winfo_screenheight())
        
        
        self.mainloop()
        
    def _end(self):
        self.destroy()

    def save_all(self,*event):
        m = "for_save"
        if event:#called directly
            m = "for_save_no_warning"
        for tab_not_closed_index in range(len(self.model.tabs_html)-1,-1,-1):#we save all tabs or cancel
            self.html_text_tabs.select(tab_not_closed_index)
            self.model.selected_tab = tab_not_closed_index
            close_all = self.close_tab((m))
            if close_all=="cancel":
                return close_all
        return "no_cancel"
    
    def intercept_close(self):
        if self.save_all() != "cancel":
            path_list = []
            for tab_not_closed_index in range(len(self.model.tabs_html)-1,-1,-1):
                #we close all tabs and save the location for the next time
                if self.model.tabs_html[tab_not_closed_index].get_save_path():
                    path_list.insert(0,self.model.tabs_html[tab_not_closed_index].get_save_path())
                self.html_text_tabs.select(tab_not_closed_index)
                self.model.selected_tab = tab_not_closed_index
                self.close_tab(("already_saved"))
            self.model.set_option("previous_files_opened",path_list)
            self._end()
    
    def view_license(self,already_accepted = False):
        license_window = tk.Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
        license_window.title("LICENSE")
        LICENSE = codecs.open(os.path.normpath("LICENSE/LICENSE.txt"),'r','utf-8').read()
        license_text = tk.Text(license_window)
        license_text.grid(column=0,row=0)
        license_text.insert('end',LICENSE)
        
        LICENSE_NOTICE = codecs.open(os.path.normpath("LICENSE/notice_license.txt"),'r','utf-8').read()
        License_notice_text = tk.Text(license_window)
        License_notice_text.grid(column=1,row=0)
        License_notice_text.insert('end',LICENSE_NOTICE)
        license_window.lift(self)
        
        if not already_accepted:
            license_window.grab_set()
            license_window.focus_set()
            license_window.focus_force()#force focus
            def accept(self):
                self.model.set_option("license_accepted_and_read",True)
                license_window.destroy()

            def refuse(self):
                self.model.set_option("license_accepted_and_read",False)
                self._end()
            
            license_window.protocol("WM_DELETE_WINDOW", lambda:refuse(self))
            
            accept_button = tk.Button(license_window,text = _("Accepter"),command=lambda:accept(self))
            accept_button.grid(column=0,row=1)
            refuse_button = tk.Button(license_window,text=_("Refuser"),command=lambda:refuse(self))
            refuse_button.grid(column=0,row=2)
            
    def switch_writing_place(self,*event):#todo redesign this old thing
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        current_text_field = self.text_fields[tab_index][0]
        if self.insertion_tk_var.get():
            before_cursor_text = current_text_field.get('1.0', 'insert')
            current_object.insertion = len(before_cursor_text)
        else:
            current_object.insertion = None
            
    def change_size(self,event):
        try:
            equivalent = event.keysym#when zooms with keyboard
        except AttributeError:
            equivalent = event#zoom with something else (menu)

        for treeview in self._treeviews:
            treeview.column("local",width=200)
        if equivalent== '0':
            self.current_font['size'] = -15
        elif equivalent == 'plus':
            if self.current_font['size'] > -60:
                self.current_font['size'] -= 1
        elif equivalent == 'minus':
            if self.current_font['size'] < -7:
                self.current_font['size'] += 1
                
    def print_text_links(self, messages=[], links=[]):
        self.info = tk.Toplevel(self)
        for message in messages:
            ttk.Label(self.info,text=message).grid(sticky='w')
        for link in links:
            HyperLink(self.info,link[0],link[1]).grid(sticky='w')
        ttk.Button(self.info,text = _("Ok"),command=self.info.destroy).grid()
        soft_destruction(self,self.info)
        self.info.grid()
                
    def feedback_verification(self,messages,links,finished):
        if finished:
            self.lock_tutorial(False)
        self.print_text_links(messages,links)        
        
    def lock_tutorial(self, lock=True):
        if lock:
            state="disabled"
            self.tutorial_frame.grid(row=0,column=2,sticky='')
        else:
            state=tk.NORMAL
            self.tutorial_frame.grid_forget()
        self.Menus_tk.entryconfigure(self.tuto_label, state=state)
    
    def change_mod(self):
        for t_frame in self.t_frames:
            t_frame.grid_forget()
        self.t_frames[self.mode.get()].grid(row=1,column=0,sticky='we',columnspan=2)

    def set_indent_size(self):
        if self.indent_size_tk_var.get()== -1:
            self.model.set_option("indent_size",1)
            self.model.set_option("indent_style","\t")
        else:
            self.model.set_option("indent_size",self.indent_size_tk_var.get())
            self.model.set_option("indent_style"," ")

    def app_got_focus(self, event):
        pass
    
    def tk_index_from_plain(self,text, plain_index):
        if plain_index == -1:
            return "1.0"
        else:
            before = text[0:plain_index]
            lines = before.count("\n")
            columns = len(before.split("\n")[-1])
            tk_index = str(1 + lines) + "." + str(columns)
            return tk_index
    
    def prepare_find_dialog(self, *event):
        self.find_or.set(True)
        self.find_dialog('disabled')
    def prepare_replace_dialog(self, *event):
        self.find_or.set(False)
        self.find_dialog('normal')
    def find_dialog(self,state):
        self.search_dialog = tk.Toplevel(self, bd=1, bg=WINDOW_BACK_COLOR)
        
        search_string = _("Rechercher")
        replace_string = _("Remplacer")
        replace_radio = ttk.Radiobutton(self.search_dialog, text=replace_string,variable=self.find_or,value=False)
        find_radio = ttk.Radiobutton(self.search_dialog, text=search_string,variable=self.find_or,value=True)
        replace_entry = ttk.Entry(self.search_dialog, textvariable=self.replace_with,state=state)
        
        replace_radio.grid(column=1,row=0)
        find_radio.grid(column=0,row=0)
        
        label = ttk.Label(self.search_dialog, text=search_string)
        label.grid(column=0,row=1)
        label_2 = ttk.Label(self.search_dialog, text=replace_string)
        label_2.grid(column=0,row=2)
        replace_entry.grid(column=1,row=2)
        entry = ttk.Entry(self.search_dialog, textvariable=self.search_what)
        entry.focus()
        entry.select_range(0, tk.END)#Select All
        entry.grid(column=1,row=1)
        self.search_message = ttk.Label(self.search_dialog, text="")
        self.search_message.grid(column=0,row=3)

        soft_destruction(self,self.search_dialog)
        self.search_dialog.bind('<Return>', self.find_next)
        self.search_dialog.grid()
        return 'break'

    def find_next(self, *event):
        search_what = self.search_what.get()
        if search_what == "":
            return None
        tab_index = self.model.selected_tab
        current_object = self.model.tabs_html[tab_index]
        current_text_field = self.text_fields[tab_index][0]

        if self.find_or.get():
            where = current_object.find(search_what)
            print_message = ""
            if where == -1:
                #bottom reached
                print_message += _(u"Bas de page dépassé, recommence au début\n")
                where = current_object.find(search_what, start = 0)
                if where == -1:#still not found
                    print_message += _(u"Non trouvé !")
            if where != -1:
                tk_index = self.tk_index_from_plain(current_object.text, where)
                current_text_field.see(tk_index)
                current_text_field.mark_set(tk.INSERT, tk_index)
                #unselect all, then select the research pattern
                current_text_field.tag_remove(tk.SEL, "1.0", tk.END)
                current_text_field.tag_add(tk.SEL,
                    tk_index,
                    tk_index + "+{}c".format(len(search_what)))
                current_text_field.focus()
            else:
                if self.search_message.winfo_viewable():
                    self.search_message['text'] = print_message
        else:
            current_object.replace(search_what,self.replace_with.get(),1)
            self.tk_copy_text(current_object)
        
        
    def paint_menus(self):
        ######----Menus-----######
        FILEMENU = {}
        FILEMENU["name"] = _("Fichier")
        FILEMENU["command"] = [
             {'label':_("Nouveau [Ctrl+N]"),'command':self.prepare_new_file},\
             {'label':_("Ouvrir [Ctrl+O]"),'command':self.edit_file_dialog},\
             {'label':_("Enregistrer [Ctrl+S]"),'command':lambda: self.model.save_html_file()},\
             {'label':_("Enregistrer sous[Ctrl+Shift+S]"),'command':lambda: self._save_file_dialog()},\
             {'label':_("Enregistrer tout [Ctrl+Shift+A]"),'command':lambda: self.save_all("forced_arg")},\
             {'label':_("Essayer ! [Ctrl+Shift+T]"),'command':lambda: self.save_file_to_test_control()},\
             {'label':_("Fermer Onglet [Ctrl+W]"),'command':lambda: self.close_tab(("easy"))},\
             {'label':_("Quitter"),'command':lambda: self.intercept_close()}
        ]
        FILEMENU["radiobutton"] = []

        EDITMENU = {}
        EDITMENU["name"] = _("Edition")
        EDITMENU["command"] = [
            {'label':_("Recherche [Ctrl+F]"),'command':self.prepare_find_dialog},
            {'label':_("Recherche prochain [Ctrl+G]"),'command':self.find_next},
            {'label':_("Remplacer [Ctrl+H]"),'command':self.prepare_replace_dialog}
        ]
        EDITMENU["radiobutton"] = []
        
        VALIDATEMENU = {}
        VALIDATEMENU["name"] = _("Valider")
        VALIDATEMENU["command"] = [{'label':_("Valider HTML"),'command':lambda: self.print_text_links(self.model.validate_document())}]
        VALIDATEMENU["radiobutton"] = []

        VIEWMENU = {}
        VIEWMENU["name"] = _("Vue")
        VIEWMENU["command"] = [
             {'label':_("Pas de Zoom[Ctrl+0]"),'command':lambda: self.change_size("0")},\
             {'label':_("Zoom +[Ctrl+ +]"),'command':lambda: self.change_size("plus")},\
             {'label':_("Zoom -[Ctrl+ -]"),'command':lambda: self.change_size("minus")}
         ]
        VIEWMENU["radiobutton"] = []

        self.html_window.translate_html_level_tk_var = tk.IntVar(value=self.model.get_option("translate_html_level"))
        if self.model.get_option("indent_style")=="\t":
            self.indent_size_tk_var = tk.IntVar(value=-1)
        else:
            self.indent_size_tk_var = tk.IntVar(value=self.model.get_option("indent_size"))
        OPTIONMENU = {}
        OPTIONMENU["name"] = _("Options")
        OPTIONMENU["command"] = []
        trans = [[_(u"Remplacer tout caractère spécial"),10],
               [_(u"Remplacer le minimum"),1],
               [_(u"Remplacer aucun caractère spécial"),0]]
        OPTIONMENU["radiobutton"] = []
        for text_,value_ in trans:
            OPTIONMENU["radiobutton"].append(
                {'label':text_, 'command':self.html_window.set_translation,'value':value_,"variable":self.html_window.translate_html_level_tk_var})
        for size in [0,2,3,4,8]:
            OPTIONMENU["radiobutton"].append(
                {'label':_(u"Indenter avec {} espaces").format(size), 'command':self.set_indent_size,'value':size,"variable":self.indent_size_tk_var})
            
        
        #([{'label':_("Compact"),'command':self.change_mapping,'value':True,"variable":self.small_layout},
                                    #{'label':_("Etendu"),'command':self.change_mapping,'value':False,"variable":self.small_layout}])
        self.tuto_label = _("Tutoriel")
        TUTORIALMENU = {}
        TUTORIALMENU["name"] = self.tuto_label
        TUTORIALMENU["command"] = []
        tutorial_progress = self.model.get_option("tutorial_progress")
        score = 0
        for info, folder in detect_existing_tutorials():
            name = info["name"]
            if folder in tutorial_progress:
                if tutorial_progress[folder]["finished"]:
                    score += info["reward"]
                    color = "#46a717"#green
                    expl = _(" (tutoriel terminé)")
                else:
                    current = tutorial_progress[folder]["current"]
                    size = len(info["steps"])
                    score += int(float(current)/float(size) * float(info["reward"]))
                    color = "#e3b333"#yellow
                    expl = _(" (tutoriel en cours)")
            else:
                color = "#fefefe"#near white
                expl = ""
            TUTORIALMENU["command"].append({'label':name+expl,"bg":color,'command':lambda: start_tutorial(folder,self)})
        
        TUTORIALMENU["radiobutton"] = []
        
        HELPMENU = {}
        HELPMENU["name"] = _("Aide")
        HELPMENU["command"] = ([
                              {'label':_("Lisez_moi"),'command':lambda: webbrowser.open("Documentation\Lisez_moi.html",new=2)},
                              {'label':_("To-do"),'command':lambda: webbrowser.open("Documentation\To_do.html",new=2)},
                              {'label':_("Patch notes"),'command':lambda: webbrowser.open("Documentation\Patch_Notes.html",new=2)},
                              {'label':_("Version"),'command':lambda: webbrowser.open("Documentation\Version.html",new=2)},
                              {'label':_("LICENSE"),'command':lambda: self.view_license(already_accepted=True)}])
        HELPMENU["radiobutton"] = []
        
        SCOREMENU = {}
        SCOREMENU["name"] = _("Score: ") + str(score)
        SCOREMENU["command"] = []
        SCOREMENU["radiobutton"] = []
        #start file doesn t work on every platform use webbrowser
        ALL_MENUS = [FILEMENU,EDITMENU,VALIDATEMENU,VIEWMENU,
                     OPTIONMENU, TUTORIALMENU, SCOREMENU, HELPMENU]
        top = self.winfo_toplevel()#for macs menu to render as users are used to
        self.Menus_tk = tk.Menu(top)
        top['menu'] = self.Menus_tk
        sub_menu_list = []
        #All_MENU_ITEM_OPTION={'activebackground':"blue"}
        
        #This loop creates the menus described just before. from dicts to menus of menus
        for index,submenu in enumerate(ALL_MENUS):
            sub_menu_list.append(tk.Menu(self.Menus_tk,tearoff=0))#,tearoff=0 disables the popopable menu item with the dottet bar
            self.Menus_tk.add_cascade(label=submenu["name"], menu=sub_menu_list[index],underline=0)
            for command_ in submenu["command"]:
                if 'bg' in command_:
                    c = command_['bg']
                else:
                    c = "white"
                sub_menu_list[len(sub_menu_list)-1].add_command(label=command_["label"], command=command_["command"],background=c,activebackground="blue")
            for radiobutton_ in submenu["radiobutton"]:
                sub_menu_list[len(sub_menu_list)-1].add_radiobutton(label=radiobutton_["label"], command=radiobutton_["command"],\
                                                                    variable=radiobutton_["variable"],value=radiobutton_["value"],activebackground="blue")


        
        
        
