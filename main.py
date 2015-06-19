import pymongo as mongo

import web

render = web.template.render('templates/', base='layout')

urls = (
    '/', 'Index',
    '/(.*)', 'List'
)

class Index:
    def GET(self):
            return render.index()

class List:
    def GET(self, id):
            client = mongo.MongoClient('localhost', 27017)
            db = client.check
            collection = db.lists

            try:
                document = collection.find_one({'id' : int(id)})
            except ValueError:
                return render.error(id)

            print(document['id'])
            print(document['collaborators'][0]['name'])

            return render.list(document)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
