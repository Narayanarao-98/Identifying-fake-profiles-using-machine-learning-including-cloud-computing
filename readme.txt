1. here we are use RDS database instance, Create RDS instance database correctly and use it

 -----> put VPC security public access "on"
 -----> add In-bound runle "type:mysql, anywhere IPV4, anywhere" 

2. Change settings.py database

3. DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your database name',  # The name of the database you created in RDS
        'USER': 'Your Master name',  # Your master username
        'PASSWORD': 'your password',  # The password you set during RDS setup
        'HOST': 'you instance rds end point',  # The endpoint of your RDS instance
        'PORT': '3306',  # Default MySQL port
    }
 }


4. migrate the data

