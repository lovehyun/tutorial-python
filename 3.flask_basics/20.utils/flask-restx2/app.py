from flask import Flask
from flask_restx import Api, Namespace, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Demo API', description='A simple demo API')

# Define a model for request and response
model = api.model('Model', {
    'name': fields.String(required=True, description='Name'),
    'age': fields.Integer(required=True, description='Age')
})

# Create a namespace for '/hello' endpoint
hello_ns = Namespace('hello', description='Hello endpoint')
api.add_namespace(hello_ns)

@hello_ns.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world!'}

# Create a namespace for '/user' endpoint
user_ns = Namespace('user', description='User endpoint')
api.add_namespace(user_ns)

@user_ns.route('/')
class UserResource(Resource):
    @user_ns.expect(model)  # Expecting the defined model as request payload
    @user_ns.marshal_with(model)  # Marshal the response using the same model
    def post(self):
        data = user_ns.payload
        return data

if __name__ == '__main__':
    app.run(debug=True)
