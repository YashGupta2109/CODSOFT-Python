import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")
        self.contacts = load_contacts()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.contacts_listbox = tk.Listbox(self.frame, width=40, height=15)
        self.contacts_listbox.pack(side=tk.LEFT, padx=10)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.show_contact_details)

        self.contacts_text = scrolledtext.ScrolledText(self.frame, width=60, height=15, wrap=tk.WORD, state='disabled')
        self.contacts_text.pack(side=tk.RIGHT, padx=10)

        self.update_listbox()

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.name_label = tk.Label(self.entry_frame, text="Name")
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.entry_frame, width=20)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        self.phone_label = tk.Label(self.entry_frame, text="Phone")
        self.phone_label.pack(side=tk.LEFT)
        self.phone_entry = tk.Entry(self.entry_frame, width=20)
        self.phone_entry.pack(side=tk.LEFT, padx=5)

        self.email_label = tk.Label(self.entry_frame, text="Email")
        self.email_label.pack(side=tk.LEFT)
        self.email_entry = tk.Entry(self.entry_frame, width=20)
        self.email_entry.pack(side=tk.LEFT, padx=5)

        self.address_label = tk.Label(self.entry_frame, text="Address")
        self.address_label.pack(side=tk.LEFT)
        self.address_entry = tk.Entry(self.entry_frame, width=20)
        self.address_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.update_button = tk.Button(self.button_frame, text="Update Contact", command=self.update_contact)
        self.update_button.pack(side=tk.LEFT, padx=10)

        self.search_button = tk.Button(self.button_frame, text="Search Contact", command=self.search_contact)
        self.search_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def update_listbox(self, contacts=None):
        self.contacts_listbox.delete(0, tk.END)
        contacts = contacts if contacts is not None else self.contacts
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, contact['name'])

    def show_contact_details(self, event):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            selected_contact = self.contacts[selected_index[0]]
            self.contacts_text.config(state='normal')
            self.contacts_text.delete(1.0, tk.END)
            self.contacts_text.insert(tk.END, f"Name: {selected_contact['name']}\n")
            self.contacts_text.insert(tk.END, f"Phone: {selected_contact['phone']}\n")
            self.contacts_text.insert(tk.END, f"Email: {selected_contact['email']}\n")
            self.contacts_text.insert(tk.END, f"Address: {selected_contact['address']}\n")
            self.contacts_text.config(state='disabled')

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone or not email or not address:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        contact = {'name': name, 'phone': phone, 'email': email, 'address': address}
        self.contacts.append(contact)
        save_contacts(self.contacts)
        self.update_listbox()

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def update_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            contact_index = selected_index[0]
            contact = self.contacts[contact_index]

            name = simpledialog.askstring("Update Contact", "Enter new name:", initialvalue=contact['name'])
            phone = simpledialog.askstring("Update Contact", "Enter new phone:", initialvalue=contact['phone'])
            email = simpledialog.askstring("Update Contact", "Enter new email:", initialvalue=contact['email'])
            address = simpledialog.askstring("Update Contact", "Enter new address:", initialvalue=contact['address'])

            if name and phone and email and address:
                self.contacts[contact_index]['name'] = name
                self.contacts[contact_index]['phone'] = phone
                self.contacts[contact_index]['email'] = email
                self.contacts[contact_index]['address'] = address

                save_contacts(self.contacts)
                self.update_listbox()
                self.show_contact_details(None)
            else:
                messagebox.showwarning("Input Error", "All fields are required.")
        else:
            messagebox.showwarning("Selection Error", "No contact selected. Please select a contact to update.")

    def search_contact(self):
        search_term = simpledialog.askstring("Search Contact", "Enter name or phone number to search:")
        if search_term:
            results = [
                contact for contact in self.contacts
                if search_term.lower() in contact['name'].lower() or search_term in contact['phone']
            ]
            self.update_listbox(results)
        else:
            messagebox.showwarning("Input Error", "Search term is required.")

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            del self.contacts[selected_index[0]]
            save_contacts(self.contacts)
            self.update_listbox()
            self.contacts_text.config(state='normal')
            self.contacts_text.delete(1.0, tk.END)
            self.contacts_text.config(state='disabled')
        else:
            messagebox.showwarning("Selection Error", "No contact selected. Please select a contact to delete.")

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
