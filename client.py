import socket
import sys

#method to make a new connection to rs
def send_query(rs_host, rs_port, domain, query_id, mode):


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:   


        client_socket.connect((rs_host, rs_port))


        #print(rs_host)        
        message = f"0 {domain.lower()} {query_id} {mode}"    


        client_socket.sendall(message.encode())   

        response = client_socket.recv(1024).decode()

        client_socket.close() 

        return response


def main():    
    if len(sys.argv) != 3:  

        print("Usage: python3 client.py <rs_hostname> <rs_port>")  

        sys.exit(1) 

    rs_host = sys.argv[1]  

    rs_port = int(sys.argv[2])

    query_id = 1 

    #writing responses to resolved.txt   
    resolved_file = open("resolved.txt", "w") 

    with open("hostnames.txt", "r") as file:        
        for line in file: 

            domain, mode = line.strip().split() 

            response = send_query(rs_host, rs_port, domain, query_id, mode) 

            resolved_file.write(response + "\n")   

            print(response)

            #checking if response is an ns
            response_parts = response.split()
            
            if response_parts[-1] == "ns":

                tld_server = response_parts[2]

                #print(tld_server) 
                #sending new query to tld server for it (iterative) queries
                query_id += 1

                response = send_query(tld_server, 45496, domain, query_id, mode) 

                resolved_file.write(response + "\n")   

                print(response)  
                          
            query_id += 1 

    resolved_file.close()

if __name__ == "__main__":    
    main()
