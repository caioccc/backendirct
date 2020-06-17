# Invoice Risk Categorization BACKEND
### Step 1
Install all dependencies (AT THE ROOT OF THE IRCT "SERVER" PROJECT FOLDER)
>pip install -r requirements.txt

### Step 3
> python manage.py makemigrations

### Step 4
> python manage.py migrate

### Step 5
Create a super user
> python manage.py createsuperuser

A form will appear in the terminal, just fill it out.

### Step 6
run the app
>python manage.py runserver 0:8080

or

>python manage.py runserver localhost:8080

### Step 7
open the application in the preferred browser, at https://localhost:8000/admin

### Step 8
Enter with previously created login and password.

### Step 9
Now, at the first login, you must create Roles for your personas. Access the Role link, and create the personas:

- OPERATOR
- CONFIGURATOR
- MANAGER
- AGENT

Type exactly as described, in Uppercase.

### Step 10
Now, at the first login, you must also create some customized users, that is, the personas of the system.
Just go to the CustomUsers link and add a new CustomUser. Remember to create a User with login and password in the form inside CustomUser, as well as Group and link to any Role previously created.

Finally, created the users, access https: // localhost: 4200 (frontend application), and login with one of the previously registered users.