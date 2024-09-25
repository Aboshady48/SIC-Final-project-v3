import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_dict(self):
        return {'username': self.username, 'email': self.email, 'password': self.password}

class SocialMediaManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.posts_file = 'posts.json'
        self.load_data()

    def load_data(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

        try:
            with open(self.posts_file, 'r') as f:
                self.posts = json.load(f)
        except FileNotFoundError:
            self.posts = {}

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f, indent=4)

    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            return True
        return False

    def register(self, username, email, password):
        if username in self.users:
            return False
        new_user = User(username, email, password)
        self.users[username] = new_user.get_dict()
        self.save_data()
        return True

def show_login_frame():
    login_frame.tkraise()

def show_signup_frame():
    signup_frame.tkraise()

def login():
    username = entry_username.get()
    password = entry_password.get()
    if smm.login(username, password):
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password")

def register():
    username = entry_new_username.get()
    email = entry_email.get()
    password = entry_new_password.get()
    if smm.register(username, email, password):
        messagebox.showinfo("Register", "Registration successful!")
    else:
        messagebox.showerror("Register", "Username already exists")
    

smm = SocialMediaManager()

root = tk.Tk()
root.title("Login and Sign-Up")
root.geometry("400x500")

# Load and set background image
bg_image = Image.open("360_F_391461057_5P0BOWl4lY442Zoo9rzEeJU0S2c1WDZR.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

login_frame = tk.Frame(root, bg='white', bd=5)
signup_frame = tk.Frame(root, bg='white', bd=5)

for frame in (login_frame, signup_frame):
    frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=400)

# Login Frame
tk.Label(login_frame, text="Login", font=("Helvetica", 20), bg='white').pack(pady=10)
tk.Label(login_frame, text="Username", bg='white').pack()
entry_username = tk.Entry(login_frame)
entry_username.pack()

tk.Label(login_frame, text="Password", bg='white').pack()
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack()

tk.Button(login_frame, text="Login", command=login, bg='#3897f0', fg='white').pack(pady=10)
tk.Button(login_frame, text="Go to Sign-Up", command=show_signup_frame, bg='white', fg='#3897f0').pack()

# Sign-Up Frame
tk.Label(signup_frame, text="Sign Up", font=("Helvetica", 20), bg='white').pack(pady=10)
tk.Label(signup_frame, text="Username", bg='white').pack()
entry_new_username = tk.Entry(signup_frame)
entry_new_username.pack()

tk.Label(signup_frame, text="Email", bg='white').pack()
entry_email = tk.Entry(signup_frame)
entry_email.pack()

tk.Label(signup_frame, text="Password", bg='white').pack()
entry_new_password = tk.Entry(signup_frame, show="*")
entry_new_password.pack()

tk.Button(signup_frame, text="Register", command=register, bg='#3897f0', fg='white').pack(pady=10)
tk.Button(signup_frame, text="Go to Login", command=show_login_frame, bg='white', fg='#3897f0').pack()

show_login_frame()
root.mainloop()

class HomePage(tk.Frame):
    def __init__(self, parent, controller, social_media_manager):
        super().__init__(parent)
        self.controller = controller
        self.social_media_manager = social_media_manager

        # Create the logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(side=tk.TOP, anchor='e')

        # Create the posts section
        self.create_posts_section()

    def logout(self):
        # Logic to log out and go back to login page
        self.controller.show_frame("LoginPage")

    def create_posts_section(self):
        # Display posts
        for post in self.social_media_manager.posts:
            post_frame = tk.Frame(self)
            post_frame.pack(pady=10)

            # Post Author with Follow button
            author_label = tk.Label(post_frame, text=f"Posted by {post['author']}")
            author_label.pack(side=tk.TOP, anchor='w')
            
            follow_button = tk.Button(post_frame, text="Follow", command=lambda p=post: self.follow_user(p['author']))
            follow_button.pack(side=tk.TOP, anchor='e')

            # Post Image
            image = Image.open(post['image_path'])
            image = image.resize((400, 300), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(post_frame, image=photo)
            image_label.image = photo  # Keep a reference to the image
            image_label.pack()

            # Like and Comment buttons
            like_button = tk.Button(post_frame, text=f"Like ({post['likes']})", command=lambda p=post: self.like_post(p['post_id']))
            like_button.pack(side=tk.LEFT, padx=10)

            comment_button = tk.Button(post_frame, text="Comment", command=lambda p=post: self.comment_on_post(p['post_id']))
            comment_button.pack(side=tk.LEFT, padx=10)

    def follow_user(self, username):
        # Logic to follow the user
        print(f"Followed {username}")
        messagebox.showinfo("Follow", f"You followed {username}")

    def like_post(self, post_id):
        # Logic to like a post
        for post in self.social_media_manager.posts:
            if post['post_id'] == post_id:
                post['likes'] += 1
        self.social_media_manager.save_data()
        self.refresh()

    def comment_on_post(self, post_id):
        # Logic to comment on a post
        print(f"Comment on post {post_id}")
        # Add your comment logic here

    def refresh(self):
        # Refresh the page to update like counts, etc.
        for widget in self.winfo_children():
            widget.destroy()
        self.create_posts_section()

# Assuming you have your SocialMediaManager class from earlier
social_media_manager = SocialMediaManager()

# Then in your main GUI you can create the HomePage like this:
root = tk.Tk()
home_page = HomePage(root, None, social_media_manager)
home_page.pack()
root.mainloop()