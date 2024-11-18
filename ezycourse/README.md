<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [EzyCourse Python SDK](#ezycourse-python-sdk)
  - [Installation](#installation)
  - [Login](#login)
    - [Do Login](#do-login)
    - [Login from cookies](#login-from-cookies)
  - [Persisting the session](#persisting-the-session)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# EzyCourse Python SDK


## Installation

```bash
pip install ezycourse
```

## Login

### Do Login

First, you need to login to your EzyCourse account. You can do this by running the following command:

The library support multiple sites, you can provide the url of the site you want to login to. For example: `https://app.ezyeducation.com`.

```python
from ezycourse.sdk import Auth

user = input("Enter your username: ")
password = input("Enter your password: ")
site = input("Enter your site: ")

auth = Auth()
auth.do_login(site, user, password)

# Check if login is successful
if auth.is_logged:
    print("Login successful")
else:
    print("Login failed")
```

### Login from cookies

If you have already logged in to your account and have the cookies, you can use the following code to login:

```python
from ezycourse.sdk import Auth

cookies = "NEXT_LOCALE_V2=xxxxxx%3D%3D; swuid=s%xxxxxxxxx; zabUserId=xxxxx; zps-tgr-dts=xxxx; _gcl_au=xxxx; _ga_8RQEBBFXT4=xxxx; _ga=xxxx; __stripe_mid=xxxx; crisp-client%2Fsession%2Fxxxxxx; zabHMBucket=xxxx; zpsfa_8o1PxPY=xxxxx; __stripe_sid=xxxx"
site = input("Enter your site: ")

auth = Auth()
auth.save_session_cookie(site, cookies)

# Check if login is successful
if auth.is_logged:
    print("Login successful")
else:
    print("Login failed")
```

### Persisting and restoring the session

The library will keep the session in the user's home directory. You can use the following code to save the session to a file and load it later:

```python
from ezycourse.sdk import Auth

user = input("Enter your username: ")
password = input("Enter your password: ")
site = input("Enter your site: ")

auth = Auth()
auth.do_login(site, user, password)

# Saving the session at the user's home directory
auth.save()

# Check if login is successful
if auth.is_logged:
    print("Login successful")
else:
    print("Login failed")

# Restoring the session
auth = Auth()
auth.restore()

# Check if login is successful
if auth.is_logged:
    print("Login successful")
else:
    print("Login failed")

```


## Communities

You can manage the communities using the library.

### List all communities

```python
from ezycourse.sdk import Auth, Communities

auth = Auth()
auth.restore()

for community in Communities(auth).list():
    print(community)
```

### Get a community

```python
from ezycourse.sdk import Auth, Communities

community_id = int(input("Enter the community id: "))

auth = Auth()
auth.restore()
communities = Communities(auth)
community = communities.get(community_id)

print(f"\tTitle: {community.title}")
print(f"\tDescription: {community.short_description}")
print(f"\tMembers: {community.total_members}")
print(f"\tPricing: {community.pricing.price}")
print('\n')
```

## Community Spaces

A space is a concept community content. When you enter on a community, you will see the spaces. You can see a community like a channel inside a community.

### List all spaces

```python
from ezycourse.sdk import Auth, Communities

community_id = int(input("Enter the community id: "))

auth = Auth()
auth.restore()
communities = Communities(auth)

for space in communities.get(community_id).list_spaces():
    print(f" - [{space.identifier}] {space.name}")
```

### List all posts in a space

A space contains posts. You can list all the posts in a space using the following code:

```python
from ezycourse.sdk import Auth, Communities

community_id = int(input("Enter the community id: "))
space_id = int(input("Enter the space id: "))

auth = Auth()
auth.restore()
communities = Communities(auth)

for post in communities.get(community_id).get_space(space_id).list_posts():
    print(f"  ID: {post.identifier}")
    print(f"  Title: {post.title}")
    print(f"  Likes: {post.likes}")
    print(f"  Created at: {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Updated at: {post.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'-' * 60}")
```

### Create a new post in a space

You can create a new post in a space using the following code:

```python
from ezycourse.sdk import Auth, Communities

community_id = int(input("Enter the community id: "))
space_id = int(input("Enter the space id: "))

auth = Auth()
auth.restore()
communities = Communities(auth)
space = communities.get(community_id).get_space(space_id)

# Ask for post title and content
content = input('Content')

space.create_post(content)
```

> Note 1: The content must be a simple text. The library does not support markdown or HTML.
> Note 2: If you include a link, the library will automatically download the metadata of the link and include it in the post.

## Courses

You can manage the courses using the library.

### List all courses with statistics

```python
from ezycourse.sdk import Auth, Courses

community_id = int(input("Enter the community id: "))
space_id = int(input("Enter the space id: "))

auth = Auth()
auth.restore()

for course, statistics in Courses(auth).list_courses():
    print(
      (
            f" - [{course.identifier}] {course.title} - ({statistics.total_enrollments} Enrollments | {statistics.total_lessons} Lessons " 
            f"| {statistics.total_reviews} Reviews | {statistics.total_orders} Orders)"
      )
    )
    print()
```

### Get a course

```python
