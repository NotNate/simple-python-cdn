from flask import Flask, request, jsonify
from load_balancer_manager import LoadBalancerManager

app = Flask(__name__)
lb_manager = LoadBalancerManager()

'''
json_format
{
    "ip": "address"
    "port": "port"
    "name": "name"
}
'''

@app.route('/register', methods=['POST'])
def register():
    '''
    Flask route to handle registration of edge servers.
    Expects a JSON payload with the server's IP, port, and name.
    Registers the server using the LoadBalancerManager.
    
    :return: JSON response confirming successful registration.
    '''
    server_info = request.json
    lb_manager.register_edge_server(server_info)
    return jsonify({"message": "Edge server registered successfully"}), 200

@app.route('/deregister', methods=['POST'])
def deregister():
    '''
    Flask route to handle deregistration of edge servers.
    Expects a JSON payload with the server's name.
    Deregisters the server using the LoadBalancerManager.
    
    :return: JSON response confirming successful deregistration.
    '''
    server_info = request.json.get('name')
    lb_manager.deregister_edge_server(server_info)
    return jsonify({"message": "Edge Server deregistered successfully"}), 200

@app.route('/route', methods=['GET'])
def route_request():
    '''
    Flask route to get the next available edge server for routing requests.
    Uses a round-robin method to select the next server.

    :return: JSON containing the details of the next server, or an error message if no servers are available.
    '''
    server = lb_manager.get_next_server()
    if server:
        return jsonify(server), 200
    return jsonify({"error": "No edge servers available"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)