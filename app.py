import falcon
from config import MongoDBConfig
from repository import UserRepository
from resource import UserResource

mongo_config=MongoDBConfig()
db=mongo_config.get_database()
user_repository=UserRepository(db)
app=falcon.App()

user_resource=UserResource(user_repository)
app.add_route('/users',user_resource)


