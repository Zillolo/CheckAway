import pymongo as mongo
import random
import uuid
import web
from web import form

render = web.template.render('templates/', base='layout')

urls = (
    '/Check', 'Check',
    '/Create', 'Create',
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

            print(id)
            document = collection.find_one({'id' : id})

            if document is None:
                return render.error(id)

            return render.list(document)

class Create:
    createForm = form.Form(
        form.Textbox('name', form.notnull, description='Name'),
        form.Textarea('collaborators', form.notnull, description='Collaborators'),
        form.Textarea('itemlist', form.notnull, description='Items'),
        form.Hidden('id', value=uuid.uuid4()),
        form.Button('submit', type="submit", description="Create")
    )


    def GET(self):
        return render.create(self.createForm)

    def POST(self):
        client = mongo.MongoClient('localhost', 27017)
        db = client.check
        collection = db.lists

        f = self.createForm()
        if not f.validates():
            pass

        print(f.d.name)
        print(f.d.collaborators)
        print(f.d.items)

        document = {'id' : f.d.id, 'name' : f.d.name,
            'collaborators' : self.parseCollaborators(f.d.collaborators),
            'items' : self.parseItems(f.d.itemlist)}

        print(document)

        collection.insert(document)

        return web.seeother("/%s" % id)

    def parseCollaborators(self, collaborators):
        ret = []

        id = 1
        r = lambda: random.randint(0,255)

        for name in collaborators.split(','):
            ret.append({'id' : id, 'name' : name, 'color' : "#%02X%02X%02X" % (r(), r(), r())})
            id = id + 1
        return ret

    def parseItems(self, item):
        ret = []

        id = 1
        for name in item.split(','):
            ret.append({'id' : id, 'name' : name, 'checked' : []})
            id = id + 1
        return ret

class Check:
    checkForm = form.Form(
        form.Hidden('id'),
        form.Hidden('item'),
        form.Hidden('user')
    )

    def POST(self):
        pass


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
