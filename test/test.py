import urllib

data = {"data":"123"}
a = urllib.urlencode(data)
print(a)