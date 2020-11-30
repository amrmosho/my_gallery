# CS50-Final-Project

This is the Final Project of the CS50 online course series 
"My gallery" is a photosharing site that allows users to upload photos and share with others.

My Gallery lets users do the following:

- Create account and login in to the website.
- Edit his profile anytime he needs.
- Upload photos to share with others.
- Explore other images uploaded from other users.
- Like pictures.
- Follow other users to Follow their latest photos.
- Search for specific photos.

|                     Login                     |                       Pages                       |
| :-------------------------------------------: | :-----------------------------------------------: |
| <img src="Screenshots/login.gif" width="400"> | <img src="Screenshots/pages_3.gif" width = "400"> |

|                      Home                      |
| :--------------------------------------------: |
| <img src="Screenshots/home.gif" width = "800"> |

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

I've used Python based Flask web framework. To deal with the database i have used flask-sqlalchemy to manage SQL database with sqlite . I have created my own class to do basic actions in the database such as get data , insert , update and delete.
also i did the necessary javascript code (script.js file) and css code (css/style.css)

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
