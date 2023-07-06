
# Webble webapp

The project was developed as the final assignement for my 6 month CodeAcademy entry level Python course.

I created this project using Django framework. I utilized PyMuPDF and Pillow libraries to develop an application that enables users to read books directly on a webpage. Additionally, the app includes features such as the ability to leave reviews, create bookmarks, and conveniently track reading progress, allowing users to easily resume from where they left off.

The model objects are created via the Django Administration page and a staff group was created to restrict access to only the Book, Genre and Author models.

Book model - the cover image and summary are automatically populated. Cover image.JPG is created from the first page of the uploaded PDF book. The description is scrapped via Wikipedia API.

Author model - the portrait and bio attributes are automatically populated. Both are scrapped via the Wikipedia API and saved within the database.

## Authors

- [@Evaldas Melianas](https://github.com/psysheep)


## Demo

![Webble](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjVtbnB3dzlyY292dmhhZGszZGRvcDNkMDR1dnR3M2tuOWFhMXQ2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t20pFxfyhLralVnnHC/giphy.gif)
