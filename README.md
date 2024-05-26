# history-parser
project for intermediate digital forensics course.  Parses edge,firefox,and chrome web history databases into CSV file.  
## Usage
```
usage: history_parser.py [-h] -f FILE -o OUTPUT_FILE [-g] {firefox,chrome,edge}

Simple CSV Browser History Parser for Google Chrome, Firefox and Microsoft Edge

positional arguments:
  {firefox,chrome,edge}
                        type of history file to parse

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to browser history database, i.e History(Chrome,Edge), places.sqlite3(Firefox)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        path to output file (csv)
  -g, --graph           create graph of top 10 dates and destinations
```
## Installation
- make sure you have all the requirements for your python3 installation detailed in requirements.txt
```bash
pip3 install -r requirements.txt
```
- tested on edge, firefox and google chrome browsing history databases
- -g, --graph option requires GUI
## A little context...
Recently, a team of students and myself took part in a Digital Forensics/Incident Response simulation/competition.  We were given images of several servers/workstations and tasked with analyzing an attack on a small business. This required us to consolidate browsing histories from multiple hosts each with a variety of browsers in use.  This project came about in response to the need to quickly get an idea as to the traffic and traffic patterns in these browsing history databases.  While there is much more to be found by querying the databases themselves, this simple parser can give an investigator a quick view of browsing history in the form of a csv file with url and localized timestamps.  Also included in the csv is a tally of the total visits to the particular url. The tool includes a --graph option for a quick graph of the top 10 most visted domains and busiest traffic days.

## Usual locations for browser history files
- Google Chrome:
  
  Windows : C:\Users\\"username"\AppData\Local\Google\Chrome\User Data\Default\History
  
  Linux : /home/"username"/.config/google-chrome/Default/History
  
  MacOs :  /Users/"username"/Library/Application Support/Google/Chrome/Default/History
  
- Mozilla Firefox:
- 
  Windows : C:\Users\\"username"\AppData\Local\Mozilla\Firefox\Profiles\"something".default-release\places.sqlite
  
  Linux : /home/"username"/.mozilla/firefox/<something>.default-esr/places.sqlite
  
  MacOs : /Users/"username"/Library/Application Support/Firefox/Profiles/"something".default-release\places.sqlite
  
- Microsoft Edge
- 
  Windows: C:\Users\\"username"\AppData\Local\Microsoft\Edge\User Data\Default\History
  
  Linux : um...
  
  MacOs : Users/"username"/Library/Application Support/Microsoft Edge/Default/History

## tips and screenshots
I suggest using forward slashes '/' for specifying paths.  Also, it may be a good idea to make a copy of the databases and move to a separate folder to run this script on multiple browser histories, saving the csv files in the current directory.  Otherwise, make sure to include paths with spaces in single quotes.  
![image](https://github.com/cactus-dad/history-parser/assets/85032657/cc7b1ba9-4516-4c22-8176-a2fa1995cf01)
![image](https://github.com/cactus-dad/history-parser/assets/85032657/0cfd4d24-ef2d-42f8-8425-e64f2eb23a65)

![image](https://github.com/cactus-dad/history-parser/assets/85032657/0996b38e-a8e4-4e26-be1e-6278a6579094)

## todo
- allow for specific fields to be selected for csv file
- html output
- downloads/cookies history
- so much todo so little time
