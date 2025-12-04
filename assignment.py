d={"username":[], "password":[]}

# 1. Define the decorator
def log_execution(func):
    def wrapper():
        print(f"--- Starting {func.__name__} ---")
        func()
        print(f"--- Finished {func.__name__} ---")
    return wrapper

# 2. Use the decorator with the @ symbol
@log_execution
def signup():
    usernm=input("enter username: ")
    passwrd=input("enter password: ")
    d["username"].append(usernm)
    d["password"].append(passwrd)
    print("signup successful")

@log_execution
def login():
    usernm=input("enter username: ")
    passwrd=input("enter password: ")
    if usernm in d["username"] and passwrd in d["password"]:
        print("login successful")
    else:
        print("login failed")
    


while True:
    choice=input("enter your choice (signup/login/exit): ")
    if choice=="signup":
        signup()
    elif choice=="login":
        login()
    elif choice=="exit":
        break
    else:
        print("invalid choice")
