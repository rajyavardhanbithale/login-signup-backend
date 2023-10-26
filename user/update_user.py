from fastapi import HTTPException
from user import save_ip_address
def updatee_user(check_username_password,collection,user,is_verified,request):
    if check_username_password and is_verified:
        # Setting Old Password In DB
        update_data = {"$set": {"old_password": user.old_password}}
        result = collection.update_one({"username":user.username}, update_data)

        if check_username_password["password"] != user.new_password:        
            update_data = {"$set": {"password": user.new_password}}
            result = collection.update_one({"username":user.username}, update_data)
             
            if result.raw_result['nModified'] == 1:
                save_ip_address.save_ip_address(collection=collection,
                                                data_name="ip_update",
                                                check_username_password=check_username_password,
                                                request=request)      

                
                raise HTTPException(status_code=400,detail="password updated")
        else:
             raise HTTPException(status_code=400,detail="new password cannot be same as new")

    raise HTTPException(status_code=401,detail="invalid [username : password] or user does not exsist")    