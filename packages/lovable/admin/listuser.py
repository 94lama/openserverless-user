import subprocess, json, sys

listuser = ["", "devel true false false false true", "admin true false false false true", "aaaaa true false false false true"] #mockup

def main():
    #command = b'if test -n "{{._username_}}" then kubectl -n nuvolaris get wsku /{{._username_}} -ojsonpath="{.spec}" | jq . else kubectl -n nuvolaris get wsku fi'
    #users = subprocess.run(command.decode("utf-8"), capture_output=True, shell=True, text=True)
    #users = subprocess.run(["if","test -n '{{._username_}}'","then kubectl -n nuvolaris get wsku '{{._username_}}' -ojsonpath='{.spec}' | jq .", "else", "kubectl -n nuvolaris get wsku", "fi"], capture_output=True, shell=True, text = True)
    """ users = subprocess.run("ops admin listuser", capture_output=True, shell=True, text=True)
    userlist = users.stdout.split("\n") """
    res = []
    if listuser[0] == "": listuser.pop(0)
    for item in listuser:
        user = list(filter(lambda x: x != "", item.split(" ")))
        if(user):
            res.append({
                "name": user[0],
                "options": {
                    "couchdb": user[1] == "true",
                    "mongodb": user[2] == "true",
                    "redis": user[3] == "true",
                    "objectStorage": user[4] == "OK...",
                    "route": user[5] == "true"
                }
            })

    #sys.stdout(res)
    return res

if __name__ == "__main__":
    main()