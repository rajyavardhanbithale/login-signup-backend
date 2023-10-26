import time
from fastapi import HTTPException

def delete_user(check_username_password,is_verified,collection_delete,collection,request,user):
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
			raise HTTPException(status_code=200,detail="user deleted")

	raise HTTPException(status_code=401,detail="invalid [username : password] or user does not exsist ")