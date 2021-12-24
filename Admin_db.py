import sqlite3
def ad(Usid,Prev_reading,Img_path):
    conn = sqlite3.connect('userdata1.db')
    c=conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS user1(
                    usid text primary key,
                    prev_reading float,
                    cur_reading float,
                    mon_reading float,
                    bill_amt float,
                    img_path text)""")
    Prev_reading=float(Prev_reading)
    Cur_reading=0.0
    Mon_reading=Cur_reading-Prev_reading
    c.execute("INSERT INTO user1 VALUES ('{}','{}','{}','{}','{}','{}')".format(Usid,Prev_reading,Cur_reading,Mon_reading,-1,Img_path))
    # c.execute("SELECT * FROM user1")
    # rows=c.fetchall()
    # for row in rows:
    #     print(row)
    conn.commit()
    conn.close()