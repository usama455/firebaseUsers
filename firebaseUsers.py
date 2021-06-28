import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


cred = credentials.Certificate("PATH TO FIREBASE SECRET KEY1")
firebase_admin.initialize_app(cred)


db = firestore.client()
userDataFromExcel = pd.read_excel(r'./usersFile.xlsx')


emailList = userDataFromExcel['Emails'].tolist()
nameList = userDataFromExcel['Names'].tolist()
passwordList = userDataFromExcel['Passwords'].tolist()

#zip lets you iterate over multiple lists , but only up to the number of elements of the smallest list
def createUser(user):
    try:
        newUser = auth.create_user(
            email=user['email'],
            email_verified=True,
            password=user['password'],
            disabled=False,
            displayName=user['name']

)
	userData=user
        userData['uid'] = '{0}'.format(newUser.uid)

        print("ADDED USER")
        return addUserInDb(userData)
    except Exception as e:
        print("ERROR in USER")
        return {"error": e}


def addUserInDb(userData):
# saving added user in the users collection in firestore 
    usersCollection = db.collection(u'users').document(userData['uid'])
    try:
        usersCollection.set({
            u"email": userData["email"],
            u"password": userData["password"],
            u"name": userData["name"]
      })

        print("Adding in DB")
        return {"success": 1,
                "data": userData}
    except Exception as e:
        print("ERROR in DB", e)
        return {
            "success": 0,
            "error": "db"}



for name,email,password in zip(nameList,emailList,passwordList):
    user = {
        "name": name,
        "email": email,
        "password": password
    })
    createUser(user)


