from fastapi import HTTPException
from verification import otp_manager as otp

def resend_otp(check_username,collection,user):
    if(check_username):
        if(check_username["is_verified"]=="false"):
            generate_otp = otp.otp_generate(5)
            expire_time = otp.otp_expire(5)
            
            update_otp = collection.update_one(
                {"username":user.username},
                {
                    "$set":{
                        "otp_verification.otp":generate_otp,
                        "otp_verification.expiration_time": expire_time
                    }
                })

            if update_otp.raw_result['nModified'] == 1:
                raise HTTPException(status_code=200,detail="otp send successfully")
            
        else:
            raise HTTPException(status_code=200,detail="user already verified")
        
    raise HTTPException(status_code=401,detail="user doesn't exist")