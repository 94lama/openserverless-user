import subprocess, sys

def main():
    user = sys.argv[1]

    if user:
        res = subprocess.run(["ops","admin","deleteuser",user], capture_output=True, text=True)
        return res
    else: return json.loads({"error": "The username is not valid"})

if __name__ == "__main__":
    main()