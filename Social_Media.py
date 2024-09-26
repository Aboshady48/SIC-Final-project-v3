import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

class User:
    def __init__(self, username, email, password,bio):
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.friends = []
        self.friend_requests = []
        self.posts = []
        self.messages_to_you = []
        self.messages_from_you = []

    def get_dict(self):
        dict_obj = {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "Bio": self.bio,
                "friends": [],
                "friend_requests": [],
                "posts": [],
                "messages_to_you": [],
                "messages_from_you": []
            }
        return dict_obj

# inheritance  & polymorphism : inheritance , override
class Post:
    def __init__(self, author, post_id):
        self.author = author
        self.post_id = post_id
        self.likes = 0
        self.comments = []

    def to_dict(self):
        return {
            "author": self.author,
            "post_id": self.post_id,
            "likes": self.likes,
            "comments": self.comments
        }


class TextPost(Post):
    def __init__(self, author, post_id, content):
        super().__init__(author, post_id)
        self.type = "text"
        self.content = content

    def to_dict(self):
        post_dict = super().to_dict()
        post_dict["type"] = self.type
        post_dict["content"] = self.content
        return post_dict


class ImagePost(Post):
    def __init__(self, author, post_id, image_path):
        super().__init__(author, post_id)
        self.type = "image"
        self.image_path = image_path

    def to_dict(self):
        post_dict = super().to_dict()
        post_dict["type"] = self.type
        post_dict["image_path"] = self.image_path
        return post_dict


class SocialMediaManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.posts_file = 'posts.json'
        self.load_data()

    def load_data(self):
        with open(self.users_file, 'r') as f:
            self.users = json.load(f)

        with open(self.posts_file, 'r') as f:
            self.posts = json.load(f)

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f,indent=4)
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f,indent=4)

    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            return 'hello',self.users[username]['username']
        return None

    def register(self, username, email, password,bio):
        if username in self.users:
            return False
        new_user = User(username, email, password,bio)
        self.users[username] = new_user.get_dict()
        self.save_data()

    def create_post(self, username, content, post_type):
        post_id = len(self.posts) + 1
        if post_type == "text":
            post = TextPost(username, post_id, content)
        elif post_type == "image":
            post = ImagePost(username, post_id, content)

        self.posts[post_id] = post.to_dict()
        self.users[username]['posts'].append(post_id)
        self.save_data()
        return post

    def send_friend_request(self, from_user, to_user):
        if to_user in self.users and from_user not in self.users[to_user]['friend_requests']:
            self.users[to_user]['friend_requests'].append(from_user)
            self.save_data()

    def accept_friend_request(self, user, friend):
        if friend in self.users[user]['friend_requests']:
            self.users[user]['friends'].append(friend)
            self.users[friend]['friends'].append(user)
            self.users[user]['friend_requests'].remove(friend)
            self.save_data()

    def decline_friend_request(self, user, friend):
        if friend in self.users[user]['friend_requests']:
            self.users[user]['friend_requests'].remove(friend)
            self.save_data()

    def view_friend_requests(self, user):
        return self.users[user]['friend_requests']

    def send_message(self, from_user, to_user, message):
        if to_user in self.users and from_user in self.users:
            self.users[to_user]['messages_to_you'].append({'from': from_user,
                                                    'content': message
                                                    })
            self.users[from_user]['messages_from_you'].append({'to': to_user,
                                                    'content': message
                                                    })

            self.save_data()

    def view_inbox(self, user):
        return self.users[user]['messages_to_you'],self.users[user]['messages_from_you']

    def like_post(self, post_id, user):
        if post_id in self.posts and user in self.users:
            self.posts[post_id]['likes'] += 1
            self.save_data()

    def comment_on_post(self, post_id, user, comment):
        if post_id in self.posts:
            self.posts[post_id]['comments'].append({'user': user,
                                                    'comment': comment
                                                    })
            self.save_data()

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
        found = self.binary_search(usernames, search_username)

        if found:
            return (f"User '{search_username}' found \n '{self.users[search_username]['username']}'"
                    f" \n '{self.users[search_username]['friends']}' \n '{self.users[search_username]['posts']}'")
        else:
            return f"No results found for '{search_username}'"

    # 3 functions for admin if we want
    # def delete_user(self, username):
    #     if username in self.users:
    #         del self.users[username]
    #         self.save_data()
    #
    # def block_user(self, username):
    #     if username in self.users:
    #         self.users[username]['blocked'] = True
    #         self.save_data()
    #
    # def view_platform_stats(self):
    #     return {
    #         'users_count': len(self.users),
    #         'posts_count': len(self.posts)
    #     }

