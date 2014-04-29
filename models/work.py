from google.appengine.ext import ndb

class Work(ndb.Model):
    last_modified = ndb.DateTimeProperty(auto_now=True)
    priority = ndb.IntegerProperty()
    title = ndb.StringProperty()
    price = ndb.StringProperty()

    @staticmethod
    def get_root():
        root = Work.query(Work.title == '').order(-Work.last_modified).fetch()
        return Work.fill(root[0]) if len(root) else { 'title': '', 'price': '', 'children': [] }

    @staticmethod
    def fill(work):
        return Work.fill_children({
            'key': work.key,
            'title': work.title,
            'priority': work.priority,
            'price': work.price
        })

    @staticmethod
    def fill_children(work):
        work['children'] = []
        for child in Work.query(ancestor=work['key']).order(+Work.priority).fetch():
            if work['key'] == child.key.parent():
                work['children'].append(Work.fill(child))

        return work
