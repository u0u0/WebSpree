#!/usr/bin/python
#-*-coding:utf-8*

#CSSWindows.py
#Role: Define the CSS specific tools in tkinter

#Walle Cyril
#08/05/2014

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


from tutorial import*
##DATA##
from file_extractor import*
##STYLES##
from tks_styles import*
##LOG##
#from log_writer import log_writer
##TOOLS##
from tk_tools import* #def create_context_menu
from tks_widgets_1 import DragDropFeedback, MainPlusHelp, HyperLink, next_gen, prev_gen

def _(l_string):
    #print("local language: "+l_string)
    return l_string

######this data will be exported in external json files soon
SELECTOR_LIST=[
    ["CSS1",[
          [", "],
          [" "],
          ["#id"],
          [".class"],
          [":link"],
          [":visited"]]],
     ["CSS2",[
          ["*"],
          [">"],
          ["+"]]]
     ]
GENERAL_PROPERTY_LIST_2={
    "color":[
               ["color",["color"]]
            ],
    "font":[
             ["font-size",["size"]],
             ["font-family",["font-family"]],
             ["font-weight",["font-weight","number"]]
             ],
    "margin":[
           ["margin",["size","auto"]],
           ["margin-top",["size","auto"]],
           ["margin-right",["size","auto"]],
           ["margin-bottom",["size","auto"]],
           ["margin-left",["size","auto"]]
           ],
    "padding":[
           ["padding",["size","auto"]],
           ["padding-top",["size","auto"]],
           ["padding-right",["size","auto"]],
           ["padding-bottom",["size","auto"]],
           ["padding-left",["size","auto"]],
           ]
    }


VALUE_LIST_2={
    "color":["green",
       "blue",
       "red"],
    "font-family":["Arial",
        "Verdana",
        "Sylfaen"],
    "font-weight":[
        "lighter",
        "normal",
        "bold"
        "bolder"],
    "auto":[
        "auto",
        ],
    "number":[
        "0-999",
        ],
    "size":[
        "em",
        "px",
        "%"]
    }
######this data will be exported in external json files soon

