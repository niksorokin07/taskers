import sqlite3



def add_member(nikname, mail):
    connect = sqlite3.connect('taskerbase1.sqlite')
    cur = connect.cursor()
    cur.execute(f"""INSERT INTO Rooms(Managers, Users) VALUES({nikname}, {mail})""")
    connect.commit()
    cur.close()