
# Webble project

The project was developed as the final assignment for my CodeAcademy beginner Python course.

The application is build to serve as a web library. 
Users can navigate through the available database entries to find authors and books they are interested in. 
The application tracks their reading progress and enables them to leave  bookmarks for easy access later.

## Views:
There are several defined views in the code:

'Webble' app views:
1. HomeView - displays the random genres and books associated with them as suggestions.
2. AllAuthorsView - displays all available authors in the database.
3. AllBookView - displays all available books in the database.
4. GenreListView - displays books filtered to have the selected genre.
5. BookDetailView - displays details for the specified book object.
6. AuthorDetailView - displays details for the specified author object.
7. SearchBookView - displays books and authors that match the searched string.
8. ReadBookView - displays the specified page of the accessed book. Saves readers progress in the background.

'User' app views:
1. RegisterView - displays registration form and validates it.
2. UserDetails - allows the user to access and delete his reading progress, bookmark entries.
3. CreateReview  - displays review form and validates it.
4. UpdateReview - retrieves existing review and allows for it to be modified.
5. DeleteReview - allows user to delete their review.

## Demo

![Webble](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjVtbnB3dzlyY292dmhhZGszZGRvcDNkMDR1dnR3M2tuOWFhMXQ2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t20pFxfyhLralVnnHC/giphy.gif)

## Requirements

1. Python 3.11.1
2. Django 4
3. SQLite 3.12

## Setting up
1. Clone the project.

```
git clone https://github.com/psysheep/webble_app.git
```
2. Activate the virtual environment.
```
source venv/bin/activate
```
   On Windows:
```
venv\scripts\activate
```
   On Linux:
```
source venv/bin/activate
```
3. Install required packages.
```
pip install -r requirements.txt
```
4. Create the database - note that this is running on SQLite by default, you will have to download and install it.

```
py manage.py makemigrations
py manage.py migrate
```
5. Create superuser for model updates and the ability to create user groups that modify access in the admin panel.
```
py manage.py createsuperuser
```
6. Run the application.
```
py manage.py runserver
```

## Admin panel
The database is 'controlled' through the django admin panel " < HOST >/admin) " address.
By default only the superuser has the rights to fully access the admin panel.
We can access the 3 links defined in the dropdown that allow us to quickly access the 3 main models.

<img src="https://i.imgur.com/0pt6hQt.png" width="30%">

Users can be modified to have staff permissions in order to enable their access to the Django admin panel.
Take note that rights have to be assigned in order for said user to access the desired views.

The code was written to enable staff to access the Book, Author and Genre models.

<img src="https://i.imgur.com/6EkL8pI.png" width="70%">

Users can be accessed through the " < HOST >/admin/auth/user " address.



## Authors

- [@Evaldas Melianas](https://www.linkedin.com/in/evaldas-melianas-9387a5261)
