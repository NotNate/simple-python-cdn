class LoadBalancerManager:
    '''
    A class to manage the load balancing of edge servers.
    It can register, deregister, and select edge servers for handling requests.
    '''
    def __init__(self):
        '''
        Initializes the LoadBalancerManager instance.
        '''
        self.edge_servers = []
        self.current_index = 0
        
    def register_edge_server(self, server_info):
        '''
        Registers a new edge server.
        Adds the server to the list of available edge servers.

        :param server_info: Dictionary containing the server's IP, port, and name.
        '''
        if server_info not in self.edge_servers:
            self.edge_servers.append(server_info)
            print(f"Registered edge server: {server_info}")
        
    def deregister_edge_server(self, name):
        '''
        Deregisters an edge server.
        Removes the server from the list of available edge servers.

        :param name: Name of the edge server to be deregistered.
        '''
        self.edge_servers = [server for server in self.edge_servers if server['name'] != name]
        print(f"Deregistered edge server: {name}")
        
    def get_next_server(self):
        '''
        Retrieves the next available edge server.
        Uses a round-robin algorithm to cycle through the servers.

        :return: Dictionary containing the next server's details.
        '''
        server = self.edge_servers[self.current_index]
        self.current_index = (self.current_index + 1)
        if (self.current_index >= len(self.edge_servers)):
            self.current_index = 0
        return server