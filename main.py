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
                if not isinstance(self.posts, list):
                    self.posts = []
        except FileNotFoundError:
            self.posts = []

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f, indent=4)

    def quick_sort(self, list):
        if len(list) <= 1:
            return list
        pivot = list[len(list) // 2]
        left = [x for x in list if x < pivot]
        middle = [x for x in list if x == pivot]
        right = [x for x in list if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    def binary_search(self, myList, target):
        left, right = 0, len(myList) - 1
        while left <= right:
            mid = (left + right) // 2
            if myList[mid] == target:
                return True
            elif myList[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def user_search(self, search_username):
        usernames = self.quick_sort(list(self.users.keys()))
        return self.binary_search(usernames, search_username)

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

        # Logout button
        tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage")).pack(side=tk.TOP, anchor='e')

        # Create post section
        self.create_post_section()

        # Search user section
        self.create_search_section()

        # Posts section
        self.create_posts_section()

    def create_post_section(self):
        # Create post frame
        create_post_frame = tk.Frame(self)
        create_post_frame.pack(pady=10)

        tk.Label(create_post_frame, text="Username").pack()
        self.username_entry = tk.Entry(create_post_frame)
        self.username_entry.pack()

        tk.Label(create_post_frame, text="Image Path").pack()
        self.image_path_entry = tk.Entry(create_post_frame)
        self.image_path_entry.pack()

        create_post_button = tk.Button(create_post_frame, text="Create Post", command=self.create_post)
        create_post_button.pack(pady=10)

    def create_search_section(self):
        # Search user frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search for User").pack()
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack()

        search_button = tk.Button(search_frame, text="Search", command=self.search_user)
        search_button.pack(pady=10)

        self.search_result_label = tk.Label(search_frame, text="")
        self.search_result_label.pack(pady=10)

    def search_user(self):
        search_username = self.search_entry.get()
        found = self.social_media_manager.user_search(search_username)
        if found:
            self.search_result_label.config(text=f"User '{search_username}' found!")
        else:
            self.search_result_label.config(text=f"User '{search_username}' not found.")

    def create_posts_section(self):
        # Display posts
        for post in self.social_media_manager.posts:
            post_frame = tk.Frame(self)
            post_frame.pack(pady=10)

            author_label = tk.Label(post_frame, text=f"Posted by {post['author']}")
            author_label.pack(side=tk.TOP, anchor='w')

            try:
                image = Image.open(post['image_path'])
                image = image.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(post_frame, image=photo)
                image_label.image = photo
                image_label.pack()
            except Exception as e:
                tk.Label(post_frame, text="Image not found").pack()

            like_button = tk.Button(post_frame, text=f"Like ({post['likes']})", command=lambda p=post: self.like_post(p['post_id']))
            like_button.pack(side=tk.LEFT, padx=10)

    def create_post(self):
        username = self.username
if __name__ == "__main__":
    smm = SocialMediaManager()
    app = MainApp(smm)
    app.mainloop()