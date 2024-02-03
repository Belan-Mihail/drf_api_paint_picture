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
