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
                if not isinstance(self.posts, dict):
                    self.posts = {}
        except FileNotFoundError:
            self.posts = {}

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f, indent=4)

    def user_search(self, search_username):
        usernames = [user.lower() for user in self.users.keys()]
        if search_username.lower() in usernames:
            return self.users[search_username]
        else:
            return None

    def get_user_posts(self, username):
        return [post for post in self.posts.values() if post['author'] == username]


class UserSearchApp:
    def __init__(self, root):
        self.manager = SocialMediaManager()

        self.root = root
        self.root.title("Search User")
        self.root.geometry("300x150")

        self.search_button = tk.Button(root, text="Open Search", command=self.open_search_window)
        self.search_button.pack(pady=20)

        self.current_user = "current_user"  # Replace this with the actual logged-in user

    def open_search_window(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search for User")
        self.search_window.geometry("300x300")

        tk.Label(self.search_window, text="Enter username:").pack(pady=5)
        self.search_entry = tk.Entry(self.search_window)
        self.search_entry.pack(pady=5)

        search_button = tk.Button(self.search_window, text="Search", command=self.search_user)
        search_button.pack(pady=5)

        self.result_frame = tk.Frame(self.search_window)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def search_user(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        username = self.search_entry.get()
        user_data = self.manager.user_search(username)
        if user_data:
            post_data = self.manager.get_user_posts(username)
            self.display_user_bar(username, post_data)
        else:
            tk.Label(self.result_frame, text="User not found.", fg="red").pack()

    def display_user_bar(self, username, posts):
        bar_frame = tk.Frame(self.result_frame, bd=2, relief="groove", padx=10, pady=5)
        bar_frame.pack(fill=tk.X, pady=5)

        user_label = tk.Label(bar_frame, text=username, font=("Arial", 12, "bold"))
        user_label.pack(side=tk.LEFT)

        follow_button = tk.Button(bar_frame, text="Send Friend Request", command=lambda: self.send_friend_request(username, follow_button))
        follow_button.pack(side=tk.RIGHT, padx=5)

        # View Profile Button
        view_profile_button = tk.Button(bar_frame, text="View Profile", command=lambda: self.open_profile_view(username, posts))
        view_profile_button.pack(side=tk.RIGHT, padx=5)

        if posts:
            posts_frame = tk.Frame(bar_frame)
            posts_frame.pack(fill=tk.X, pady=5)

            tk.Label(posts_frame, text="Posts:", font=("Arial", 10, "bold")).pack(anchor="w")

            for post in posts:
                if post['type'] == "text":
                    post_label = tk.Label(posts_frame, text=post['content'], wraplength=200, justify="left", font=("Arial", 9))
                else:
                    post_label = tk.Label(posts_frame, text="Image Post", wraplength=200, justify="left", font=("Arial", 9))
                post_label.pack(anchor="w")
        else:
            tk.Label(bar_frame, text="No posts available.", fg="gray").pack()

    def open_profile_view(self, username, posts):
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{username}'s Profile")
        profile_window.geometry("400x400")

        tk.Label(profile_window, text=f"Profile of {username}", font=("Arial", 16, "bold")).pack(pady=10)

        if posts:
            posts_frame = tk.Frame(profile_window)
            posts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            tk.Label(posts_frame, text="User's Posts:", font=("Arial", 12, "bold")).pack(anchor="w")

            for post in posts:
                post_frame = tk.Frame(posts_frame, bd=1, relief="solid", padx=10, pady=5)
                post_frame.pack(fill=tk.X, pady=5)

                # Post Type and Content
                if post['type'] == "text":
                    tk.Label(post_frame, text=f"Text Post: {post['content']}", wraplength=300, justify="left").pack(anchor="w")
                elif post['type'] == "image":
                    tk.Label(post_frame, text="Image Post:").pack(anchor="w")
                    try:
                        image = Image.open(post['image_path'])
                        image = image.resize((200, 200), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(image)
                        img_label = tk.Label(post_frame, image=img)
                        img_label.image = img  # Keep a reference
                        img_label.pack(anchor="w")
                    except Exception as e:
                        tk.Label(post_frame, text=f"Error loading image: {e}", fg="red").pack(anchor="w")

                # Likes and Comments
                tk.Label(post_frame, text=f"Likes: {post['likes']}, Comments: {len(post['comments'])}", fg="blue").pack(anchor="w")

                # Comments
                for comment in post['comments']:
                    tk.Label(post_frame, text=f"{comment['user']}: {comment['comment']}", wraplength=250, justify="left").pack(anchor="w", padx=10)

        else:
            tk.Label(profile_window, text="No posts available.", fg="gray").pack(pady=20)

    def send_friend_request(self, username, follow_button):
        success = self.manager.send_friend_request(self.current_user, username)

        if success:
            messagebox.showinfo("Friend Request", f"You sent a friend request to {username}.")
            follow_button.config(text="Request Sent", state=tk.DISABLED)
        else:
            messagebox.showwarning("Friend Request", f"Could not send a friend request to {username}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserSearchApp(root)
    root.mainloop()