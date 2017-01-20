import web
import model
import markdown

### Url mappings
urls = (
    '/', 'Index',
    '/design', 'Design',
    '/linux_command', 'LinuxCommand',
    '/linux_software', 'LinuxSoftware',
    '/new', 'New',
    '/edit/(.*)', 'Edit',
    '/delete/(.*)', 'Delete',
    '/view/(.*)', 'Page',
)

### Templates
t_globals = {
    'datestr': web.datestr,
    'markdown': markdown.markdown,
}
render = web.template.render('templates', base='base', globals=t_globals)

### index.html
class Index:
    def GET(self):
        return render.index(None)

class Design:
    def GET(self):
        page = model.get_pages_by_key('design', 'url', 'design*design')
        if not page:
            raise web.seeother('/new?url=%s' % web.websafe(url))
        return render.view('design', page)

class LinuxCommand:
    def GET(self):
        pages = model.get_pages('linux_command')
        return render.main('linux_command', pages)

class LinuxSoftware:
    def GET(self):
        pages = model.get_pages('linux_software')
        return render.main('linux_software', pages)

class Page:
    def GET(self, url):
        table = model.get_table_by_url(url)
        page = model.get_pages_by_key(table, "url", url)
        if not page:
            raise web.seeother('/new?url=%s' % web.websafe(url))
        return render.view(table, page)

class New:
    def not_page_exists(url):
        return not bool(model.get_pages_by_key('linux_command', 'url', url))
    page_exists_validator = web.form.Validator('Page already exists', 
                                not_page_exists)
    form = web.form.Form(
        web.form.Textbox('url', web.form.notnull, page_exists_validator,
            size=30,
            description="Location:"),
        web.form.Textbox('command', web.form.notnull, 
            size=30,
            description="Page title:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Page content:", post="Use markdown syntax"),
        web.form.Button('Create page'),
    )

    def GET(self):
        url = web.input(url='').url
        form = self.form()
        form.fill({'url':url})
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_page('linux_command', form.d.url, form.d.title, form.d.content)
        raise web.seeother('/view/' + form.d.url)


class Delete:
    def POST(self, id):
        model.del_page('linux_command', int(id))
        raise web.seeother('/')

class Edit:
    def create_form(self, table):
        if (table == 'linux_command'):
            form = web.form.Form(
                web.form.Textbox('url', web.form.notnull, size=30, description="Location:"),
                web.form.Textbox('command', web.form.notnull, size=30, description="Command:"),
                web.form.Textarea('content', web.form.notnull, rows=30, cols=80, description="Page content:", post="Use markdown syntax"),
                web.form.Button('Update page'),
            )
        else:
            form = web.form.Form(
                web.form.Textbox('url', web.form.notnull, size=30, description="Location:"),
                web.form.Textbox('title', web.form.notnull, size=30, description="Page title:"),
                web.form.Textarea('content', web.form.notnull, rows=30, cols=80, description="Page content:", post="Use markdown syntax"),
                web.form.Button('Update page'),
            )
        return form


    def GET(self, url):
        table = model.get_table_by_url(url)
        page = model.get_page_by_url(table, url)
        form = self.create_form(table)
        form.fill(page)
        return render.edit(table, page, form)

    def POST(self, url):
        table = model.get_table_by_url(url)
        page = model.get_page_by_url(table, url)
        form = self.create_form(table)
        id = model.get_id_by_url(table, url)
        if not form.validates():
            return render.edit(table, page, form)
        model.update_page(table, id, form.d.url, form.d.title, form.d.content)
        raise web.seeother('/')

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
