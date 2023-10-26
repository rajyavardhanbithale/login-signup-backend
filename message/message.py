message = {
        "welcome":"WELCOME TO LOGIN | FASTAPI | @rajyavardhanbithale",
        "login": {
            "info" :"for login use url /login and REQUEST : POST",
            "fields":"username : password",
            "example":{
                "username":"rage",
                "password":"KzkxrdHS2Ed"
            }
        },

        "sign up": {
            "info" : "for sign up use url /signup and REQUEST : POST",
            "fields" : "first_name : last_name : email : phone_number : username : password",
            "example" : {
                
                "first_name": "raj",
                "last_name": "bit",
                "email": "rajbit98@komp.net",
                "phone_number": "+91 9863256875",
                "username": "rage",
                "password": "KzkxrdHS2Ed" 
            
            },
            "more_info" : "password minimum 8 char"
        },

        "update": {
            "info" :"for update use url /update/password and REQUEST : PUT" ,
            "fields": "username : old_password : new_password",
            "example":{
                "username":"rage",
                "old_password":"KzkxrdHS2Ed",
                "new_password": "supereasypassword"
            },
            "more_info":"old_password is current password"
        },

        "delete": {
            "info" : "for deletion of user use url /delete and REQUEST : DELETE | DEL",
            "example":{
                "username":"rage",
                "password":"supereasypassword"
            },
            "fields": "username : password"
        }
    }