# k = int(input("enter your choice : "))
# username = "bat"
# if k == 1:
#     typee = input("[1] text post , [2] image post : ")
#     content = input("Enter the content")
#     if typee =='1':
#         SMM.create_post(username, content, 'text')
#     else:
#         SMM.create_post(username, content, 'image')
# if k == 2:
#     to_user = input("enter user")
#     SMM.send_friend_request(username, to_user)
# if k == 3 :
#     friend = input("enter")
#     SMM.accept_friend_request(username, friend)
# if k == 4 :
#     requested_user = input("Enter request user ")
#     SMM.decline_friend_request(username,requested_user)
# if k == 5 :
#     print(SMM.view_friend_requests(username))
#
# if k == 6:
#     to_user = input("enter")
#     message = input("message: ")
#     SMM.send_message(username, to_user, message)
#
# if k == 7:
#     print(SMM.view_inbox(username))
#
# if k == 8:
#     post_id = input("post id")
#     SMM.like_post(post_id, username)
# if k == 9:
#     post_id = input("id")
#     comment = input("comment:")
#     SMM.comment_on_post(post_id, username, comment)
#
# if k == 10:
#     user = input("Enter your username :")
#     password = input("Enter your password :")
#     print(SMM.login(user, password))
# if k == 11:
#     user = input("Enter your username :")
#     email = input("Enter your email :")
#     password = input("Enter your password :")
#     bio = input("Enter your bio :")
#     SMM.register(user, email, password,bio)
#
# if k == 12:
#     user_search = input("Enter username to search: ")
#     print(SMM.user_search(user_search))


def add_post_form(main_window, user_name):
    main_window.title("Add Post")
    main_window.geometry("600x700")

    label = tk.Label(main_window, text="Add Post Page", font=("Times New Roman", 16, "bold", "italic"), fg="#301934")
    label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

    def browse_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            image_entry.delete(0, tk.END)
            image_entry.insert(0, file_path)

    # type menu
    ttk.Label(main_window, text="Post Type:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    type_choice = tk.StringVar()
    type_menu = ttk.Combobox(main_window, textvariable=type_choice, values=["text", "image"], state="readonly")
    type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    type_menu.current(0)

    content_label = ttk.Label(main_window, text="Content:")
    content_entry = ttk.Entry(main_window, width=40)
    image_label = ttk.Label(main_window, text="Image Path:")
    image_entry = ttk.Entry(main_window, width=30)

    browse_button = ttk.Button(main_window, text="Browse", command=browse_image)

    # show fields based on post type
    def show_specific(*args):
        if type_choice.get() == "text":
            image_label.grid_forget()
            image_entry.grid_forget()
            browse_button.grid_forget()
            content_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            content_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        elif type_choice.get() == "image":
            content_label.grid_forget()
            content_entry.grid_forget()
            image_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            image_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
            browse_button.grid(row=2, column=2, padx=5, pady=5)

    type_choice.trace("w", show_specific)

    def save_post():
        post_type = type_choice.get()

        if post_type == "text":
            content = content_entry.get()
            if not content:
                messagebox.showwarning("Input Error", "Text content cannot be empty!")
                return
            post = SMM.create_post(user_name, content, "text")

        elif post_type == "image":
            image_path = image_entry.get()
            if not image_path:
                messagebox.showwarning("Input Error", "Please select image!")
                return
            post = SMM.create_post(user_name, image_path, "image")

        messagebox.showinfo("Success", "Post added successfully!")
        SMM.save_data()

    button_frame = tk.Frame(main_window)
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)
    add_button = ttk.Button(button_frame, text="Add Post", command=save_post)
    add_button.grid(row=0, column=0, padx=10)
    back_button = ttk.Button(button_frame, text="Back")  # command back
    back_button.grid(row=0, column=1, padx=10)


