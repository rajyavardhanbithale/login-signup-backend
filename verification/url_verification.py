from cryptography.fernet import Fernet
import json
import base64
from fastapi import HTTPException
import time

def build_url_for_verification(key:str,username:str,email:str,exp_time:int) -> str:
    fernet = Fernet(key)
    user_dict = {
        "username" : username,
        "email" : email,
        "exp_time" : exp_time
    }
    user_dict_str = json.dumps(user_dict)

    encrypt_user_information = fernet.encrypt(user_dict_str.encode())
    
   

    return base64.b64encode(encrypt_user_information)


def decrypt_fernet(key:str,enc_str:str):
    try:
        fernet = Fernet(key)
        load_bytes = base64.b64decode(enc_str.encode('utf-8'))
        decrypted_data = fernet.decrypt(load_bytes).decode('utf-8')
        return json.loads(decrypted_data)
    except:
        raise HTTPException(status_code=401,detail="invalid url or url expire")
    


def user_url_verification(collection,check_user,decrypted_data):
    if(check_user):
        if(check_user["is_verified"]=="false"):
            if(time.time()<check_user["otp_verification"]["expiration_time"]):
                update_data = collection.update_one({"username":decrypted_data["username"]},{
                    "$set":{
                        "is_verified": "true"
                    }
                })
                
                
                
                if update_data.raw_result['nModified'] == 1:
                    otp_delete = collection.update_one({"username":decrypted_data["username"]},{
                        "$unset":{
                            "otp_verification":""
                        }
                    })
                    raise HTTPException(status_code=200,detail="user verified") 
                
            else:
                raise HTTPException(status_code=401,detail="invalid url or url expire")
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



# key = b"K3nYOXKcW7BIVmCYMmrvNKTw5YShzlRtOT-3-qTK4Gk="
# run = build_url_for_verification(
#     key=key,
#     username="rage",
#     email="rage@rage.com",
#     otp=58963,
#     exp_time= 15235
#     )

# run =b"Z0FBQUFBQmxPb09GTmxnVXI1MlpEcTQwWGtIbGVMd2VlVkQxa0d4anUzU09jU0UxbHRRLWh3bElwNjF2Unp2X083akJNcFlPMnVHekFpX1VLM0JmSHEybWpPRWcxLVR0UkJPMXo1ZWZDNGFnWEkwS3hQWWVMdGJvU3VlZVpaRFFERUZERkQ5QW5NYXg4YjllalhMdnhSOFF3LTFKdldVTlNQbGlfM2FTRG1BZy10dmtHeGJka3M4PQ=="
# run1 = decrypt_fernet(
#     key=key,
#     enc_str= run
#     )

# print(run1)