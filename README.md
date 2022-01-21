# EmailScraper
Python program that allows you to scan a given URL for emails.


# Installation Progress:
* Download python from this URL: 
*https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe*
* Download the files from this repository by clicking on 'Code', Download ZIP.
* Extract the files from the .zip, and navigate to the new folder.
* Open this folder in CMD. *click on the search bar and type cmd*
* Install the dependencies:  
```
$ pip install -r req.txt
```

# How To Use:
* Help:
```
python main.py -h
```
* Command Structure:
```
python main.py -u [URL] -sf [FILENAME] -c [NUMBER] -v -ce
```
# Flags And Meaning:
  -h, --help   *=>*          show this help message and exit. <br>
  -u [URL], --url [URL]   *=>*  Specify the target url you want to scan. <br>
  -sf [FILE_NAME], --save-file [FILE_NAME] *=>*
                        Specify file name if you want to save it. defualt is None.<br>
  -c [COUNT], --count [COUNT] *=>*
                        Specify the number of URLs you want to scan. defualt is 100.<br>
  -v, --verbose    *=>*     Specify if you want to see output. defualt is False.<br>
  -ce, --check-email  *=>*  Specify if you want to check for invalid emails. defualt is False.<br>
  
# Examples:
*scan 10 "subdomains" of github.com, save the emails to 'emails.txt', check for invalid emais:* <br>
``` python main.py -u https://github.com/ -sf emails.txt -c 10 -ce ```

# Pay Attention❤️
The word subdomains is misleading. The program scans for links in the corrent page.<br>
It's using the fact that links usually stored in *a* tags.<br>
```html
<a href="URL">TEXT</a>
```
When you specify -c *n*, the program will stop after *n* itterations, *n* links.<br>
Therefore the greater *n*, the greater the runtime of the program, and potentially the greater number of emails.

# Disclaimer. Thie developer DOES NOT Promote or encourage Any illegal activities.