def user_profile_page(main_window, s_manager, user_name):
    main_window.title(f"{user_name}'s Profile")
    main_window.geometry("600x700")

    user_data = s_manager.users.get(user_name)
    post_data = []
    for p_id, post in s_manager.posts.items():
        if post['author'] == user_name:
            post_data.append(post)

    def show_post_details(post):
        details = f"Likes: {post['likes']}\nComments:\n"
        if post['comments'] == []:
            details += "No Comments Yet!"
        else:
            for comment in post['comments']:
                details += f"{comment['user']}: {comment['text']}\n"
        messagebox.showinfo("Post Details", details)

    # frame1: username, posts num, friends num
    post_num = len(post_data)
    friends_num = len(user_data['friends'])

    frame1 = tk.Frame(main_window, highlightbackground="lavender", highlightthickness=3, highlightcolor="purple")
    frame1.pack(pady=10)

    tk.Label(frame1, text=user_data['username'], font=("Times New Roman", 15, "bold")).grid(row=0, column=0, columnspan=2)
    tk.Label(frame1, text="Posts",font=("Times New Roman", 13)).grid(row=1, column=0)
    tk.Label(frame1, text=f'{post_num}',font=("Times New Roman", 12),fg="purple").grid(row=2, column=0)
    tk.Label(frame1, text="Friends",font=("Times New Roman", 13)).grid(row=1, column=1)
    tk.Label(frame1, text=f'{friends_num}', font=("Times New Roman", 12),fg="purple").grid(row=2, column=1)

    # frame2: bio
    frame2 = tk.Frame(main_window, highlightbackground="lavender", highlightthickness=3, highlightcolor="purple")
    frame2.pack(pady=10)

    tk.Label(frame2, text="Bio", font=("Times New Roman", 13)).pack()
    tk.Label(frame2, text=user_data.get('Bio', 'No bio'), wraplength=400, justify="left",font=("Times New Roman", 12),fg="purple").pack()

    # frame3: posts
    frame3 = tk.Frame(main_window, highlightbackground="purple", highlightthickness=2, highlightcolor="purple")
    frame3.pack(pady=10, fill="both", expand=True)

    # scrollbar
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Vertical.TScrollbar",background="lavender",troughcolor="lavender",arrowcolor="purple")
    canvas = tk.Canvas(frame3, height=400)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame3, orient=tk.VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    post_frame = tk.Frame(canvas)
    canvas.create_window((250, 0), window=post_frame, anchor="n", width=500)

    if post_data == []: # empty
        post_label = tk.Label(post_frame, text="No posts to show!", wraplength=400, justify="left",font=("Times New Roman", 12),fg="gray")
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
                post_label.image = photo  # Keep a reference to avoid garbage collection

            post_label.pack(pady=5, anchor=tk.CENTER)
            details_button = tk.Button(post_frame, text="Details", command=lambda p=post: show_post_details(p))
            details_button.pack(anchor=tk.CENTER)

        post_frame.update_idletasks()  # to ensure geometry is calculated
        canvas.configure(scrollregion=canvas.bbox("all"))

    back_button = tk.Button(main_window, text="Back")
    back_button.pack(side="bottom", pady=10)


root = tk.Tk()
SMM = SocialMediaManager()
# add_post_form(root ,"user2")
user_profile_page(root,SMM, "user2")

root.mainloop()