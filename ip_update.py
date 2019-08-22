import http.client, json

# Connection info
API_ENDPOINT = "cloudinfra-gw.portal.checkpoint.com" # << Don't change this
NSAAS_SITE_NAME = "EDIT ME" # << Your EXACT site name
NSAAS_CLIENT_ID = "EDIT ME" # << Your NSaaS Client ID
NSAAS_SECRET_KEY = "EDIT ME" # << Your NSaaS Access Key

# Request authorisation token

conn = http.client.HTTPSConnection(API_ENDPOINT)

payload = "{\n  \"clientId\": \"" + NSAAS_CLIENT_ID + "\",\n  \"accessKey\": \"" + NSAAS_SECRET_KEY + "\"\n}"
headers = { 'content-type': "application/json" }
conn.request("POST", "/auth/external", payload, headers)

res = conn.getresponse()
data = res.read()
auth_token = json.loads(data)['data']['token']
conn.close()
res.close()
# Request Site ID

conn = http.client.HTTPSConnection(API_ENDPOINT)

headers = {
    'content-type': "application/json",
    'authorization': "Bearer " + auth_token
    }
payload = "{\"query\":\"# get all sites\\nquery getSites {\\n  sites {\\n    id\\n    name\\n    description\\n  }\\n}\",\"operationName\":\"getSites\"}"
conn.request("POST", "/app/gwaas/graphql", payload, headers)
res = conn.getresponse()
data = res.read()
conn.close()
sites = json.loads(data)['data']['sites']
site_id = ""
for s in sites:
    if s['name'] == NSAAS_SITE_NAME:
        site_id = s['id']
        break
if site_id == "":
    print("[ERROR] Could not find Site ID for given site name. Please check access keys and EXACT site name!")
    exit()


# Retrieve new external IP

conn = http.client.HTTPSConnection("ifconfig.co")
conn.request("GET", "/json")
res = conn.getresponse()
data = res.read()
ext_ip = json.loads(data)['ip']
conn.close()
# Update site with new IP address

conn = http.client.HTTPSConnection("cloudinfra-gw.portal.checkpoint.com")

payload = "{\"query\":\"# update an existing site\\nmutation updateSite($id: ID!, $data: UpdateSiteInput!) {\\n  updateSite(id: $id, data: $data)\\n}\",\"variables\":{\"id\":\"" + site_id + "\",\"data\":{\"routerExternalIP\":\"" + ext_ip + "\"}}}"

headers = {
    'content-type': "application/json",
    'authorization': "Bearer " + auth_token
    }

conn.request("POST", "/app/gwaas/graphql", payload, headers)

res = conn.getresponse()
data = res.read()
conn.close()
print("external IP updated: " + ext_ip)
