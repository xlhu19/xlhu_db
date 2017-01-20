import web

db = web.database(dbn='postgres', db='xlhu_db', user='postgres', pw='123456')

# All tables should has a column 'id' and 'url'
def get_pages(table):
    return db.select(table, order='url ASC')

def get_table_by_url(url):
    return (url.split('*'))[0]

def get_pages_by_key(table, key, val):
    try:
        return db.select(table, where=key+'=$val', vars=locals())[0]
    except IndexError:
        return None

def get_page_by_id(table, id):
    try:
        return db.select(table, where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def get_page_by_url(table, url):
    try:
        return db.select(table, where='url=$url', vars=locals())[0]
    except IndexError:
        return None

def get_id_by_url(table, url):
    try:
        return (db.select(table, where='url=$url', vars=locals())[0]).id
    except IndexError:
        return None
    

def new_page(table, url, title, text):
    if (table == 'linux_command'):
        db.insert(table, url=url, command=title, content=text)

def del_page(table, id):
    db.delete(table, where="id=$id", vars=locals())

def update_page(table, id, url, title, text):
    db.update(table, where="id=$id", vars=locals(),
        url=url, title=title, content=text)
