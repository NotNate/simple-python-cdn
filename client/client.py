import requests
import os

def fetch_file_from_cdn(lb_url, filename):
    edge_server_response = requests.get(f"{lb_url}/route")
    if edge_server_response.status_code != 200:
        print("Error getting edge server information from load balancer.")
        return
    
    client_dir = 'downloads/'
    
    edge_server_info = edge_server_response.json()
    edge_server_url = f"http://{edge_server_info['ip']}:{edge_server_info['port']}"
    
    file_response = requests.get(f"{edge_server_url}/content/{filename}")
    if file_response.status_code == 200:
        if not os.path.exists(client_dir):
            os.makedirs(client_dir)
        file_path = os.path.join(client_dir, filename)
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
        print(f"File '{filename}' has been downloaded")
    else:
        print(f"File not found on edge server")
        
def main():
    load_balancer_url = "http://localhost:6000"
    
    while True:
        filename = input("Enter the filename to fetch (or type 'exit' to quit): ")
        if filename.lower() == 'exit':
            break
    
        fetch_file_from_cdn(load_balancer_url, filename)

if __name__ == "__main__":
    main()