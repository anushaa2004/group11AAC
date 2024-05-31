#tkinter stuff
#made it so it's 4 boxes adjacent to each other per row
#conjugation based on pronoun

import tkinter as tk
from tkinter import messagebox
# import example2

# Variable to store user selections
selected_subject = None
selected_verb = None
selected_object = None

# Function to conjugate verbs based on the subject
def conjugate_verb(verb, subject):
    conjugations = {
        "To ask": {"I": "ask", "You": "ask", "He": "asks", "She": "asks", "We": "ask", "They": "ask"},
        "To be": {"I": "am", "You": "are", "He": "is", "She": "is", "We": "are", "They": "are"},
        "Can": {"I": "can", "You": "can", "He": "can", "She": "can", "We": "can", "They": "can"},
        "To come": {"I": "come", "You": "come", "He": "comes", "She": "comes", "We": "come", "They": "come"},
        "To do": {"I": "do", "You": "do", "He": "does", "She": "does", "We": "do", "They": "do"},
        "To have": {"I": "have", "You": "have", "He": "has", "She": "has", "We": "have", "They": "have"},
        "To feel": {"I": "feel", "You": "feel", "He": "feels", "She": "feels", "We": "feel", "They": "feel"},
        "To know": {"I": "know", "You": "know", "He": "knows", "She": "knows", "We": "know", "They": "know"},
        "To like": {"I": "like", "You": "like", "He": "likes", "She": "likes", "We": "like", "They": "like"},
        "To make": {"I": "make", "You": "make", "He": "makes", "She": "makes", "We": "make", "They": "make"},
    }
    return conjugations.get(verb, {}).get(subject, verb)

# Function to open a new window
def open_new_window(category):
    new_window = tk.Toplevel(root)  # Use Toplevel instead of Tk to create additional windows
    new_window.title(f"{category} Window")
    new_window.geometry('800x600')
    return new_window

# Function to handle the "Subject" category
def open_subject_window():
    new_window = open_new_window("Subject Pronouns")

    # Add buttons for different pronouns
    pronoun_buttons = [
        ("I", "I"),
        ("You", "You"),
        ("He", "He"),
        ("She", "She"),
        ("We", "We"),
        ("They", "They")
    ]

    row, col = 0, 0
    for pronoun, text in pronoun_buttons:
        btn = tk.Button(new_window, text=pronoun, command=lambda t=text: on_button_click(t, "subject"), height=5, width=15)
        btn.grid(row=row, column=col, padx=20, pady=20)
        col += 1
        if col > 3:
            col = 0
            row += 1

# Function to handle the "Verb" category
def open_verb_window():
    if not selected_subject:
        messagebox.showwarning("No Subject Selected", "Please select a subject first.")
        return

    new_window = open_new_window("Verbs")

    # Add buttons for common verbs
    verb_buttons = [
        ("To ask", "To ask"),
        ("To be", "To be"),
        ("Can", "Can"),
        ("To come", "To come"),
        ("To do", "To do"),
        ("To have", "To have"),
        ("To feel", "To feel"),
        ("To know", "To know"),
        ("To like", "To like"),
        ("To make", "To make")
    ]

    row, col = 0, 0
    for verb, text in verb_buttons:
        conjugated_verb = conjugate_verb(verb, selected_subject)
        btn = tk.Button(new_window, text=conjugated_verb, command=lambda t=conjugated_verb: on_button_click(t, "verb"), height=5, width=15)
        btn.grid(row=row, column=col, padx=20, pady=20)
        col += 1
        if col > 3:
            col = 0
            row += 1

# Function to handle the "Object" category
def open_object_window():
    new_window = open_new_window("Object Categories")

    # Add buttons for Object subcategories
    object_buttons = [
        ("School", "School"),
        ("Shop", "Shop"),
        ("Food", "Food"),
        ("Drink", "Drink"),
        ("Home", "Home"),
    ]

    row, col = 0, 0
    for obj, text in object_buttons:
        btn = tk.Button(new_window, text=obj, command=lambda t=text: open_specific_object_window(t), height=5, width=15)
        btn.grid(row=row, column=col, padx=20, pady=20)
        col += 1
        if col > 3:
            col = 0
            row += 1

def open_specific_object_window(category):
    new_window = open_new_window(category)

    # Add specific words based on the object category
    specific_objects = {
        "School": ["Book", "Teacher", "Classroom"],
        "Shop": ["Cashier", "Store", "Checkout"],
        "Food": ["Apple", "Bread", "Cake"],
        "Drink": ["Water", "Juice", "Milk"],
        "Home": ["Bed", "Sofa", "Television"]
    }

    row, col = 0, 0
    for obj in specific_objects.get(category, []):
        btn = tk.Button(new_window, text=obj, command=lambda t=obj: on_button_click(t, "object"), height=5, width=15)
        btn.grid(row=row, column=col, padx=20, pady=20)
        col += 1
        if col > 3:
            col = 0
            row += 1

# Button click handler
def on_button_click(selection, category):
    global selected_subject, selected_verb, selected_object

    if category == "subject":
        selected_subject = selection
    elif category == "verb":
        selected_verb = selection
    elif category == "object":
        selected_object = selection

    print(f"You selected {selection}")

    if selected_subject and selected_verb and selected_object:
        finalize_selection()

# Function to finalize the selection
def finalize_selection():
    sentence = f"{selected_subject} {selected_verb} {selected_object}"
    result_window = tk.Toplevel(root)
    result_window.title("Finalize Selection")
    result_window.geometry('800x600')

    label = tk.Label(result_window, text=sentence, font=("Arial", 24))
    label.pack(pady=20)

    edit_button = tk.Button(result_window, text="Edit", command=result_window.destroy, height=2, width=10)
    edit_button.pack(side='left', padx=20, pady=20)

    approve_button = tk.Button(result_window, text="Approve", command=lambda: approve_selection(sentence), height=2, width=10)
    approve_button.pack(side='right', padx=20, pady=20)

# Function to approve the selection and output via speakers
def approve_selection(sentence):
    # Output the sentence via speakers
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(sentence)
    engine.runAndWait()

    messagebox.showinfo("Sentence Output", f"The sentence '{sentence}' has been spoken.")

# Initializing the main window
root = tk.Tk()
root.title('AAC Home Window')
root.geometry('800x600')

# Creating a frame to hold the buttons and center them
frame = tk.Frame(root)
frame.pack(expand=True)

# Creating buttons for Subject, Verb, Object, and placing them in the frame
subject_button = tk.Button(frame, text="Subject", command=open_subject_window, height=10, width=25)
subject_button.grid(row=0, column=0, padx=20, pady=20)

verb_button = tk.Button(frame, text="Verb", command=open_verb_window, height=10, width=25)
verb_button.grid(row=0, column=1, padx=20, pady=20)

object_button = tk.Button(frame, text="Object", command=open_object_window, height=10, width=25)
object_button.grid(row=0, column=2, padx=20, pady=20)

# Start the main loop
root.mainloop()
