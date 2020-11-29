# CS50-Final-Project

This is the Final Project of the CS50 online course series "My gallery" it's photosharing site Allows users to upload photos and share with other.

My Gallery lets users do the following:

- Create account then login in they area from website.
- Edit his frofile anytime he needs.
- Upload photos to share with other.
- Explore other images uploaded from other users.
- Make like to likes photo.
- Follow anther users to Follow up the latest photos.
- Search for specific photos.

|                     Login                     |                       Pages                       |
| :-------------------------------------------: | :-----------------------------------------------: |
| <img src="Screenshots/login.gif" width="400"> | <img src="Screenshots/pages_3.gif" width = "400"> |

| Responsive Web |
| :------------: |

 <img src="Screenshots/home.gif" width = "400">

|                       MyPage                        |                      Search                      |
| :-------------------------------------------------: | :----------------------------------------------: |
| <img src="Screenshots/mypage_12.gif" width = "400"> | <img src="Screenshots/search.gif" width = "400"> |

# Features

- Python
- Flask
- Flask-SQLAlchemy
- sqlite3
- html
- css
- js

I've used Flask web framework based in Python its was necessary flask-sqlalchemy for manage SQL database with sqlite . I created my own class to do basic actions in the database such as get data , insert , update and delete.
also i did the necessary javascript code at script.js file and css code at css/style.css

## My code is divided into three main sections

- pages

```
index
user_home
explore
user
mypage
search
about

```

- usre actions

```
signup
login
logout
get_login_data
edit_my_data
follow_unfollow
is_follow
```

- images actions

```
saveimage
get_image
add_image
edit_image
delete_image
add_remove_like
add_like_unlike_image

```
