from flask import Flask, send_file, request, jsonify
import argparse
import requests
from cache_manager import CacheManager
from sync_manager import SyncManager
import atexit
import requests

app = Flask(__name__)

def get_content_from_central_server(filename, cache_manager, central_server_url):
    '''
    Retrieves content identified by filename from the central server.
    If the content is found, it's cached using the cache manager.

    :param filename: Name of the file to be retrieved.
    :param cache_manager: Instance of CacheManager to manage caching.
    :param central_server_url: URL of the central server.
    :return: Content if found, else None.
    '''
    response = requests.get(f"{central_server_url}/content/{filename}")
    if response.status_code == 200:
        cache_manager.cache_content(response.content, filename)
        return response.content
    return None

@app.route('/content/<filename>', methods=['GET'])
def content(filename):
    '''
    Endpoint to serve content. First, tries to retrieve the content from cache.
    If not found in cache, attempts to fetch it from the central server.
    Increments download count if content is served.

    :param filename: Name of the file requested.
    :return: The requested file if available, else a 404 error.
    '''
    content = cacheManager.retrieve_content(filename)
    if content is not None:
        requests.post(f"http://localhost:5000/download_increment/{filename}")
    if content is None:
        content = get_content_from_central_server(filename, cacheManager, "http://localhost:5000")
    if content is not None:
        return send_file(f"{cacheManager.cache_directory}/{filename}", as_attachment=True, download_name=filename), 200
    return jsonify({"message": "Content not found"}), 404

def register_with_lb(name, port):
    '''
    Registers the edge server with a load balancer.
    Sends the server's name, port, and IP address to the load balancer's registration URL.

    :param name: Name of the edge server.
    :param port: Port number on which the edge server is running.
    '''
    load_balancer_url = "http://localhost:6000/register"
    edge_server_info = {
        'name': name,
        'port': port,
        'ip': 'localhost'
    }
    requests.post(load_balancer_url, json=edge_server_info)

def deregister_with_lb(name, port):
    '''
    Deregisters the edge server from the load balancer upon shutdown.
    Sends the server's name, port, and IP address to the load balancer's deregistration URL.

    :param name: Name of the edge server.
    :param port: Port number on which the edge server is running.
    '''
    load_balancer_url = "http://localhost:6000/deregister"
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
    
    sync_int = 600
    
    cacheManager = CacheManager(dir=args.name)
    synchronizer = SyncManager(center_server_url="http://localhost:5000", cm=cacheManager, sync_interval=sync_int)
    
    atexit.register(deregister_with_lb, name=args.name, port=args.port)
    
    synchronizer.synchronize()
    register_with_lb(args.name, args.port)
    
    app.run(host='0.0.0.0', port=args.port)