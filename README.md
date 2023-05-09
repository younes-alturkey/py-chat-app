To run this:

- Run `pip3 install colorama`
- Run `python loadbalancer.py` to initialize the load balancer server.
- Run `python server1.py` to create a group as in server1.py.
- Run `python server2.py` to create a group as in server2.py.
- Run `python server3.py` to create a group as in server3.py.
- Run `python client.py` 6x clients to demo groups and load balancer functionalities.
- Press `w` to see who is online in a given group (server)
- All chat messages are saved in sqlite `app.db`
- Install Sqlite3 https://www.sqlitetutorial.net/download-install-sqlite/
- Add sqlite3 to `PATH` on windows so it works on command lines (terminals)
- Be in the `root directory`
- Run `sqlite3 app.db`
- SQL Query `SELECT * FROM HISTORY;` to see saved chats
