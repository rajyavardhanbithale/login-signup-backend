import random
import time 
import string
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
dev = os.getenv("DEV")

def otp_expire(minutes):
    return time.time() + (minutes*60)

def otp_generate(size):
    if(dev=="True"):
        return 111
    otp = int(''.join(random.choices(string.digits, k=size)))
    return otp


def otp_verify(collection,check_user,user):
    if(check_user):
        if(check_user["is_verified"]=="false"):
            if(check_user["otp_verification"]["otp"]==user.otp and time.time()<check_user["otp_verification"]["expiration_time"]):
                update_data = collection.update_one({"username":user.username},{
                    "$set":{
                        "is_verified": "true"
                    }
                })
                
                
                
                if update_data.raw_result['nModified'] == 1:
                    otp_delete = collection.update_one({"username":user.username},{
                        "$unset":{
                            "otp_verification":""
                        }
                    })
                    raise HTTPException(status_code=200,detail="user verified") 
                
            else:
                raise HTTPException(status_code=401,detail="invalid otp" if check_user["otp_verification"]["otp"]!=user.otp else "time expire")
        else:
            raise HTTPException(status_code=200,detail="user already verified")
        
    raise HTTPException(status_code=401,detail="user verification fail")


def check_if_user_verified(check_user):
    if(check_user):
        if(check_user["is_verified"]=="true"):
            return True
    
    if(check_user==None):
        return "none_type"
    
    return False