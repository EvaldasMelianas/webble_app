
# Webble webapp

The project was developed as the final assignement for my CodeAcademy beginner level Python course.

I created this project using Django framework. I utilized PyMuPDF and Pillow libraries to develop an application that enables users to read books directly on the webpage. Additionally, the app includes features such as the ability to leave reviews, create bookmarks, and conveniently track reading progress, allowing users to easily resume from where they left off.

There are two apps in the projects, "webble" that deals with the books and "user", which contains the views and logic behind user progress, reviews and bookmarks.

The model objects are created via the Django Administration page and a staff group was created to restrict access to only the Book, Genre and Author models.

Book model - the cover image and summary are automatically populated. Cover image.JPG is created from the first page of the uploaded PDF book. The description is scrapped via Wikipedia API.

Author model - the portrait and bio attributes are automatically populated. Both are scrapped via the Wikipedia API and saved within the database.

## Usage

Home page - displays suggestions of available books (up to 6) based on 3 random genres.

Books page - displays all available books in the database.

Authors page - displays all available authors in the database.

Genres page - access through the navbar dropdown selection, displays books as per the selected Genre.

Search input - displays books and authors that fit the keyword searched.

Detail pages - each image for Author and Book are clickable to access the objects detail page.

Book detail page - the page has two buttons that either direct you to a review form or a view that displays a single page of the selected book object.

Read book page - displays the image of the page and allows you to save bookmarks on the page you are currently on. It automatically saves the highest page visited of the book to your users progress model.

User page - contains the bookmarks and reader progress data, allows for quick access of the captured pages and delete them one by one.

## Authors

- [@Evaldas Melianas](https://www.linkedin.com/in/evaldas-melianas-9387a5261)


## Demo

![Webble](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjVtbnB3dzlyY292dmhhZGszZGRvcDNkMDR1dnR3M2tuOWFhMXQ2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t20pFxfyhLralVnnHC/giphy.gif)
