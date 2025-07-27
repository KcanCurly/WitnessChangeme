# Warning
Archieved! Merged with [Nessus Verifier](https://github.com/KcanCurly/nessus-verifier)

# Installation:
```bash
pipx install git+https://github.com/kcancurly/witnesschangeme
```

# Usage:

```bash
witnesschangeme -t http://target.com
witnesschangeme -t file.txt
witnesschangeme -t file.txt --threads 20
```

There will be 6 files where you run the command
 - witnesschangeme-error.txt -> Urls that gave error such as 4xx,5xx, Timeout or any error in program
 - witnesschangeme-known-bad.txt -> Urls that it is known that it doesn't have login functionality or doesn't have default credentials
 - witnesschangeme-valid.txt -> Urls that had valid default credentials
 - witnesschangeme-valid-template-no-credential.txt -> Urls that had a template but didn't have default credentials
 - witnesschangeme-valid-url-no-template.txt -> Urls that was valid but had no template
 - witnesschangeme-manual.txt -> Urls that has spicy login mechanism so i didn't bother to automate, each entry will have default password to help you