Usage:

```bash
witnesschangeme -t http://target.com
witnesschangeme -t file.txt
```

There will be 6 files where you run the command
 - witnesschangeme-error.txt -> Urls that gave error such as 4xx,5xx, Timeout or any error in program
 - witnesschangeme-known-bad.txt -> Urls that it is known that it doesn't have login functionality or doesn't have default credentials
 - witnesschangeme-valid.txt -> Urls that had valid default credentials
 - witnesschangeme-valid-template-no-credential.txt -> Urls that had a template but didn't have default credentials
 - witnesschangeme-valid-url-no-template.txt -> Urls that was valid but had no template
 - witnesschangeme-manual.txt -> Urls that has spicy login mechanism so i didn't bother to automate, file will contain default passwords to help you