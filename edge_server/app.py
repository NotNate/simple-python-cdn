from flask import Flask, send_file, request, jsonify
import argparse
import requests
from cache_manager import CacheManager
from sync_manager import SyncManager

app = Flask(__name__)
synchronizer = SyncManager("http://localhost:5000")
cacheManager = CacheManager()

@app.route('/content/<filename>', methods=['GET'])
def content(filename):
    content = cacheManager.retrieve_content(filename)
    if content is not None:
        return send_file(content, as_attachment=filename), 200
    return jsonify({"message": "Content not found"}), 404

def register_with_lb(name, port):
    load_balancer_url = "http://localhost:6000"
    edge_server_info = {
        'name': name,
        'port': port,
        'ip': 'localhost'
    }
    requests.post(load_balancer_url, json=edge_server_info)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an edge server")
    parser.add_argument('name', type=str, help='Name of the edge server to identify it.')
    parser.add_argument('port', type=int, help='Port of the edge server to connect to.')
    args = parser.parse_args()
    
    synchronizer.synchronize()
    register_with_lb(args.name, args.port)
    
    app.run(host='0.0.0.0', port=args.port)