import time

def save_ip_address(collection,data_name:str,check_username_password:bool, request):
     # Saving IP
    if check_username_password:    
        client_host = request.client.host
        update_data = {"$push": 
            {
                f"ip.{data_name}.timestamp":time.time(),
                f"ip.{data_name}.ip":client_host,
            }
        }
        result = collection.update_one({"_id":check_username_password['_id']}, update_data)