# WAC

_STACK DJANGO TEST_

## Starting 🚀

_Basic user management. Allowing to login to the API, as well as to edit the user's profile._

### Installation 🔧

_Basic installation_

```
	git init

	git clone https://github.com/robmonteagudo/api_wac.git

	create virtual env -> virtualenv env --no-site-packages

	activate -> source env/bin/activate

	Install the project dependencies -> pip install -r requirements.txt

	create env variables 	
		export SECRET_KEY='<secret_key>'
		export DEBUG=True
		
	create a postgress variables
		export POSTGRES_DB='<postgres_db>'
		export POSTGRES_USER='<postgres_user>'
		export POSTGRES_PASSWORD='<postgres_password>'
		export POSTGRES_HOST='<postgres_host>'
		export POSTGRES_PORT='<postgres_port>'
		
	create migrations
		python manage.py makemigrations
		
	migrate
		python manage.py migrate
		
	create admin account
		python manage.py createsuperuser
		
	start the development server

		python manage.py runserver
		
	Open localhost:8000 on your browser to view the app.
```

_With Docker_

```
    Create a folder envs
    
    Create a file .django
        Add SECRET_KEY = <secret_key>
        Add DEBUG = True
    
    Create a file .postgres
        POSTGRES_HOST=db
        Add POSTGRES_PORT=<postgres_port>
        Add POSTGRES_DB=<postgres_db>
        Add POSTGRES_USER=<postgres_user>
        Add POSTGRES_PASSWORD=<postgres_password>
    
    Build the container
        docker-compose build
		
    Lift the service
        docker-compose up -d
```


## Running tests ⚙️

_Test profile model_

```
	python manage.py test profiles
```

## End points 🖇️

_Login_
```
	POST - /profiles/login/
	
	Parameters
	    Email*
	    Password*
	
	Response
	    User details
	    Access Token
```

_Create JWT Token_
```
	POST - /api/token/
	Parameters
	    Email*
	    Password*
	
	Response
	    Refresh Token
        Access Token
```

_Refresh JWT Token_
```
	POST - /api/token/refresh/
	Parameters
	    Refresh*
	
	Response
	    Access Token
```

_Edit Profile_
```
	PATCH - Headers with Token* - /profiles/<pk>/ 
	Paramenters
	    Email
	    First_name
	    Last_name
	    Avatar
	Response
	    User details
```

_Change Password_
```
	POST - Headers with Token* - /profiles/password/  
	Paramenters
	    Old Password
	    New Password
	Response
	    Code Status
            Message
```

---
⌨️ con ❤️ por [Roberto Monteagudo Sanz](https://es.linkedin.com/in/roberto-monteagudo-sanz-900b828b) 😊
