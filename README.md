# DRF API PAINT PICTURE


**Developer: Bilan Mykhailo**

[Live link](https://paint-picture-backend-6b0b98f6459e.herokuapp.com/)

This repository contains the API set up using Django REST Framework for the Paint Picture front-end application ([repository here](https://github.com/Belan-Mihail/paint_picture) and [live website here](https://paint-picture-frontend-29a39ba64062.herokuapp.com/))

## Table of Contents
  - [User Stories](#user-stories)
  - [Database](#database)


## User Stories
The back-end section of the project focuses on its administration side and covers one user story:
- As an admin, I want to be able to create, edit and delete the users, pictures, comments, likes, followers, plans and wallitems, so that I can have a control over the content of the application and remove any potential inappropriate content.


## Database

The following models were created to represent the database model structure of the application:
<img src="docs/readme/database-diagram.jpg">

### User Model

- The User model contains information about the user. It is part of the Django allauth library.
- One-to-one relation with the Profile model owner field
- ForeignKey relation with the Picture model owner
- ForeignKey relation with the Plan model owner
- ForeignKey relation with the Comment model owner
- ForeignKey relation with the Wallitem model owner
- ForeignKey relation with the Likes model owner
- ForeignKey relation with the Followers model owner

### Profile Model

- The model was created to create/delete profile for the user and to provide user with the ability to view, edit own profile on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True

- updated_at
    - type: DateTimeField
    - validation: auto_now=True

- name
   - type: CharField
   - validation: max_length=255, blank=True 

- content
   - type: TextField
   - validation: blank=True 

- image
   - type: ImageField
   - upload_to='images/', default='../default_profile_rg7ho0'

- greeting
   - type: CharField
   - validation: max_length=25, blank=True


### Picture Model

- The model was created to provide the user with the ability to create, view, edit and delete pictures on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True

- updated_at
    - type: DateTimeField
    - validation: auto_now=True

- title
   - type: CharField
   - validation: max_length=255 

- description
   - type: TextField
   - validation: blank=True 

- image
   - type: ImageField
   - validation: upload_to='images/', default='../default_post_x6zdvo', blank=True

- picture_category
   - type: CharField
   - validation: max_length=32, choices=category_choices, default='other' 

- Following categories choices were added for user to select for an pictures:

category_choices = 
            ('landscapes', 'landscapes'),
            ('animals', 'animals'),
            ('plants', 'plants'),
            ('abstraction', 'abstraction'),
            ('other', 'other'),
        

### Plan Model

- The model was created to provide the user with the ability to create, view, edit and delete plans on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE, related_name="plan_owner"

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True

- updated_at
    - type: DateTimeField
    - validation: auto_now=True

- plans_title
   - type: CharField
   - validation: max_length=255, blank=False

- plans_description
   - type: TextField
   - validation: max_length=300, blank=False 

- plans_date
   - type: DateField
   - validation: -

- until
   - type: BooleanField
   - validation: default=False 


### Comment Model

- The model was created to provide the user with the ability to create, view, edit and delete comments on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE 

- picture
   - type: ForeignKey(Picture)
   - validation: on_delete=models.CASCADE 

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True

- updated_at
    - type: DateTimeField
    - validation: auto_now=True

- content
   - type: TextField
   - validation: - 



### WallItem Model

- The model was created to provide the user with the ability to create, view, edit and delete wallitem on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE,
   related_name="wallitem_owner" 

- profile
   - type: ForeignKey(Profile)
   - validation: on_delete=models.CASCADE, blank=True, null=True 

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True

- updated_at
    - type: DateTimeField
    - validation: auto_now=True

- message
   - type: TextField
   - validation: blank=False, null=False


### Likes Model

- The model was created to provide the user with the ability to create, view and delete likes on the site. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE,
   

- picture
   - type: ForeignKey(Picture)
   - validation: on_delete=models.CASCADE

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True


### Followers Model

- The model was created to provide the user with the ability to use followers functionality. this model contains the following fields

- owner
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE,
    related_name='following'
   

- followed
   - type: ForeignKey(User)
   - validation: on_delete=models.CASCADE, related_name='followed'

- created_at
   - type: DateTimeField
   - validation: auto_now_add=True


## Technologies Used

### Languages & Frameworks

- Python
- Django

### Libraries & Tools

- [Django REST Framework](https://www.django-rest-framework.org/) was used this to build the back-end API
- [Django AllAuth](https://django-allauth.readthedocs.io/en/latest/index.html) was used for user authentication
- [Git](https://git-scm.com/) was used this for version control and to push the code to GitHub
- [GitHub](https://github.com/) was used this as a remote repository to store project code
- [Cloudinary](https://cloudinary.com/) was used to store default images for profiles and pictures
- [Gitpod](https://gitpod.io/workspaces) was used this to host a virtual workspace
- [Heroku](https://heroku.com) was used this was used to deploy the project into live environment
- [ElephantSQL](https://www.elephantsql.com/) was used as the deployed project on Heroku uses an ElephantSQL database
- [CI Python Linter](https://pep8ci.herokuapp.com/) was used for validation of python files.
- [Psycopg2](https://www.psycopg.org/docs/) was used as a PostgreSQL database adapter for Python
- [Pillow](https://pillow.readthedocs.io/en/stable/) was used for image processing and validation

## Agile 

- create Issue Template
   <details><summary>Issue template</summary>
   <img src="docs/readme/agile/issue-template.jpg">
   </details>

- create Milestones
   <details><summary>Milestones</summary>
   <img src="docs/readme/agile/milestones.jpg">
   </details>
- create project [Link to project](https://github.com/users/Belan-Mihail/projects/7)
- create issues (based on the template). A total of 48 issues were created
   <details><summary>Issues</summary>
   <img src="docs/readme/agile/issues.jpg">
   </details>

- create main labels and mark issues in accordance with Moscow Prioritisation
   <details><summary>Labels</summary>
   <img src="docs/readme/agile/labels.jpg">
   </details>

- create Kanban Board to visualize the process of completing tasks
   <details><summary>Kanban Board</summary>
   <img src="docs/readme/agile/kanban-board.jpg">
   </details>

This project was the second time I used agile development methods. The importance of these principles is beyond doubt. There may have been certain inaccuracies in the use of all the principles of this methodology.

