import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('links.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS data(link)')
    base.commit()


async def sql_add_command(link):
    cur.execute('INSERT INTO data VALUES(?)', (link,))
    base.commit()


async def sql_delete_command(link):
    cur.execute('DELETE FROM data WHERE link == ?', (link,))
    base.commit()


async def sql_read():
    return cur.execute('SELECT * FROM data').fetchall()