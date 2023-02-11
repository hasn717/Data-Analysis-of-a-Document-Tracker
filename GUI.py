import datetime
import json
import os

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog


from MainClass import MainClass


class GUI():
    """
    Class to handle all GUI related tasks and elements
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(
            "Data Analysis of a Document Tracker")
        self.args = dict()

        # File Dialog
        file_explore = tk.Button(
            self.root, text='Select JSON File', command=self.browse_files)
        file_explore.grid(row=0, column=0, columnspan=2,
                          padx=3, sticky=tk.NSEW)

        # Document UUID
        self.label = ttk.Label(self.root, text='Document UUID:')
        self.label.grid(row=1, column=0)
        self.document_id = tk.StringVar(name="Document UUID")
        self.document_entry = ttk.Entry(
            self.root, textvariable=self.document_id, width=30)
        self.document_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # User UUID
        self.label_user = ttk.Label(self.root, text='User UUID:')
        self.label_user.grid(row=2, column=0)
        self.user_id = tk.StringVar(name="User UUID")
        self.user_id_entry = ttk.Entry(
            self.root, textvariable=self.user_id, width=50)
        self.user_id_entry.grid(row=2, column=1, sticky=tk.NSEW)

        # center the window in the middle of the screen
        # Gets the requested values of the height and widht.
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        print("Width", windowWidth, "Height", windowHeight)

# Gets both half the screen width/height and window width/height
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.resizable(0, 0)

# Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        # Views By Country Button
        self.view_button_country = ttk.Button(
            self.root, text='Task 2a. Views By Country', command=self.view_country_button_clicked)
        self.view_button_country.grid(
            row=3, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # Views By Continent Button
        self.view_button_continent = ttk.Button(
            self.root, text='Task 2b. Views By Continent', command=self.view_continent_button_clicked)
        self.view_button_continent.grid(
            row=4, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # Views By User Agent
        self.view_useragent_button = ttk.Button(
            self.root, text='Task 3a. Views By User Agent', command=self.view_useragent_button_clicked)
        self.view_useragent_button.grid(
            row=5, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # Views By Browser Button
        self.view_browser_button = ttk.Button(
            self.root, text='Task 3b. Views By Browser', command=self.view_browser_button_clicked)
        self.view_browser_button.grid(
            row=6, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # View Top 10 Avid Readers Button
        self.top_readers_button = ttk.Button(
            self.root, text='Task 4. Top 10 Avid Readers', command=self.view_top_readers_button_clicked)
        self.top_readers_button.grid(
            row=7, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # View Top Documents
        self.top_documents_button = ttk.Button(
            self.root, text='Task 5d. Top 10 Documents', command=self.view_top_documents_button_clicked)
        self.top_documents_button.grid(
            row=8, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # View 'Also Likes' Graph
        self.also_likes_graph_button = ttk.Button(
            self.root, text='Task 6. "Also Likes" Graph', command=self.view_also_likes_button_clicked)
        self.also_likes_graph_button.grid(
            row=9, column=0, columnspan=2, padx=3, sticky=tk.NSEW)

        # Error/Warning Message
        self.message_label = ttk.Label(self.root, text='', foreground='red')
        self.message_label.grid(row=10, column=0, columnspan=2, sticky=tk.NSEW)
        self.exec = MainClass()

        self.root.mainloop()

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(5000, self.hide_message)
        self.document_entry['foreground'] = 'red'

    def hide_message(self):
        self.message_label['text'] = ''

    def validate_file_and_UUID(self):
        try:
            self.args['file_name']
        except:
            self.show_error("Enter JSON file")
            #messagebox.showwarning(title="Error", message="Enter JSON file!")
            return False
        if len(self.args) == 0:
            self.show_error("Enter JSON file")
            return False
        elif self.args['file_name'] == '':
            self.show_error("Enter a valid JSON file")
            return False
        if self.document_id.get() == '':
            self.show_error("Enter a Document UUID")
            return False
        else:
            return True

    def validate_file_User_DOC_UUID(self):
        try:
            self.args['file_name']
        except:
            self.show_error("Enter JSON file")
            return False
        if len(self.args) == 0:
            self.show_error("Enter JSON file")
            return False
        elif self.args['file_name'] == '':
            self.show_error("Enter a valid JSON file")
            return False
        elif self.document_id.get() == '':
            self.show_error("Enter a Document UUID")
            return False
        elif (self.user_id.get() == ''):
            self.show_error("Enter a User UUID")
            return False
        else:
            return True

    def validate_file(self):
        try:
            self.args['file_name']
        except:
            self.show_error("Enter JSON file")
            return False
        if len(self.args) == 0:
            self.show_error("Enter JSON file")
            return False
        elif self.args['file_name'] == '':
            self.show_error("Enter a valid JSON file")
            return False
        else:
            return True

    def view_country_button_clicked(self):
        if self.validate_file_and_UUID():
            try:
                self.args['document_uuid'] = self.document_id.get()
                self.args['task'] = '2a'
            # countriesReturned=list()
            # countriesReturned=self.viewsByCountry(self.args['document_uuid'])
            # if len(countriesReturned)>0:
                self.exec.runTasks(self.args)
                # except (KeyError, ValueError) as error:
            # else:
             #   self.show_error('UUID is not exist')
            except Exception as e:
                self.show_error(e)

    def view_continent_button_clicked(self):
        if self.validate_file_and_UUID():
            try:
                self.args['document_uuid'] = self.document_id.get()
                self.args['task'] = '2b'
                self.exec.runTasks(self.args)
       # except (KeyError, ValueError) as error:
            except Exception as e:
                self.show_error(e)

    def view_useragent_button_clicked(self):
        if self.validate_file():  # to validate the file input by the user
            try:
                self.args['task'] = '3a'
                self.exec.runTasks(self.args)
            except Exception as e:
                self.show_error(e)

    def view_browser_button_clicked(self):
        if self.validate_file():  # to validate the file input by the user
            try:
                self.args['task'] = '3b'
                self.exec.runTasks(self.args)
            except Exception as e:
                self.show_error(e)

    def view_top_readers_button_clicked(self):
        if self.validate_file():  # to validate the file input by the user
            try:
                self.args['task'] = '4'
                result = dict()
                for d in self.exec.viewTopAvidReaders():
                    result[d['visitor_uuid']] = datetime.datetime.fromtimestamp(
                        d['event_readtime'] / 1000).strftime('%H:%M:%S')
                self.view_listbox(result)
            except Exception as e:
                self.show_error(e)

    def view_listbox(self, readers_list):
        readers_window = tk.Tk()
        readers_window.title('Top 10 Readers (Descending)')
        columns = ('visitor_uuid', 'event_readtime')
        tree = ttk.Treeview(readers_window, columns=columns, show='headings')
        tree.heading('visitor_uuid', text='visitor_uuid')
        tree.heading('event_readtime', text='read time')

        for reader, readtime in readers_list.items():
            tree.insert('', tk.END, values=[reader, readtime])
        tree.grid(row=0, column=0, sticky='nsew')
        readers_window.mainloop()

    def view_top_documents_button_clicked(self):
        if self.validate_file_and_UUID():
            try:
                self.args['task'] = '5d'
                self.args['document_uuid'] = self.document_id.get()
                self.args['user_uuid'] = self.user_id.get()
                self.args['sorter'] = 'desc'
                result = dict()
                for k, v in self.exec.viewTopDocuments(self.args['document_uuid'], self.args['user_uuid'], self.args['sorter']).items():
                    result[k] = v
                self.view_top_documents_listbox(result)
            except Exception as e:
                self.show_error(e)

    def browse_files(self):
        direc = os.getcwd()
        filename = filedialog.askopenfilename(
            initialdir=direc, title='Select a File', filetypes=[("JSON Files", "*.json")])
        try:
            self.args['file_name'] = filename
            self.exec.records = self.exec.loadJSON(filename)
        except Exception as e:
            self.show_error(e)

    def view_top_documents_listbox(self, dic):
        documents_window = tk.Tk()
        documents_window.title('Top 10 Documents')

        columns = ('document_uuid', 'num_readers')
        tree = ttk.Treeview(documents_window, columns=columns, show='headings')
        tree.heading('document_uuid', text='Document UUID')
        tree.heading('num_readers', text='Number of Readers')

        for key, value in dic.items():
            tree.insert('', tk.END, values=(key, value))
        tree.grid(row=0, column=0, sticky='nsew')
        documents_window.mainloop()

    def view_also_likes_button_clicked(self):
        if self.validate_file_and_UUID():
            try:
                self.args['task'] = '6'
                self.args['document_uuid'] = self.document_id.get()
                self.args['user_uuid'] = self.user_id.get()
                self.exec.runTasks(self.args)
            except Exception as e:
                self.show_error(e.args[3])
