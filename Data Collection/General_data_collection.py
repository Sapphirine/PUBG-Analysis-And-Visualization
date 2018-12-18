import json
import requests
import time
import sys
f = open("match.json",'r')
filename = "./Erangel/telemetry"
f1 = open(filename + "1.json",'w')

header = {
  "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzNmJiYmY4MC1iZjY0LTAxMzYtNTAwNC02OWQ1Nzg2ZmMwZjQiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQxMDA4NTg3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IjY4OTNhbmFseXNpcyJ9.EVPTnXNlXe-zuH7ERO7As2_OSlRodYULbQh3j6mLUIE",
  "Accept": "application/vnd.api+json"
}
file_count = 2
count = 1
correct = 0
error = 0
line = f.readline()
start_time = time.time()
while line:
	data = json.loads(line.strip('\n'))
	if data['data']['attributes']['mapName'] != 'Erangel_Main':
		line = f.readline()
		continue
	m = data['included']
	for i in m:
		if i['type'] == "asset":
			url = i['attributes']['URL']
	if correct%100 == 0:
		f1.close()
		f1 = open(filename + str(file_count) + ".json",'w')
		file_count = file_count + 1
	if count == 1000:
		f1.close()
		break
	try:
		r = requests.get(url, headers=header)
		f1.write(json.dumps(r.json()))
		f1.write('\n')
		print(count, error)
		m, s = divmod(time.time()-start_time, 60)
		h, m = divmod(m, 60)
		difftime = "%02dh%02dm%02ds" % (h,m,s)
		print(difftime)
		count = count + 1
		correct = correct + 1
		line = f.readline()
		time.sleep(6)
	except:
		print("error")
		error = error + 1
		print(count, error)
		m, s = divmod(time.time()-start_time, 60)
		h, m = divmod(m, 60)
		difftime = "%02dh%02dm%02ds" % (h,m,s)
		print(difftime)
		count = count + 1
		line = f.readline()
		time.sleep(6)

print("All done")
print(count)
print(error)
