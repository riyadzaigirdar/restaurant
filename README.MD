
### CODING ASSIGNMENT

#### TO START THE PROJECT AUTOMATICALLY SIMPLE RUN (declaimer: database vol added in project directory)

	docker-compose up
 
#### Admin credentials
   
        email => admin@gmail.com 
        password => 12345

#### ENVIRONMENT VARIABLES ARE
      
       DB_NAME
       DB_USER
       DB_PASS
       DB_HOST
       DB_PORT
       REDIS_HOST
       REDIS_PORT
       JWT_SECRET   

#### TO RUN THE PROJECT MANUNUALLY SIMPLE SET UP THE VIRTUAL ENVIRONEMENT

   1. python -m venv venv

   2. source ./venv/bin/activate

   3. python manage.py runserver

#### TO RUN ALL THE TEST TOGERTHER

   python manage.py test
   

