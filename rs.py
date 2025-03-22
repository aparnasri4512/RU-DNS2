import sys

import socket



with open("rsresponses.txt", "w") as rs_file:

        res_file.write("")

        res_file.close()


#method to load rsdatabase.txt
def load_database(filename):    


    mappings = {}

    with open(filename, "r") as file:

        lines = file.readlines()

        ts1_host = lines[0].split()[1]

        ts2_host = lines[1].split()[1]

        for line in lines[2:]:

            domain, ip = line.strip().split()

            mappings[domain.lower()] = (domain, ip)

    return ts1_host, ts2_host, mappings




#method to forward recursive query to tld server and returning response
def forward_query(server_host, port, domain, query_id, mode):    



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TS_socket:



        TS_socket.connect((server_host, port))



        mess = f"0 {domain} {query_id} {mode}"



        TS_socket.sendall(mess.encode())



        response = ts_socket.recv(1024).decode()        



        return response  # Forward response back to client




#method to handle client requests
def handle_client(conn, ts1_host, ts2_host, mappings, port):    



    while True:    



        data = conn.recv(1024).decode()  



        if not data:            



            break



        parts = data.split()    



        if len(parts) != 4:  



            break      



              

        _, domain, query_id, mode = parts    



        domain_lower = domain.lower()        



        if domain in mappings:        

            org_domain, ip = mappings[domain_lower]

            res = f"1 {domain} {org_domain} {query_id} aa"



        else:        



            tld = domain.split(".")[-1]



            if mode == "it":

                if tld == "com":

                    response = f"1 {domain} {ts1_host} { query_id} ns"

                elif tld == "edu":

                    response = f"1 {domain} {ts2_host} {query_id} ns"  

                else:

                    response = f"1 {domain} 0.0.0.0 {query_id} nx"  



            elif mode == "rd":    



                if tld == "com": 



            



                    res = forward_query(ts1_host, 45496, domain, query_id, mode)



                    res_parts = res.split()



                    if res_parts[-1] == "aa":

                        res = f"1 {domain} {response_parts[2]} {query_id} ra"

                elif tld == "edu":

                    res = forward_query(ts2_host, 45496, domain, query_id, mode)

                    res_parts = response.split()

                    if res_parts[-1] == "aa":

                        res = f"1 {domain} {response_parts[2]} {query_id} ra"



                else:                



                    res = f"1 {domain} 0.0.0.0 {query_id} nx"



        with open("rsresponses.txt", "a") as rs_file:

             rs_file.write(res + "\n")



        conn.sendall(res.encode())



    conn.close()





def main():    



    if len(sys.argv) != 2:        



        print("Usage: python3 rs.py <port>")        



        sys.exit(1)    



    port = int(sys.argv[1])    



    ts1_host, ts2_host, mappings = load_database("rsdatabase.txt")    



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.bind(("",port))

        server_socket.listen()

        print(f"RS linstening on port {port}")        



        while True:            



            conn, _ = server_socket.accept()            



            handle_client(conn, ts1_host, ts2_host, mappings, port)





if __name__ == "__main__":    



    main()