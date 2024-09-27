import json
import os

from pymongo.errors import DuplicateKeyError

from model import UserModel
class UserRepository:
    def __init__(self,db):
        self.collection=db['user']
        self.collection.create_index([("email", 1)], unique=True)

    def create_user(self,user_data:UserModel):
        user_dict=user_data.to_dict()
        try:
            result = self.collection.insert_one(user_dict)
            return result.inserted_id
        except DuplicateKeyError:
            raise ValueError(f"Email '{user_data.email}' is already in use.")

    def get_user_by_email(self,email):
        return self.collection.find_one({"email": email}, {"_id": 0})


    def write_user_to_json(self, user_data: UserModel):
        # Check if the file exists and read existing data
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as json_file:
                try:
                    data = json.load(json_file)  
                except json.JSONDecodeError:
                    data = []  
        else:
            data = []  

        # Append the new user data
        data.append(user_data.to_dict())

        # Write the updated list back to the file
        with open('user_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
