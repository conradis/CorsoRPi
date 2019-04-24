import sqlite3
conn = sqlite3.connect('robot.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE position
             (date text, rwheelspace real, lwheelspace real)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
