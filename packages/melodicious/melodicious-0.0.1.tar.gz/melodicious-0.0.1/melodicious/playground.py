import melodicious

client = melodicious.APIClient(base_url='', username='', usertoken='', callEndpoint='', data='')

response = client.playing()

print(response)
