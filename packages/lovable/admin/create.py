import subprocess, json, sys
from listuser import listuser

def main(args):
    name = args[1]
    email = args[2]
    password = args[3]

    if username and email and password:
        #command = ["ops","admin","adduser",name,email,password]
        #""" if (args.get("options")):
        #    if args.options.get("redis"):
        #        command.push """
        #res = subprocess.run(command, capture_output=True, text=True)
        res = listuser.append({name:name, email:email, password:password})
        print(res)
        return res
    else: 
        return json.loads({"error": "some parameters are missing"})

if __name__ == "__main__":
    main(sys.argv)