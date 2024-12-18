If you are running this from headless environment for example linux that doesn't have desktop, then:
sudo apt install xvfb
xvfb-run witnesschangeme -h

Run the following command to download, extract, and move Geckodriver to the appropriate directory for global usage:

```bash
cd $HOME && wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz && \
  mkdir gecko && tar -xvf geckodriver-v0.35.0-linux64.tar.gz -C ./gecko && \
  sudo mv ./gecko/geckodriver /usr/local/bin/ && rm -r gecko && rm geckodriver-v0.35.0-linux64.tar.gz;
```

If you are working in a headless environment, you need to install `Xvfb` (X Virtual Framebuffer), which simulates a display for running graphical applications.

```bash
sudo apt install -y xvfb
```

Usage:

```bash
witnesschangeme -t http://target.com
witnesschangeme -t file.txt
xvfb-run witnesschangeme -t file.txt
```

If you run with xvfb-run, don't forget to kill the xvfb-run process later on

There will be 4 files where you run the command
witnesschangeme-error.txt -> Urls that gave error such as 4xx,5xx
witnesschangeme-valid.txt -> Urls that had valid default credentials
witnesschangeme-valid-template-no-credential.txt -> Urls that had a template but didn't have default credentials
witnesschangeme-valid-url-no-template.txt -> Urls that was valid but had no template