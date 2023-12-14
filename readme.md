# How to run
1. Start an instance of the central server by doing `cd central_server`, and then `python app.py`
2. Start an instance of the load balancer by doing `cd load_balancer` in a new terminal, and then `python app.py`
3. Start an instance of an edge server by doing `cd edge_server` in a new terminal, and then `python app.py {name} {port}
4. Start an instance of the client by doing `cd client` in a new terminal, and then `python client.py`
5. Type a file name that exists on the server in the client, and hit enter
6. Repeat.