import subprocess, json, sys

def main():
    #command = b'if test -n "{{._username_}}" then kubectl -n nuvolaris get wsku /{{._username_}} -ojsonpath="{.spec}" | jq . else kubectl -n nuvolaris get wsku fi'
    #users = subprocess.run(command.decode("utf-8"), capture_output=True, shell=True, text=True)
    #users = subprocess.run(["if","test -n '{{._username_}}'","then kubectl -n nuvolaris get wsku '{{._username_}}' -ojsonpath='{.spec}' | jq .", "else", "kubectl -n nuvolaris get wsku", "fi"], capture_output=True, shell=True, text = True)
    """ users = subprocess.run("ops admin listuser", capture_output=True, shell=True, text=True)
    userlist = users.stdout.split("\n") """
    userlist = ["", "devel true false false false true", "admin true false false false true", "aaaaa true false false false true"] #mockup
    res = []
    userlist.pop(0)
    for item in userlist:
        user = list(filter(lambda x: x != "", item.split(" ")))
        if(user):
            res.append({
                "NAME": user[0],
                "COUCHDB": user[1] == "true",
                "MONGODB": user[2] == "true",
                "REDIS": user[3] == "true",
                "OBJECTSTORAGE": user[4] == "OK...",
                "ROUTE": user[5] == "true"
            })

    #sys.stdout(res)
    return res

if __name__ == "__main__":
    main()