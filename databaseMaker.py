import sqlite3
conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE APPS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME CHAR(200) NOT NULL,
    PRICE CHAR(20) NOT NULL,
    ICON CHAR(200) NOT NULL,
    URL CHAR(200) NOT NULL,
    CATEGORY CHAR(50) NOT NULL)''')
