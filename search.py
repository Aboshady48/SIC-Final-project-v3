import json
import tkinter as tk
from tkinter import messagebox

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
        usernames = self.quick_sort(list(self.users.keys()))
        found = self.binary_search(usernames, search_username)

        if found:
            user_data = self.users[search_username]
            return (f"User '{search_username}' found\n"
                    f"Username: {user_data['username']}\n"
                    f"Friends: {', '.join(user_data.get('friends', []))}\n"
                    f"Posts: {', '.join(user_data.get('posts', []))}")
        else:
            return f"No results found for '{search_username}'"


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
        self.search_window.geometry("300x200")

        # Label and Entry for search input
        tk.Label(self.search_window, text="Enter username to search:").pack(pady=5)
        self.search_entry = tk.Entry(self.search_window)
        self.search_entry.pack(pady=5)

        # Search button
        search_btn = tk.Button(self.search_window, text="Search", command=self.perform_search)
        search_btn.pack(pady=10)

        # Label to display the result
        self.result_label = tk.Label(self.search_window, text="")
        self.result_label.pack(pady=10)

    def perform_search(self):
        search_username = self.search_entry.get()

        # Perform the search using the SocialMediaManager's search method
        result = self.manager.user_search(search_username)

        # Display the result in the result label
        self.result_label.config(text=result)


# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = UserSearchApp(root)
    root.mainloop()