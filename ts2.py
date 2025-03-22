import socket
import sys

#to clear ts1responses file out after 1st iteration
with open("ts2responses.txt", "w") as log_file:
        log_file.write("")
        log_file.close()
    
#method to load ts1database.txt
def load_database(filename):


    mappings = {}


    with open(filename, "r") as file: 

        for line in file: 

            domain, ip_add = line.strip().split() 

            mappings[domain.lower()] = ip_add 

    return mappings

#method for query handling
def handle_request(connections, mappings): 

    data = connections.recv(1024).decode() 

    parts = data.split() 

    if len(parts) != 4:

        connections.close()

        return 
     
    _, domain, query_id, _ = parts 

    domain_lower = domain.lower()

    if domain_lower in mappings: 

        org_domain, ip = mappings[domain_lower] 

        response = f"1 {org_domain} {ip} {query_id} aa"    
    else:        
        response = f"1 {domain} 0.0.0.0 {query_id} nx"


    #writing into ts1responses.txt
    with open("ts2responses.txt", "a") as log_file:
             log_file.write(response + "\n")


    #sending all connections     
    connections.sendall(response.encode())    

    connections.close()

def main():    
    if len(sys.argv) != 2:  


        print("Usage: python3 ts2.py <port>") 


        sys.exit(1)
    #extracting port from command line   
        
    port = int(sys.argv[1])


    mappings = load_database("ts2database.txt")


    #creating connection 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:


        server_socket.bind(("", port)) 



        server_socket.listen()


        print(f"TS2 listening on port {port}")


        while True:  



            connections, _ = server_socket.accept()


            handle_request(connections, mappings)




if __name__ == "__main__":
        
    main()

