import webapp2
from google.appengine.ext import ndb
from models.work import *
from admin.templates import render
import re

work_line_re = re.compile(
    r"""^(?P<indent>\s*?)
    (?P<title>\S.*?)\s+
    (?P<price>\S+)\s*
    $""", re.VERBOSE)

class WorksAdminHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(render('works', { 'works': Work.get_root()['children'] }))

    def post(self):
        root = Work(title='', price='')
        root.put()

        work = None
        works = [{ 'item': root, 'indent': -1 }]
        priority = 0

        for line in self.request.get('works').splitlines():
            match = work_line_re.match(line)
            if match:
                work = { 'indent': len(match.group('indent')) }
                priority += 1

                while work['indent'] <= works[-1]['indent']: works.pop()

                work['item'] = Work(
                    title=match.group('title'),
                    price=match.group('price'),
                    priority=priority,
                    parent=works[-1]['item'].key)
                work['item'].put()

                if work['indent'] >= works[-1]['indent']: works.append(work)

        self.redirect('/admin/works/')


    def bla(self):
        # post about work photo
        if self.request.get('work'):
            # try get existing...
            photo = None
            try:
                photo = ndb.Key(urlsafe=self.request.get('key')).get()
            except TypeError:
                pass
            # or create new one
            if not photo:
                work = ndb.Key(urlsafe=self.request.get('work')).get()
                photo = WorkPhoto(parent=ndb.Key(Work, work.key.id()))

            photo.title = self.request.get('title')
            photo.url = self.request.get('url')
            photo.priority = int(self.request.get('priority'))
            photo.put()

        # post about work
        else:
            # try get existing...
            work = None
            try:
                work = ndb.Key(urlsafe=self.request.get('key')).get()
            except TypeError:
                pass
            # or create new one
            if not work:
                work = Work()

            work.priority = int(self.request.get('priority'))
            work.name = self.request.get('name')
            work.title = self.request.get('title')
            work.description = self.request.get('description')
            work.put()

        self.redirect('/works/')
