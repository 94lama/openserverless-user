## API endpoints

List of all endpoints used by the app with a JSON format.
Variables follows the following schema:
- user: <User> 


### listuser [GET]

'''http
GET /api/v1/kube/listuser
'''
Returns a list of all <user> in JSON format

'''JSON
{"output": [users]}
'''


### adduser [PUT]

'''http
POST /api/v1/kube/adduser
'''
Adds a new user to the Kubernetes cluster. User data are given by a form 
adduser(<user>): void


### deleteuser [DELETE]

'''http
DELETE /api/v1/kube/deleteuser
'''
Removes a user to the Kubernetes cluster. The body contains the user["name"] value.

