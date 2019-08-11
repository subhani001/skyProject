"# skyProject" 
"# skyProject" 

Project Name: skyProject
Application Name: skyTestApp

To test the app
1) Run the server from the command prompt    > python manage.py runserver
2) tkae the server ip address from log of abovee command ... default is http://127.0.0.1:8000
3) Default page is like below... It has users,groups,api links to get users,groups and api(based on ID) pages

Api Root
The default basic root view for DefaultRouter

GET /
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "users": "http://127.0.0.1:8000/users/",
    "groups": "http://127.0.0.1:8000/groups/",
    "api": "http://127.0.0.1:8000/api/"
}

For ex:
i.e. to get ID=1 record type  http://127.0.0.1:8000/api/1
     to get ID=20 record type http://127.0.0.1:8000/api/20

  

4) to insert the records
http://127.0.0.1:8000/addrecs

5) to delete recodds (clear all data)
http://127.0.0.1:8000/delrecs

6) To check all taks information with filled requiredments at http://127.0.0.1:8000/tasks/

7) This project has included static files images,CSS included nin HTML. 

8) This project has instaalled django and djangorestframework.
HOPE YOU LIKE THE RESULT OF POINT 6. :)

Regards
Subhani Shaik
