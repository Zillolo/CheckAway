import web
from modules import clist


"""
The Index class represents the homepage of the app.
"""
class Index:

    """
    Renders the homepage of the app.
    """
    def GET(self):
        return render.index()

render = web.template.render('templates/', base='layout')

"""
Defines the url this module responds to.
"""
urls = (
    '/', 'Index',
    '/List', clist.app
)

app = web.application(urls, locals())

if __name__ == "__main__":
    app.run()
