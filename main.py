import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox


# Definition of the main class of the application
class tkinterApp(tk.Tk):
   
    def __init__(self, *args, **kwargs):
       
        # Initialization of the main window
        tk.Tk.__init__(self, *args, **kwargs, )
        self.title("ClippingsCove")
        self.geometry("800x600")
        # X delete window
        self.protocol("WM_DELETE_WINDOW", self.on_quit) 
        # Makes the window not resizable
        self.resizable(width=False, height=False)  
        
        
        
        # Configuration of the button 
        style = ttk.Style()
        style.theme_use('default')
        style.configure('W.TButton',  font =('Arial', 16, 'normal'))
        style.map('W.TButton', background=[('active', '#FFE873'), ('!disabled', '#FFD43B')], 
                         foreground=[('active', '#646464'),])
        # Configuration of the button 
        style2 = ttk.Style()
        style2.configure('my.Label.TLabel', background="#306998",  font =('Arial', 14, 'normal'))
        style2.map('my.Label.TLabel',foreground=[('!disabled', 'white')])
        
        # Creation of the main container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Definition of the frames to be displayed in the application
        self.frames = {}
        for F in (StartPage, Add, Add_2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
       
        # Display of the initial frame
        self.show_frame(StartPage)
        
        # Creation of the text box for the title
        self.titolo_entry = tk.Entry()
    
    # Method to display a specific frame   
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   
    
    def on_quit(self):
        # Application closure
        if messagebox.askokcancel("Quit", "do you really want to close the application? "):
           self.destroy() 
        
          
        
        
        
# Define a new class "StartPage" that inherits from "tk.Frame"
class StartPage(tk.Frame):
    # Define the initialization method for the "StartPage" class
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Set the background color of the frame
        self.configure(bg="#306998") 
       
        # Status widget to display feedback on search and deletion operations
        statuslabel_frame = tk.Frame(self)
        statuslabel_frame.configure(bg="#306998")
        statuslabel_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.status_label = ttk.Label(statuslabel_frame, style="my.Label.TLabel", text="")
        self.status_label.pack(side="top", padx=5, pady=5)
        
        # Frame creation for the button
        button_frame = tk.Frame(self)
        button_frame.configure(bg="#306998")
        button_frame.pack(side="top", fill="y", padx=12)

        # Frame creation for the "Search" button
        search_frame = tk.Frame(button_frame)
        search_frame.pack(side="left", pady=5)

        # Label for the search box
        search_label = tk.Label(search_frame, text="Search:")
        search_label.configure(bg="#FFD43B", fg="#646464")
        search_label.pack(side="left", padx=5)

        # Input box for the search text
        self.cerca_entry = ttk.Entry(search_frame, width=12)
        self.cerca_entry.pack(side="left", padx=5)
        
        # Button to initiate search
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search)
        self.search_button.pack(side="right", pady=5)

        # Creating the frame for the "Delete" button
        delete_frame = tk.Frame(button_frame)
        delete_frame.pack(side="right", pady=5)

        # Label for delete box
        delete_label = tk.Label(delete_frame, text="Title to delete:")
        delete_label.configure(bg="#306998", fg="white")
        delete_label.pack(side="left", padx=5)

        # Input box for the title to be cleared
        self.titolo_entry = ttk.Entry(delete_frame, width=12)
        self.titolo_entry.pack(side="left", padx=5)

        # Button to delete the selected record
        delete_button = ttk.Button(delete_frame, text="Delete", command=self.elimina_record)
        delete_button.pack(side="right", pady=5)
        
        # Notes list widget
        note_db = tk.Frame(self)
        note_db.pack(side="top", fill="both", expand=True, padx=15, )
        
        # Text box to display the notes
        self.note_text = tk.Text(note_db, height=20, width=120)
        self.note_text.configure(font=("Arial", 12, "normal"), fg='#343541', bg='#F7F7F7' )
        self.note_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for the notes list
        scrollbar = ttk.Scrollbar(note_db, orient="vertical", command=self.note_text.yview)
        scrollbar.pack(side="right", fill="y")
        
       
        # Create a frame named "center_frame" with a blue background and place it at the bottom of the parent frame
        center_frame = tk.Frame(self, bg="black", bd=2, )
        center_frame.configure(bg="#306998")
        center_frame.pack(side="bottom",  fill="both", expand=True)
        
        # Create another empty frame named "left_frame" to the left of "center_frame" to move the "ENTER DATA" button to the left
        left_frame = tk.Frame(center_frame)
        left_frame.configure(bg="#306998")
        left_frame.pack(side="left", fill="both", expand=True)

        # Create another empty frame named "right_frame" to the right of "center_frame" to move the "UPDATE" button to the right
        right_frame = tk.Frame(center_frame)
        right_frame.configure(bg="#306998")
        right_frame.pack(side="right", fill="both", expand=True)

        # Create the "ENTER DATA" button inside "left_frame"
        add_button = ttk.Button(left_frame,style="W.TButton", text="Add note", command=lambda: controller.show_frame(Add))
        add_button.pack(side="left", padx=35, pady=5)
       
        # Create the "EDIT" button inside "center_frame"
        modify_button2 = ttk.Button(center_frame,style="W.TButton", text="Edit note",   command=lambda: controller.show_frame(Add_2))
        modify_button2.pack(side="left", padx=5, pady=5)
        
        # Create the "UPDATE" button inside "right_frame"
        update_button = ttk.Button(right_frame,style="W.TButton", text="Update list", command=self.refresh_notes_list)
        update_button.pack(side="right",  padx=50, pady=5)
        
       
        # Establish a connection to the database
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
         
        # Create the table "database" if it doesn't exist
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS database (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titolo TEXT,
                testo TEXT
            )
        """
        )
        
        # Define bold font tag
        
        # Retrieve all notes from the database and display them in the UI
        notes = self.c.execute("SELECT * FROM database ORDER BY id DESC").fetchall()
        
        if not notes:
            # If there are no notes in the database, display a message
            self.status_label.config(text="There are no notes.", )
        else:
            # If there are notes, display the number of notes found
            self.status_label.config(text=f"Found {len(notes)}notes in the database:")
        # Display each note in the UI    
        for nota in notes:
            #self.textbox.insert(tk.END, {nota[1]}, "bold")
            #self.note_text.insert(tk.END, f"Title: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[1]}\n", 'bold')
            #self.note_text.insert(tk.END, f"Testo: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[2]}\n\n")
            #self.note_text.insert(tk.END, f"Titolo: {nota[1]} - Testo: {nota[2]}\n") # ID: {nota[0]} - 

        # Update the list of notes in the UI
        self.refresh_notes_list()
    
    def refresh_notes_list(self):
        # Define bold font tag
        self.note_text.tag_configure('bold', font='calibri 16 bold')
        self.note_text.tag_configure('bold', font='calibri 16 bold')
        # Delete all notes currently displayed in the UI
        self.note_text.delete('1.0', tk.END)
    
        # Retrieve all notes from the database and display them in the UI
        self.c.execute("SELECT * FROM database ORDER BY id DESC")
        notes = self.c.fetchall()
        for nota in notes:
            #self.note_text.insert(tk.END, f"Title: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[1]}\n", 'bold')
            #self.note_text.insert(tk.END, f"Note: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[2]}\n\n")
        self.status_label.config(text=f"In the database there are {len(notes)} notes")    
    
    
    def elimina_record(self):
        # Get the title of the note to be deleted (.strip())
        titolo = self.titolo_entry.get().strip()
        # Check if a note with the given title exists in the database
        record = self.c.execute("SELECT * FROM database WHERE titolo=?", (titolo,)).fetchone()
        
        if record:
            # If the note exists, ask for confirmation before deleting it
            conferma = tk.messagebox.askyesno("Confirm elimination", f"Do you really want to delete the note '{titolo}' ?")
            # Method to delete a record from the database based on user confirmation
            if conferma:
                # Execute a DELETE SQL statement to delete the record with specified title
                self.c.execute("DELETE FROM database WHERE titolo=?", (titolo,))
                # Update the database with the changes
                self.conn.commit()
                # Display a message box to inform the user that the record has been deleted
                tk.messagebox.showinfo("Note deleted", f"the note '{titolo}' was deleted from the database.")
                # Clear the title entry widget
                self.titolo_entry.delete(0, tk.END)
        else:
            tk.messagebox.showerror("Note not found", f"There is no note with the title '{titolo}'.")
        # Refresh the notes list to display the updated records
        self.refresh_notes_list()
    
    
    # Method to search the database for records containing a specific text string
    def search(self):
        
         
        # Get the search text entered by the user
        search_text = self.cerca_entry.get().strip()
        
    
        # Check if the search field is empty
        if not search_text:
          # Display an error message and clear the notes area
          self.status_label.config(text="Enter the title or text of the note to be searched for")
          self.note_text.delete('1.0', tk.END)
          return
    
        # Execute a SELECT SQL statement using the LIKE operator to search for records that match the search text
        query = "SELECT * FROM database WHERE titolo LIKE ? OR testo LIKE ? ORDER BY id DESC"
        self.c.execute(query, (f"%{search_text}%", f"%{search_text}%"))
        result = self.c.fetchall()
        
        # Check for results
        if not result:
          self.status_label.config(text="No notes found")
          self.note_text.delete('1.0', tk.END)
          return
    
        # Update the note text with the search results
        self.note_text.delete('1.0', tk.END)
        for nota in result:
            self.note_text.insert(tk.END, f"Title: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[1]}\n", 'bold')
            self.note_text.insert(tk.END, f"Note: ", 'bold')
            self.note_text.insert(tk.END, f"{nota[2]}\n\n")
            #self.note_text.insert(tk.END, f"Titolo: {nota[1]} - Testo: {nota[2]}\n") # ID: {nota[0]} - 
        self.status_label.config(text=f"{len(result)} Notes found")
        # Clear the search entry after saving
        self.cerca_entry.delete(0, tk.END)
    
      
# Define a new class "Add" that inherits from "tk.Frame"
class Add(tk.Frame):
    
    # Define the initialization method for the "Add" class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        # Set the "controller" attribute of the class to the value passed as an argument
        self.controller = controller
        # Set the background color of the frame
        self.configure(bg="#306998")

        
        statuslabel_frame = tk.Frame(self)
        statuslabel_frame.configure(bg="#306998")
        statuslabel_frame.pack(side="top", fill="y", padx=10, pady=10)
        # Create the "Title" label and entry widgets
        self.titolo_label = ttk.Label(statuslabel_frame,style="my.Label.TLabel", text="Title :")
        self.titolo_label.pack(side="left", padx=5, pady=5)
        
        self.titolo_entry = ttk.Entry(statuslabel_frame, width=20)
        self.titolo_entry.pack(side="left", padx=5, pady=5)
       
        
        # Create the "text" label
        text_label = tk.Frame(self)
        text_label.configure(bg="#306998")
        text_label.pack(side="top", fill="y", padx=10, pady=10)
        
        self.testo_label = tk.Label(text_label, text="NOTE :")
        self.testo_label.configure(bg="#FFD43B")
        self.testo_label.pack(side="bottom",padx=5, pady=5 )
        
        note_db_add = tk.Frame(self)
        note_db_add.pack(side="top", fill="both", expand=True, padx=10, pady=10)
       
        self.testo_text = tk.Text(note_db_add, height=20, width=120)
        self.testo_text.configure(font=("Arial", 12, "normal"), fg='#343541', bg='#F7F7F7')
        self.testo_text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(note_db_add, orient="vertical", command=self.testo_text.yview)
        scrollbar.pack(side="right", fill="y")
        
        
        # Create an empty frame to align buttons in the center
        label = tk.Frame(self)
        label.configure(bg="#306998")
        label.pack(side="left", fill="x", padx=5, pady=5)
        
        
        # Create a frame to align buttons to the center
        center_frame = tk.Frame(self)
        center_frame.configure(bg="#306998")
        center_frame.pack(side="bottom", fill="both", expand=True)
        
        # Create an empty frame on the left of the center frame to move the "ENTER DATA" button to the left
        left_frame = tk.Frame(center_frame,)
        left_frame.configure(bg="#306998")
        left_frame.pack(side="left", fill="both", expand=True)

        # Create an empty frame on the right of the center frame to move the "UPDATE" button to the right
        right_frame = tk.Frame(center_frame)
        right_frame.configure(bg="#306998")
        right_frame.pack(side="right", fill="both", expand=True)

        # Create the "Save" button inside the left frame
        add_button = ttk.Button(left_frame, style="W.TButton", text="Save", command=self.add_note)
        add_button.pack(side="left",padx=25,pady=5)

        # Create the "HOME" button inside the right frame
        update_button = ttk.Button(right_frame,style="W.TButton", text="Home", command=lambda: controller.show_frame(StartPage))
        update_button.pack(side="right",  padx=50, pady=5)
   
        
    # Define a function to add a note to the database
    def add_note(self):
       
        # Get the title from the entry and the text from the text widget
        titolo = self.titolo_entry.get().strip()
        testo = self.testo_text.get("1.0", tk.END)
        
       
        # Check that both title and text are entered
        if not titolo and not testo:
           tk.messagebox.showerror("Error", "Title and text of the note are required.")
        elif not titolo:
            tk.messagebox.showerror("Error", "Title of the note is required.")
        elif not testo:
            tk.messagebox.showerror("Error", "Text of the note is required.")
        else:
         # Connect to the database
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor() 
     
         # Create the table if it doesn't exist already
            self.c.execute(
        """
        CREATE TABLE IF NOT EXISTS database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT,
            testo TEXT
        )
        """)
        
            # Execute the query to insert the note
            self.c.execute("INSERT INTO database (titolo, testo) VALUES (?, ?)", (titolo, testo))
        
            self.conn.commit()
    
            # Execute the query to select the notes ordered by descending id
            self.c.execute("SELECT * FROM database ORDER BY id DESC")
            database = self.c.fetchall()
    
            # Add the notes to the text widget on the main screen
            start_page_frame = self.controller.frames[StartPage]
            start_page_frame.note_text.delete("1.0", tk.END)
            for nota in database:
                #start_page_frame.note_text.insert(tk.END, f"Titolo: ", 'bold')
                start_page_frame.note_text.insert(tk.END, f"{nota[1]}\n", 'bold')
                #start_page_frame.note_text.insert(tk.END, f"Testo: ", 'bold')
                start_page_frame.note_text.insert(tk.END, f"{nota[2]}\n\n")
                #start_page_frame.note_text.insert(tk.END, f"Titolo: {nota[1]} - Testo: {nota[2]}\n") # ID: {nota[0]} -
                 
            # Show a success message
            tk.messagebox.showinfo("Success", "Note added successfully.")
            
            # Clear the text from the user interface fields: Entry 0, tk.END Text '1.0', tk.END
            self.titolo_entry.delete(0, tk.END )
            self.testo_text.delete('1.0', tk.END )
       
           
    
        
class Add_2(tk.Frame):

    def __init__(self, parent, controller):
        # Initialize the parent class
        tk.Frame.__init__(self, parent)
        # Store the controller object
        self.controller = controller
        # Set the background color
        self.configure(bg="#306998")
        
        
        
        # Create the "title", "text", "save" and "Home" buttons
        titolo_add_2 = tk.Frame(self)
        titolo_add_2.configure(bg="#306998")
        titolo_add_2.pack(side="top", fill="x", padx=5, pady=5)

        

        titolo_add2_label = tk.Label(titolo_add_2, text="Search by title:")
        titolo_add2_label.configure(bg="#FFD43B")
        titolo_add2_label.pack(side="top", padx=5, pady=8)
         
        # Create an input box to get the title of the note to search for
        self.titolo_add2_var = tk.StringVar()
        titolo_add2_entry = ttk.Entry(titolo_add_2, textvariable=self.titolo_add2_var,width=40 )
        titolo_add2_entry.pack(side="bottom", padx=10, pady=10)

        # Create a frame for the text input box and set its dimensions
        testo_frame2 = tk.Frame(self)
        testo_frame2.pack(side="top", fill="y", padx=5, pady=5)
        testo_add2_label = tk.Label(testo_frame2, text="Edit Note:")
        testo_add2_label.configure(bg="#FFD43B")
        testo_add2_label.pack(side="top")

        # Create a text input box to enter the note text and set its dimensions and styling
        text_db_add2 = tk.Frame(self)
        text_db_add2.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.text_add2 = tk.Text(text_db_add2, height=20, width=120)
        self.text_add2.configure(font=("Arial", 12, "normal"), fg='#343541', bg='#F7F7F7')
        self.text_add2.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(text_db_add2, orient="vertical", command=self.text_add2.yview)
        scrollbar.pack(side="right", fill="y")

        # Create a label and set its dimensions
        label = tk.Frame(self)
        label.configure(bg="#306998")
        label.pack(side="left", fill="x", padx=5, pady=5)
        
        # Create a center frame and set its dimensions
        center_frame = tk.Frame(self)
        center_frame.configure(bg="#306998")
        center_frame.pack(side="bottom", fill="both", expand=True)
        
        # Create a left frame and set its dimensions
        left_frame = tk.Frame(center_frame,)
        left_frame.configure(bg="#306998")
        left_frame.pack(side="left", fill="both", expand=True)

        # Create a right frame and set its dimensions
        right_frame = tk.Frame(center_frame)
        right_frame.configure(bg="#306998")
        right_frame.pack(side="right", fill="both", expand=True)

        # Create a "SAVE" button and set its dimensions and styling
        save_add2_button = ttk.Button(left_frame,style="W.TButton", text="Save", command=self.modify_data)
        save_add2_button.pack(side="left",padx=25,   pady=5)


        # Create a "HOME" button and set its dimensions and styling
        back_add2_button = ttk.Button( right_frame, style="W.TButton",text="Home", command=lambda: controller.show_frame(StartPage))
        back_add2_button.pack(side="right",padx=50, pady=5)
        
        
        # When user enters a title, display the text of the corresponding note
        self.titolo_add2_var.trace_add("write", self.show_text) 
    
    
    # Function to modify data in the database
    def modify_data(self):
        
        # Connect to the database
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        
        # Retrieve data from the database and store in a variable
        self.c.execute("SELECT * FROM database ORDER BY id DESC").fetchall()
        
        # Retrieve input values from the GUI
        titolo = self.titolo_add2_var.get().strip()
        testo = self.text_add2.get("1.0", tk.END)
        
        # Check if both input fields are not empty
        if titolo and testo:
           # Check if the title already exists in the database
           self.c.execute("SELECT * FROM database WHERE titolo = ?", (titolo,))
           result = self.c.fetchone()
           
           # If the title exists, ask for confirmation to edit it
           if result:
               confirm = messagebox.askyesno("Confirm", "Are you sure you want to edit this item?")
               # If confirmed, update the text and commit changes to the database
               if confirm:
                  self.c.execute("UPDATE database SET testo = ? WHERE titolo = ?", (testo, titolo))
                  self.conn.commit()
                  tk.messagebox.showinfo("Success", "Note successfully added.")
                  # Clear input fields after saving the record
                  self.titolo_add2_var.set("")
                  self.text_add2.delete("1.0", tk.END)
               else:
                   # If the record is not saved, update the status label with a message
                   self.status_add2_label.configure(text="Change cancelled", foreground="black")
           else:
                # If the title is not present in the database, display an error message
                tk.messagebox.showerror("Error","Title not present in the database")
                self.titolo_add2_var.set("")
                self.text_add2.delete('1.0', tk.END )
        else:
            # If any of the fields are empty, display an error message
            tk.messagebox.showerror("Error","ENTER ALL FIELDS ")
            
    # This function retrieves a record from the database based on the value of the title variable
    def show_text(self, *args ):
            
            titolo = self.titolo_add2_var.get()
            if titolo:
               # Connect to the database
               self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            # Execute a query to retrieve the record
            self.c.execute("SELECT * FROM database WHERE titolo= ?", (titolo,))
            result = self.c.fetchone()
            if result:
               # Clear the text box and insert the text from the record
               self.text_add2.delete("1.0", tk.END)
               self.text_add2.insert("1.0", result[2])
               
    
   
# Finally the end 
app = tkinterApp()
app.mainloop()






