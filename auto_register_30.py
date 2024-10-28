import requests
from bs4 import BeautifulSoup

# URL
BASE_URL = "http://127.0.0.1:5000" # Replace with your base URL
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
REALNAME_URL = f"{BASE_URL}/edit"
LOGOUT_URL = f"{BASE_URL}/logout"


name_dict = [
    "Harry", "Hermione", "Ron", "Ginny", "Neville", "Luna", "Draco", "Fred", "George", "Severus", 
    "Sirius", "Remus", "Albus", "Minerva", "Rubeus", "Tom", "Cedric", "Fleur", "Viktor", "Nymphadora", 
    "Bellatrix", "Lucius", "Molly", "Arthur", "Percy", "James", "Lily", "Cho", "Horace", "Dolores"
] # repalce to the name you like

def register_user(session, username, password):
    
    data = {
        "username": username,
        "password": password,
        "confirmation": password
    }
    
    response = session.post(REGISTER_URL, data=data)
    return response

def login_user(session, username, password):
    
    data = {
        "username": username,
        "password": password
    }
    response = session.post(LOGIN_URL, data=data)
    return response

def input_realname(session, realname):
    
    data = {
        "realname": realname
    }
    response = session.post(REALNAME_URL, data=data)
    return response

def logout_user(session):
    
    response = session.get(LOGOUT_URL)
    return response

def register_30_users():
    for i, realname in enumerate(name_dict):
        username = f"user{i+1:02d}"
        password = "abc"
        
        with requests.Session() as session:
            register_response = register_user(session, username, password)
            if register_response.status_code != 200:
                print(f"Failed to register {username}")
                continue
            
            login_response = login_user(session, username, password)
            if login_response.status_code != 200:
                print(f"Failed to log in {username}")
                continue
            
            realname_response = input_realname(session, realname)
            if realname_response.status_code == 200:
                print(f"Successfully registered and set realname for {username}")
            else:
                print(f"Failed to set realname for {username}")
                
            logout_response = logout_user(session)
            if logout_response.status_code == 200:
                print(f"Successfully logged out {username}")
            else:
                print(f"Failed to log out {username}")
            
if __name__ == "__main__":
    register_30_users()