import requests
import sys

def matches(test, item):
    if ">=" in test:
        delim=">="
    elif ">" in test:
        delim=">"
    elif "=" in test:
        delim="="
    (name, value)=test.split(delim,1)
    if value.startswith("@"):
        value = item[value[1:]]

    if delim==">":
        if float(item[name]) > float(value): 
            return True

    if delim==">=":
        if float(item[name]) >= float(value):
                return True

    if delim=="=":
        if item[name] == value:
                return True
    return False

def main():
   url = sys.argv[1]
   tests = sys.argv[2:]

   r = requests.get(url, auth=("admin@opencord.org", "letmein"))
   for item in r.json()["items"]:
       okay=True
       for test in tests:
           if not matches(test, item):
               okay=False
       if okay:
           print "matched"
           sys.exit(0)

   print "Not Matched"
   sys.exit(-1)

if __name__=="__main__":
    main()
