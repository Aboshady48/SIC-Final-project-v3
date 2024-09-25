import json
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
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
        self.image_path = image_path  # url or path

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

    def register(self, username, email, password):
        if username in self.users:
            return False
        new_user = User(username, email, password)
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


SMM = SocialMediaManager()
k = int(input("enter your choice : "))
username = "user1"
if k == 1:
    typee = input("[1] text post , [2] image post : ")
    content = input("Enter the content")
    if typee =='1':
        SMM.create_post(username, content, 'text')
    else:
        SMM.create_post(username, content, 'image')
if k == 2:
    to_user = input("enter user")
    SMM.send_friend_request(username, to_user)
if k == 3 :
    friend = input("enter")
    SMM.accept_friend_request(username, friend)
if k == 4 :
    requested_user = input("Enter request user ")
    SMM.decline_friend_request(username,requested_user)
if k == 5 :
    print(SMM.view_friend_requests(username))

if k == 6:
    to_user = input("enter")
    message = input("message: ")
    SMM.send_message(username, to_user, message)

if k == 7:
    print(SMM.view_inbox(username))

if k == 8:
    post_id = input("post id")
    SMM.like_post(post_id, username)
if k == 9:
    post_id = input("id")
    comment = input("comment:")
    SMM.comment_on_post(post_id, username, comment)

if k == 10:
    user = input("Enter your username :")
    password = input("Enter your password :")
    print(SMM.login(user, password))
if k == 11:
    user = input("Enter your username :")
    email = input("Enter your email :")
    password = input("Enter your password :")
    print(SMM.register(user, email, password))

if k == 12:
    user_search = input("Enter username to search: ")
    print(SMM.user_search(user_search))


#####################################################################
from flask import Flask, request, jsonify, session
app = Flask(__name__)
app.secret_key = 'BOMA'
manager = SocialMediaManager()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    success, message = manager.register(data['username'], data['email'], data['password'])
    return jsonify({'success': success, 'message': message})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    success, message = manager.login(data['username'], data['password'])
    return jsonify({'success': success, 'message': message})

@app.route('/create_post', methods=['POST'])
def create_post():
    data = request.json
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'User not logged in'})
    post = manager.create_post(username, data['content'], data['post_type'])
    return jsonify({'success': True, 'post': post.to_dict()})

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    data = request.json
    from_user = session.get('username')
    to_user = data['to_user']
    if not from_user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.send_friend_request(from_user, to_user)
    return jsonify({'success': True, 'message': 'Friend request sent'})

@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request():
    data = request.json
    user = session.get('username')
    friend = data['friend']
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.accept_friend_request(user, friend)
    return jsonify({'success': True, 'message': 'Friend request accepted'})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    from_user = session.get('username')
    to_user = data['to_user']
    message = data['message']
    if not from_user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.send_message(from_user, to_user, message)
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/like_post', methods=['POST'])
def like_post():
    data = request.json
    post_id = data['post_id']
    user = session.get('username')
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.like_post(post_id, user)
    return jsonify({'success': True, 'message': 'Post liked'})

@app.route('/comment_on_post', methods=['POST'])
def comment_on_post():
    data = request.json
    post_id = data['post_id']
    comment = data['comment']
    user = session.get('username')
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.comment_on_post(post_id, user, comment)
    return jsonify({'success': True, 'message': 'Comment added'})

@app.route('/decline_friend_request', methods=['POST'])
def decline_friend_request():
    data = request.json
    user = session.get('username')
    friend = data['friend']
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    manager.decline_friend_request(user, friend)
    return jsonify({'success': True, 'message': 'Friend request declined'})

@app.route('/view_friend_requests', methods=['GET'])
def view_friend_requests():
    user = session.get('username')
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    friend_requests = manager.view_friend_requests(user)
    return jsonify({'success': True, 'friend_requests': friend_requests})

@app.route('/user_search', methods=['GET'])
def user_search():
    search_username = request.args.get('username')
    user_data = manager.user_search(search_username)
    if user_data:
        return jsonify({'success': True, 'user': user_data})
    return jsonify({'success': False, 'message': 'User not found'})

@app.route('/view_inbox', methods=['GET'])
def view_inbox():
    user = session.get('username')
    if not user:
        return jsonify({'success': False, 'message': 'User not logged in'})
    inbox = manager.view_inbox(user)
    return jsonify({'success': True, 'inbox': inbox})


app.run(debug=True)