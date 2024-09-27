# resources.py
import falcon
from pydantic import ValidationError

from repository import UserRepository
from model import UserModel

class UserResource:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def on_post(self, req, resp):
        try:
            user_data = UserModel(**req.media)
            user_id = self.user_repository.create_user(user_data)
            self.user_repository.write_user_to_json(user_data)

            resp.status = falcon.HTTP_201
            resp.media = { "message": "User created successfully."}
        except ValidationError as e:
            resp.status = falcon.HTTP_400
            resp.media = {"message": "Invalid Input"}
        except ValueError as e:
            resp.status = falcon.HTTP_409
            resp.media = {"message": str(e)}



    def on_get(self, req, resp):
        email=req.get_param("email")
        # print("onget is called")
        user_data = self.user_repository.get_user_by_email(email)
        if user_data:
            resp.status = falcon.HTTP_200
            resp.media = user_data
        else:
            resp.status = falcon.HTTP_404
            resp.media = {"message": "User not found."}
