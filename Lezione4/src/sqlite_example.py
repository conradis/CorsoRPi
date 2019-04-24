import sqlite3
from time import strftime
conn = sqlite3.connect('robot.db')
c = conn.cursor()

# Insert a row of data
c.execute("INSERT INTO position VALUES ('"+strftime("%a, %d %b %Y %H:%M:%S +0000")+"',10.3,20.4)")

# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT * FROM position ORDER BY date asc'):
        print(row)
        
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()