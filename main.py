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
            self.posts = []

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

class MainApp(tk.Tk):
    def __init__(self, smm):
        super().__init__()
        self.smm = smm
        self.title("Social Media App")
        self.geometry("400x500")

        self.frames = {}
        for F in (LoginPage, SignupPage, HomePage):
            page_name = F.__name__
            frame = F(parent=self, controller=self, social_media_manager=smm)
            self.frames[page_name] = frame
            frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=400)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller, social_media_manager):
        super().__init__(parent)
        self.controller = controller
        self.social_media_manager = social_media_manager

        tk.Label(self, text="Login", font=("Helvetica", 20)).pack(pady=10)
        tk.Label(self, text="Username").pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        tk.Label(self, text="Password").pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Go to Sign-Up", command=lambda: controller.show_frame("SignupPage")).pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.social_media_manager.login(username, password):
            messagebox.showinfo("Login", "Login successful!")
            self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Login", "Invalid username or password")

class SignupPage(tk.Frame):
    def __init__(self, parent, controller, social_media_manager):
        super().__init__(parent)
        self.controller = controller
        self.social_media_manager = social_media_manager

        tk.Label(self, text="Sign Up", font=("Helvetica", 20)).pack(pady=10)
        tk.Label(self, text="Username").pack()
        self.entry_new_username = tk.Entry(self)
        self.entry_new_username.pack()

        tk.Label(self, text="Email").pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        tk.Label(self, text="Password").pack()
        self.entry_new_password = tk.Entry(self, show="*")
        self.entry_new_password.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Go to Login", command=lambda: controller.show_frame("LoginPage")).pack()

    def register(self):
        username = self.entry_new_username.get()
        email = self.entry_email.get()
        password = self.entry_new_password.get()
        if self.social_media_manager.register(username, email, password):
            messagebox.showinfo("Register", "Registration successful!")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Register", "Username already exists")

class HomePage(tk.Frame):
    def __init__(self, parent, controller, social_media_manager):
        super().__init__(parent)
        self.controller = controller
        self.social_media_manager = social_media_manager

        # Create the logout button
        logout_button = tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage"))
        logout_button.pack(side=tk.TOP, anchor='e')

        # Create the posts section
        self.create_posts_section()

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

if __name__ == "__main__":
    smm = SocialMediaManager()
    app = MainApp(smm)
    app.mainloop()