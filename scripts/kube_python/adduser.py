import os, sys
from create_pod import main as create_pod
from create_namespace import main as create_namespace
from userlist import listuser
from kubernetes.client.rest import ApiException

def create_component(username, component_name, value):
	if not value == "true": return
	try: 
		print(f"Creating pod {component_name}...")
		create_pod("test", f"{component_name}.json") #TODO fix namespace
	except ApiException as e:
		if e.status != 404:
			print(f"Unknown error: {e}")
			exit(1)

def main(username, email, password, options):
	#create_namespace(username)
		
	listuser.append(f"{username} {email} {options["minio"]} {options["postgres"]}")

	res = listuser
	for k,v in options.items():
		create_component(username, k, v)

	print(res)
	return res

if __name__ == "__main__":
	options = {"minio": sys.argv[4], "postgres": sys.argv[5]}
	main(sys.argv[1], sys.argv[2], sys.argv[3], options)