from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import dbhelper
import enum

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due_by' : fields.Date(required=True, description='Due date of the task'),
    'status' : fields.String(description='The task status',  enum = ['not_started', 'in_progress', 'finished'])
})


class TodoDAO:
    def get(self):
        result = dbhelper.fetchAll()
        if len(result) > 0:
            return result
        api.abort(404, "Todo {} doesn't exist".format(id))

    def get(self, id):
        result = dbhelper.fetchById(id)
        if len(result) > 0:
            return result
        api.abort(404, "Todo {} doesn't exist".format(id))

    def due(self, date):
        result = dbhelper.fetchDue(date)
        if len(result) > 0:
            return result
        api.abort(404, "Todo {} doesn't exist".format(id))

    def overDue(self):
        result = dbhelper.fetchOverDue()
        if len(result) > 0:
            return result
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        result = dbhelper.addTodo(todo['task'], todo['status'], todo['due_by'])
        if result:
            return {'result' : 'Task addition successful'}
        return { 'result' : 'Task addition failed' }, 400

    def update(self, id, data):
        todo = data
        result = dbhelper.addTodo(todo['task'], todo['status'], todo['due_by'], id)
        if result:
            return {'result' : 'Task updation successful'}
        return { 'result' : 'Task updation failed' }, 400

    def delete(self, id):
        result = dbhelper.deleteById(id)
        if result:
            return {'result' : 'Task deleted successfully'}
        return { 'result' : 'Task deletion failed' }, 500


DAO = TodoDAO()

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return dbhelper.fetchAll()

    @ns.doc('create_todo')
    @ns.expect(todo)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload)

@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(int(id))

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        return DAO.delete(id)

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)

# /due?due_date=yyyy-mm-dd
@ns.route('/due')
@ns.response(404, 'No todo found for specified date')
@ns.doc(params={ 'due_date': '<due>' })
class TodoDue(Resource):
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks due on given date'''
        due = request.args.get('due_date')
        return DAO.due(due)

# "GET /overdue"
@ns.route('/overdue', endpoint='overdue')
@ns.response(404, 'Error - see debugger logs')
class Overdue(Resource):
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all overdue tasks'''
        return DAO.overDue()


if __name__ == '__main__':
    app.run(debug=True)