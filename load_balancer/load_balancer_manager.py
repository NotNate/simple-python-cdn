class LoadBalancerManager:
    def __init__(self):
        self.edge_servers = []
        self.current_index = 0
        
    def register_edge_server(self, server_info):
        if server_info not in self.edge_servers:
            self.edge_servers.appen(server_info)
            print(f"Registered edge server: {server_info}")
        
    def deregister_edge_server(self, name):
        self.edge_servers = [server for server in self.edge_servers if server['name'] != name]
        print(f"Deregistered edge server: {name}")
        
    def get_next_server(self):
        server = self.edge_servers[self.current_index]
        self.current_index = (self.current_index + 1)
        if (self.current_index >= len(self.edge_servers)):
            self.current_index = 0
        return server