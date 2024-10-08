import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class SocialMediaManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.posts_file = 'posts.json'
        self.load_data()

    def load_data(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

        try:
            with open(self.posts_file, 'r', encoding='utf-8') as f:
                self.posts = json.load(f)
                if not isinstance(self.posts, dict):
                    self.posts = {}
        except FileNotFoundError:
            self.posts = {}

    def save_data(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)
        with open(self.posts_file, 'w', encoding='utf-8') as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=4)

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
        if self.binary_search(usernames, search_username.lower()):
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

        # Section for User's Posts (Image Posts)
        posts_frame = tk.Frame(self.result_frame, bd=2, relief="groove", padx=10, pady=5)
        posts_frame.pack(fill=tk.X, pady=10)

        tk.Label(posts_frame, text=f"{username}'s Posts:", font=("Arial", 12, "bold")).pack(anchor="w")

        if posts:
            for post in posts:
                post_frame = tk.Frame(posts_frame, bd=1, relief="solid", padx=10, pady=5)
                post_frame.pack(fill=tk.X, pady=5)

                # Display Post Type and Content
                if post['type'] == "text":
                    tk.Label(post_frame, text=f"Text Post: {post['content']}", wraplength=300, justify="left").pack(anchor="w")
                elif post['type'] == "image":
                    tk.Label(post_frame, text="Image Post:").pack(anchor="w")
                    try:
                        image_path = post['image_path']  # Ensure this is the correct path from JSON
                        print(f"Loading image from: {image_path}")
                        image = Image.open(image_path)
                        image = image.resize((200, 200), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(image)
                        img_label = tk.Label(post_frame, image=img)
                        img_label.image = img  # Keep a reference
                        img_label.pack(anchor="w")
                    except Exception as e:
                        tk.Label(post_frame, text=f"Error loading image: {e}", fg="red").pack(anchor="w")

        else:
            tk.Label(posts_frame, text="No posts available.", fg="gray").pack()

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
                        image_path = post['image_path']
                        print(f"Loading image from: {image_path}")
                        image = Image.open(image_path)
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
        # Simulate sending a friend request for now
        success = True  # Replace this with actual friend request functionality

        if success:
            messagebox.showinfo("Friend Request", f"You sent a friend request to {username}.")
            follow_button.config(text="Request Sent", state=tk.DISABLED)
        else:
            messagebox.showwarning("Friend Request", f"Could not send a friend request to {username}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserSearchApp(root)
    root.mainloop()