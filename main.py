from fastapi import FastAPI,HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymongo

from dotenv import load_dotenv
import os
import time


from validation import validate
from message import message
from verification import otp_manager as otp
from verification import url_verification 

load_dotenv()
dev = os.getenv("DEV")
load_key = os.getenv("VERIFICATION_KEY")
host =  os.getenv("HOST")
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number:str

    username:str = None
    password: str

    ip_creation: str = None

class GetUser(BaseModel):
    username: str
    password: str

class UpdateUser(BaseModel):
    username:str  
    old_password: str 
    new_password : str

class VerifyOTP(BaseModel):
    username: str
    password: str
    otp: int
    

    

# MONGO DB START
password = os.getenv("DB_PASSWORD")
username = os.getenv("DB_USERNAME")
if dev == "False":
    print("[**] Production")
    client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@userdata.pbqqmqu.mongodb.net/?retryWrites=true&w=majority")
else:
    print("[*] DEV")
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    
db = client["userData"] 

collection = db["user_data"]
collection_delete = db["user_delete"]
# MONGO DB END


# Routes
routes = [
    "/",                #[0]
    "/login",           #[1]
    "/signup",          #[2]
    "/delete",          #[3]
    "/update/password", #[4]
    "/users",           #[5]
    "/otp/verify",      #[6]
    "/otp/resend"       #[7]
] 

# Save IP
def save_ip(data_name:str,cup:bool, request:Request):
     # Saving IP
    if cup:    
        client_host = request.client.host
        update_data = {"$push": 
            {
                f"ip.{data_name}.timestamp":time.time(),
                f"ip.{data_name}.ip":client_host,
            }
        }
        result = collection.update_one({"_id":cup['_id']}, update_data)
 
def otp_expire(minutes):
    return time.time() + (minutes*60)



# Home
@app.get("/") #routes[0]
async def home():
    
    return message.message


# Login
@app.post("/login") #routes[1]
async def login(user:GetUser,requst:Request):

    check_username_password = collection.find_one({
            "username":user.username,
            "password":user.password                         
    }) 
    
    save_ip(data_name="ip_login",cup=check_username_password,request=requst)      

    if check_username_password and otp.check_if_user_verified(check_user=check_username_password):
        raise HTTPException(status_code=200,detail="login OK")
    
    raise HTTPException(status_code=401,detail="invalid [username : password] or user does not exsist or user not verified  ")




# Signup
@app.post("/signup") #routes[2]
async def signup(user:User,request:Request):

    client_host = request.client.host

    time_exp = otp.otp_expire(5)
    gen_otp = otp.otp_generate(5)

    validate.validate_data(user)
    valid = validate.return_data(
        data=user,
        ip=client_host,
        timestamp=time.time(),
        otp=gen_otp,
        exp_time= time_exp
    )

    is_user_exist = collection.find_one({"username":user.username})

    if is_user_exist:
       raise HTTPException (status_code=422,detail= f"User with username '{user.username}' exists.") 

    collection.insert_one(valid)      
    
    build_verification_url = url_verification.build_url_for_verification(key=load_key,username=user.username,email=user.email,exp_time=time_exp).decode()

    msg = {
        "otp": gen_otp,
        "url": host+ f"otp/verify/{build_verification_url}"
    }

    return {"message":f"user created{msg}"}


# Delete
@app.delete("/delete") #routes[3]
async def delete(user:GetUser,request:Request):
    check_username_password = collection.find_one({
            "username":user.username,
            "password":user.password                         
    })
    
    is_verified = otp.check_if_user_verified(check_user=check_username_password)
    
   
   
    if(check_username_password and is_verified):
        collection_delete.insert_one({
                "timestamp":time.time(),
                "username":user.username,
                "ip": request.client.host
        })
    
    if(is_verified):
        delete_user = collection.delete_one({
                "username":user.username,
                "password":user.password

        })

        if delete_user.raw_result["n"] ==1:
            return{"detail":"user deleted"}
    
    raise HTTPException(status_code=401,detail="invalid [username : password] or user does not exsist ")

# Update 
@app.put("/update/password") #routes[4]
async def update(user:UpdateUser,request:Request):
    check_username_password = collection.find_one({
            "username":user.username,
            "password":user.old_password                         
    })

    is_verified = otp.check_if_user_verified(check_user=check_username_password)

    if check_username_password and is_verified:
        # Setting Old Password In DB
        update_data = {"$set": {"old_password": user.old_password}}
        result = collection.update_one({"username":user.username}, update_data)

        if check_username_password["password"] != user.new_password:        
            update_data = {"$set": {"password": user.new_password}}
            result = collection.update_one({"username":user.username}, update_data)
             
            if result.raw_result['nModified'] == 1:
                save_ip(data_name="ip_update",cup=check_username_password,request=request)
                return {"detail":"password updated"}
        else:
             raise HTTPException(status_code=400,detail="new password cannot be same as new")

    raise HTTPException(status_code=401,detail="invalid [username : password] or user does not exsist")


# User
@app.get("/users") #routes[5]
async def get_users():
    users = collection.find()

    user_data = [
        {**user, '_id': str(user['_id'])} for user in users
    ]

    if not user_data:
        raise HTTPException(status_code=404, detail="No users found")

    return user_data  
   


@app.post("/otp/verify") #routes[6]
async def verify_otp(user:VerifyOTP):
    check_user = collection.find_one({
        "username": user.username,
        "password": user.password
    })
    
    otp.otp_verify(collection=collection,check_user=check_user,user=user)

    return ""

@app.get("/otp/verify/{enc_url}") #routes[6]
async def verify_user_with_url(enc_url:str):
    decrypted_data = url_verification.decrypt_fernet(load_key, enc_url)
    
    check_user = collection.find_one({
        "username": decrypted_data["username"],
        "email": decrypted_data["email"]
    })

    
    url_verification.user_url_verification(collection=collection,check_user=check_user,decrypted_data=decrypted_data)


    return ""



@app.post("/otp/resend") #routes[7]
async def resend_otp(user:GetUser):
    check_username = collection.find_one({
            "username":user.username,
            "password":user.password                         
    }) 
    
    
    if(check_username):
        if(check_username["is_verified"]=="false"):
            update_otp = collection.update_one(
                {"username":user.username},
                {
                    "$set":{
                        "otp_verification.otp":otp.otp_generate(5),
                        "otp_verification.expiration_time":otp.otp_expire(5)
                    }
                })

            if update_otp.raw_result['nModified'] == 1:
                raise HTTPException(status_code=200,detail="otp send successfully")
            
        else:
            raise HTTPException(status_code=200,detail="user already verified")
        
    raise HTTPException(status_code=401,detail="user doesn't exist")