class CSSWindows(tk.Frame):
    """CSS  frame."""

    def __init__(self,parent,master_window,model):
        tk.Frame.__init__(self,parent)
        self.model=model
        self.master_window=master_window
        
        self.select_string=""
        self.property_values=[]
        self.autoclose_bracket=tk.BooleanVar(value=True)
        
        #select
        frame_select=tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[0])
        self.select_plus_help=MainPlusHelp(frame_select,_(u"Sélécteur"),_(u"Aide"))
        self.select_treeview_lift = ttk.Scrollbar(self.select_plus_help.main_frame)
        self.select_treeview=ttk.Treeview(self.select_plus_help.main_frame,selectmode='browse',\
                                            columns=("local","select"),height=21,cursor="hand2",\
                                             yscrollcommand=self.select_treeview_lift.set,padding=0,takefocus=True,\
                                             displaycolumns=(0,1),show='headings')
        self.select_plus_help.next_=next_gen(self.select_treeview)
        self.select_plus_help.previous=prev_gen(self.select_treeview)
        self.select_treeview.column("#0",width=20,stretch=False)
        self.select_treeview.heading("local",text=_(u"Traduction"))
        self.select_treeview.column("local",minwidth=100)
        self.select_treeview.heading("select",text=_(u"Code"))
        self.select_treeview.bind('<<TreeviewSelect>>',self.update_select_selection)
        self.select_treeview_lift.config(command=self.select_treeview.yview)
        #_List of elements:
        i=0
        tags=["tag_1","tag_2"]
        self.select_treeview.tag_configure("tag_1", background='#cccfff')
        self.select_treeview.tag_configure("tag_2", background='#cfffcc')
        self.select_treeview.tag_configure("tag_3", background='#ffccbc')
        
              
              
        function=self.select_treeview.insert("",'end',values=(_(u"Element"),""),tag=tags[0])
        for couple in ELEMENTS:
            for ele in couple[1]:
                self.select_treeview.insert(function,'end', \
                                                 values=(LOCAL_ELEMENTS[ele]["translation"],ele),tag="tag_3")
        for couple in SELECTOR_LIST:
            function=self.select_treeview.insert("",'end',values=(couple[0],""),tag=tags[0])
            for _o in couple[1]:
                o=_o[0]
                self.select_treeview.insert(function,'end', \
                                                 values=("",o),tag="tag_3")
        

        self.select_treeview.grid(row=0,column=0,columnspan=2,sticky='nsw')
        self.select_treeview_lift.grid(row=0,column=2,sticky='nsw')


        
        frame_property_master=tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[1])
        frame_value_master=tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[1])
        self.property_plus_help=MainPlusHelp(frame_property_master,_(u"Propriété"),_(u"Aide"))
        
        self.property_treeview=ttk.Treeview(self.property_plus_help.main_frame,selectmode='browse',\
                                        height=21,columns=("local","property"),displaycolumns=(0,1),show='headings')
        
        self.property_plus_help.next_=next_gen(self.property_treeview)
        self.property_plus_help.previous=prev_gen(self.property_treeview)
        self.property_treeview.heading("local",text=_(u"Traduction"))
        self.property_treeview.heading("property",text=_(u"Propriété"))
        self.property_treeview.grid(row=0,column=0,sticky='w')
        
        self.property_treeview.tag_configure("tag_1", background='#cccfff')
        self.property_treeview.tag_configure("tag_2", background='#cfffcc')
        self.property_treeview.tag_configure("tag_3", background='#ffccbc')
        
        for group in GENERAL_PROPERTY_LIST_2:
            #the first values should be a local
            function=self.property_treeview.insert("",'end',values=("",group),tag="tag_1")
            for prop in GENERAL_PROPERTY_LIST_2[group]:
                #prop[1] is a list of valid value types for that property
                self.property_treeview.insert(function,'end',values=("",prop[0]),tag="tag_3")
        self.property_treeview.bind('<<TreeviewSelect>>',self.update_property_selection,"")
        
        
        height_b=13
        self.values_plus_help=MainPlusHelp(frame_value_master,_(u"Valeur"),_(u"Aide"))
        self.value_treeview_lift = ttk.Scrollbar(self.values_plus_help.main_frame)
        self.value_treeview=ttk.Treeview(self.values_plus_help.main_frame,selectmode='browse',\
                                            columns=("local","value"),height=height_b,cursor="hand2",\
                                             yscrollcommand=self.value_treeview_lift.set,padding=0,takefocus=True,\
                                             displaycolumns=(0,1),show='headings')#,show='tree'.
        
        
        
        self.values_plus_help.next_=next_gen(self.value_treeview)
        self.values_plus_help.previous=prev_gen(self.value_treeview)
        self.values_plus_help.grid(column=1,row=1)
        self.value_treeview.column("#0",width=20,stretch=False)
        self.value_treeview.heading("local",text=_(u"Traduction"))
        self.value_treeview.column("local",minwidth=100)
        self.value_treeview.heading("value",text=_(u"Code"))
        self.value_treeview_lift.config(command=self.select_treeview.yview)
        self.value_treeview.grid(row=0,column=0)
        self.value_treeview.bind('<<TreeviewSelect>>',self.update_value_selection)        
        self.value_treeview_lift.grid(row=0,column=1)
        
        self.value_treeview.tag_configure("tag_1", background='#cccfff')
        self.value_treeview.tag_configure("tag_2", background='#cfffcc')
        self.value_treeview.tag_configure("tag_3", background='#ffccbc')
        
        for group in VALUE_LIST_2:
            #the first values should be a local
            function=self.value_treeview.insert("",'end',iid=group,values=("",group),tag="tag_1")
            for value in VALUE_LIST_2[group]:
                self.value_treeview.insert(function,'end',values=("",value),tag="tag_3")
        

        
        #user input and more
        frame_2_user_input=tk.Frame(self, FRAME_STYLE_2,bg=COLOURS_A[2])#Buttons et saisies
        help_label_for_content=ttk.Label(frame_2_user_input,text=_(u"Ecrivez une règle ici"))
        help_label_for_content.grid(row=0,column=0,sticky='nw')
        

        self.content_area_form=tk.Text(frame_2_user_input,ENTRY_STYLE,width=42,height=height_b)
        self.content_area_form.grid(row=1,column=0,sticky='nw',columnspan=3)
        self.content_area_form.bind('<Button-3>',create_context_menu)
        

        self.confirm_add_button=ttk.Button(frame_2_user_input, text=_(u"Confirmer"),command=self.confirm_write)
        self.confirm_add_button.grid(row=2,column=0,sticky='nw')
        self.delete_current_button=ttk.Button(frame_2_user_input, text=_(u"Effacer règle"),command=self.delete_current)
        self.delete_current_button.grid(row=2,column=1,sticky='nw')

        self.var_for_auto_close_checkbutton=tk.BooleanVar(value=True)
        self.auto_close_checkbutton=ttk.Checkbutton(frame_2_user_input, text=_(u"Auto Fermeture"),variable=self.var_for_auto_close_checkbutton)
        self.auto_close_checkbutton.grid(row=2,column=2,sticky='nw')
        

        #Help
        self.complete_help_select=ttk.Label(self.select_plus_help.help_frame, text=_(""),wrap=400)
        self.complete_help_select.grid(row=0,column=0,sticky='nswe')
        self.complete_help_property=ttk.Label(self.property_plus_help.help_frame, text=_(""),wrap=400)
        self.complete_help_property.grid(row=0,column=0,sticky='nswe')
        self.complete_help_value=ttk.Label(self.values_plus_help.help_frame, text=_(""),wrap=400)
        self.complete_help_value.grid(row=0,column=0,sticky='nswe')
        self.master_window._treeviews=self.master_window._treeviews+[self.select_treeview,self.property_treeview,self.value_treeview]
        #keep this do work around a ttk bug: growing treeviews
        
        #self.columnconfigure(0,weight=1)
        #self.rowconfigure(0,weight=1)
        
        frame_select.grid(row=0,column=0,sticky='nsw')
        frame_property_master.grid(row=0,column=1,sticky='nsw')
        frame_value_master.grid(row=1,column=1,sticky='nsw')
        frame_2_user_input.grid(row=1,column=0,columnspan=1,sticky='nsw')
        
        #self.grid_columnconfigure(0,weight=0)

    
                                
    
    def refresh_input(self):
        fresh_text="%s {\n" % (self.select_string)
        for property_, value in self.property_values:
            fresh_text+="  %s:%s\n" % (property_, value)#here we use always 2 space todo change as user wants
        
        if self.var_for_auto_close_checkbutton.get():
            fresh_text+="}"
        self.content_area_form.delete('1.0','end-1c')
        self.content_area_form.insert('end',fresh_text)
        
    def display_help_select(self,selector):
        self.complete_help_select['text']="put help here for %s" % (selector)

    def display_help_property(self,property_):
        self.complete_help_property['text']="put help here for %s" % (property_)

    def display_help_value(self,value):
        self.complete_help_value['text']=value
        
    def update_select_selection(self,*event):
        tree=self.select_treeview#tree calling this method
        selected_item_id=tree.selection()[0]
        if tree.get_children(selected_item_id):#folder of element
            tree.see(tree.get_children(selected_item_id)[0])
        else:
            e=(tree.item(selected_item_id,'value'))[1]
            tree.heading("select",text=_(u"Sélecteur: %s")%(e))
            self.select_string+=" "
            self.select_string+=e
            self.display_help_select(e)
            self.refresh_input()
            
    def update_property_selection(self,*event):#click
        tree=self.property_treeview#tree calling this method
        selected_item_id=tree.selection()[0]
        if tree.get_children(selected_item_id):#folder of element
            tree.see(tree.get_children(selected_item_id)[0])
        else:
            e=(tree.item(selected_item_id,'value'))[1]
            tree.heading("property",text=_(u"Propriété: %s")%(e))
            if not (any(e == items[0] for items in self.property_values)):
                #check if property is already there
                self.property_values.append([e,""])
            self.display_help_property(e)
            self.refresh_values()
            self.refresh_input()

    def refresh_values(self):
        tree=self.value_treeview
        #hide all
        top_level_items=tree.get_children()
        for iid in top_level_items:
            tree.detach(iid)

        #find the important ones
        only_properties=[]
        for property_,value in self.property_values:
            only_properties.append(property_)
        self.types_of_possible_values=[]
        for group in GENERAL_PROPERTY_LIST_2:
            for prop in GENERAL_PROPERTY_LIST_2[group]:
                #prop[1] is a list of valid value types for that property
                if prop[0] in only_properties:
                    self.types_of_possible_values.append(prop[1])
        
        #display them
        for _l in self.types_of_possible_values:
            for top_level_items in _l:
                tree.move(top_level_items,"",0)
            
    def update_value_selection(self,*event):
        tree=self.value_treeview#tree calling this method
        selected_item_id=tree.selection()[0]
        if tree.get_children(selected_item_id):#folder of element
            tree.see(tree.get_children(selected_item_id)[0])
        else:
            e=(tree.item(selected_item_id,'value'))[1]
            parent=tree.parent(selected_item_id)
            tree.heading("value",text=_(u"Valeur: %s")%(e))
            #create menu of selection to choose property the value should apply
            if not (self.property_values):#no property
                pass
            elif len(self.property_values)==1:
                self.property_values[0][1]=e
            else:
                only_properties=[]
                for property_,value in self.property_values:
                    only_properties.append(property_)
                for group in GENERAL_PROPERTY_LIST_2:
                    for prop in GENERAL_PROPERTY_LIST_2[group]:
                        #prop[1] is a list of valid value types for that property
                        if prop[0] in only_properties:
                            if parent in prop[1]:
                                print("good for",prop[0])
                
                #self.property_values.append([e,""])
            self.display_help_value(e)
            self.refresh_input()
    def for_which_property_dialog(self):
        pass


    def delete_current(self):
        self.content_area_form.delete('1.0','end-1c')
        self.select_string=""
        self.property_values=[]
        self.refresh_input()
        self.refresh_values()
        
    def confirm_write(self):
        #add
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        text_to_add=(self.content_area_form.get('1.0','end-1c'))
        current_object.add_to_text(text_to_add+"\n")
        self.master_window.tk_copy_text(current_object)
        #delete the added
        self.delete_current()

    #todo here put the cursor at the end of what is just added


    def save_file_to_test_control(self,*event):#Try with CTRL+Shift+T
        self.model.save_file_totest()
        
