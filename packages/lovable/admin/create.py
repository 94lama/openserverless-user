import subprocess, json, sys

def main():
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]

    if username and email and password:
        command = ["ops","admin","adduser",username,email,password]
        """ if (args.get("options")):
            if args.options.get("redis"):
                command.push """

        res = subprocess.run(command, capture_output=True, text=True)
        print(res)
        return res
    else: 
        return json.loads({"error": "some parameters are missing"})

if __name__ == "__main__":
    main()