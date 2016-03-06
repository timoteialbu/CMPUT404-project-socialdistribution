CMPUT404-project-socialdistribution
===================================


CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

After Cloning
===================================

1)virtualenv venv 

2)source venv/bin/activate 

3) pip install -r requirements.txt

4) python my_setup.py

5) python manage.py migrate && python manage.py collectstatic

6) Create a superuser:    
>python manage.py createsuperuser    

7) python manage.py runserver    

8) Go to  "http://127.0.0.1:8000/admin" and log in using the account you created. Then navigate to 'Sites' and click 'Add'. Create a new site with a Domain Name of : "http://127.0.0.1:8000". Click 'Save' and go back to the list of sites. Click on the site you just created. Look at the address bar and notice the number: "http://127.0.0.1:8000/admin/sites/site/THIS.NUMBER/". Go to mysite/settings.py and look for the SITE_ID variable. Make sure that variable is set to THIS.NUMBER. 

8) then in browser "http://127.0.0.1:8000/"

Or run my_setup.py which does 3 and 5
Contributors / Licensing
========================

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle

