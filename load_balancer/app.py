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
    server_info = request.json
    lb_manager.register_edge_server(server_info)
    return jsonify({"message": "Edge server registered successfully"}), 200

@app.route('/deregister', methods=['POST'])
def deregister():
    server_info = request.json.get('name')
    lb_manager.deregister_edge_server(server_info)
    return jsonify({"message": "Edge Server deregistered successfully"}), 200

@app.route('/route', methods=['GET'])
def route_request():
    server = lb_manager.get_next_server()
    if server:
        return jsonify(server), 200
    return jsonify({"error": "No edge servers available"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)