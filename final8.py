import json
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


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

    def quick_sort(self, lst):
        if len(lst) <= 1:
            return lst
        pivot = lst[len(lst) // 2]
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
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
        usernames = self.quick_sort([user.lower() for user in self.users.keys()])
        found = self.binary_search(usernames, search_username.lower())

        if found:
            return self.users[search_username]  # Return user data if found
        else:
            return None  # Return None if user not found

    def follow_user(self, current_user, user_to_follow):
        if current_user in self.users and user_to_follow in self.users:
            if user_to_follow not in self.users[current_user]['friends']:
                self.users[current_user]['friends'].append(user_to_follow)
                self.users[user_to_follow]['friends'].append(current_user)
                self.save_data()
                return True
            else:
                return False  # Already following
        return False  # One of the users does not exist


class UserSearchApp:
    def __init__(self, root):
        self.manager = SocialMediaManager()

        self.root = root
        self.root.title("Search User")
        self.root.geometry("300x150")

        self.search_button = tk.Button(root, text="Open Search", command=self.open_search_window)
        self.search_button.pack(pady=20)

    def open_search_window(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search for User")
        self.search_window.geometry("300x300")

        # Label and Entry for search input
        tk.Label(self.search_window, text="Enter username:").pack(pady=5)
        self.search_entry = tk.Entry(self.search_window)
        self.search_entry.pack(pady=5)

        # Search button
        search_button = tk.Button(self.search_window, text="Search", command=self.search_user)
        search_button.pack(pady=5)

        self.result_frame = tk.Frame(self.search_window)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def search_user(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()  # Clear previous results

        username = self.search_entry.get()
        user_data = self.manager.user_search(username)
        if user_data:
            self.display_user_bar(username)
        else:
            tk.Label(self.result_frame, text="User not found.", fg="red").pack()

    def display_user_bar(self, username):
        bar_frame = tk.Frame(self.result_frame, bd=2, relief="groove", padx=10, pady=5)
        bar_frame.pack(fill=tk.X, pady=5)

        # Username label
        user_label = tk.Label(bar_frame, text=username, font=("Arial", 12, "bold"))
        user_label.pack(side=tk.LEFT)

        # Follow button
        follow_button = tk.Button(bar_frame, text="Follow", command=lambda: self.follow_user(username, follow_button))
        follow_button.pack(side=tk.RIGHT, padx=5)

        # View Profile button
        profile_button = tk.Button(bar_frame, text="View Profile", command=lambda: self.view_profile(username))
        profile_button.pack(side=tk.RIGHT, padx=5)

    def follow_user(self, username, follow_button):
        # Assuming 'current_user' is available, replace 'current_user' with the actual current logged-in user
        current_user = "current_user"
        success = self.manager.follow_user(current_user, username)

        if success:
            messagebox.showinfo("Follow", f"You followed {username}.")
            follow_button.config(text="Following", state=tk.DISABLED)
        else:
            messagebox.showwarning("Follow", f"You are already following {username}!")

    def view_profile(self, username):
        user_profile_page(self.search_window, self.manager, username)


def user_profile_page(main_window, s_manager, user_name):
    main_window.title(f"{user_name}'s Profile")
    main_window.geometry("600x700")

    user_data = s_manager.users.get(user_name)
    post_data = [post for post in s_manager.posts if post['author'] == user_name]

    def show_post_details(post):
        details = f"Likes: {post['likes']}\nComments:\n"
        if not post['comments']:
            details += "No Comments Yet!"
        else:
            for comment in post['comments']:
                details += f"{comment['user']}: {comment['text']}\n"
        messagebox.showinfo("Post Details", details)

    # Frame1: username, posts num, friends num
    post_num = len(post_data)
    friends_num = len(user_data['friends'])

    frame1 = tk.Frame(main_window, highlightbackground="lavender", highlightthickness=3)
    frame1.pack(pady=10)

    tk.Label(frame1, text=user_data['username'], font=("Times New Roman", 15, "bold")).grid(row=0, column=0, columnspan=2)
    tk.Label(frame1, text="Posts", font=("Times New Roman", 13)).grid(row=1, column=0)
    tk.Label(frame1, text=f'{post_num}', font=("Times New Roman", 12), fg="purple").grid(row=2, column=0)
    tk.Label(frame1, text="Friends", font=("Times New Roman", 13)).grid(row=1, column=1)
    tk.Label(frame1, text=f'{friends_num}', font=("Times New Roman", 12), fg="purple").grid(row=2, column=1)

    # Frame2: bio
    frame2 = tk.Frame(main_window, highlightbackground="lavender", highlightthickness=3)
    frame2.pack(pady=10)

    tk.Label(frame2, text="Bio", font=("Times New Roman", 13)).pack()
    tk.Label(frame2, text=user_data.get('Bio', 'No bio'), wraplength=400, justify="left", font=("Times New Roman", 12), fg="purple").pack()

    # Frame3: posts
    frame3 = tk.Frame(main_window, highlightbackground="purple", highlightthickness=2)
    frame3.pack(pady=10, fill="both", expand=True)

    # Scrollbar
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Vertical.TScrollbar", background="lavender", troughcolor="lavender", arrowcolor="purple")
    canvas = tk.Canvas(frame3, height=400)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame3, orient=tk.VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    post_frame = tk.Frame(canvas)
    canvas.create_window((250, 0), window=post_frame, anchor="n", width=500)

    if not post_data:  # Empty
        post_label = tk.Label(post_frame, text="No posts to show!", wraplength=400, justify="left", font=("Times New Roman", 12), fg="gray")
        post_label.pack(pady=5, anchor=tk.CENTER)
    else:
        for post in post_data:
            if post['type'] == 'text':
                post_label = tk.Label(post_frame, text=post['content'], wraplength=400, justify="left")
            elif post['type'] == 'image':
                image = Image.open(post['image_path'])
                image = image.resize((250, 250))  # Resize the image to fit
                photo = ImageTk.PhotoImage(image)
                post_label = tk.Label(post_frame, image=photo)
                post_label.image = photo  # Keep a reference to avoid garbage
                
if __name__ == "__main__":
    root = tk.Tk()
    app = UserSearchApp(root)
    root.mainloop()