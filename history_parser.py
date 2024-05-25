import sqlite3
import csv
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse
TYPES= [
   "firefox","chrome","edge"
]
def extract_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname
def create_graphs(csv_file):
    df = pd.read_csv(csv_file, sep=',',names=['date', 'url','visits'], skiprows=1, usecols=[0,1])
    df['hostname'] =df['url'].apply(extract_hostname)
    hostname_counts = df['hostname'].value_counts()
    top_10_hostnames = hostname_counts.nlargest(10).sort_index()
    df['date'] =pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] =df['date'].dt.day
    df['date_only'] = pd.to_datetime(df[['year','month','day']])
    date_counts= df['date_only'].dt.date.value_counts()
    top_10_dates = date_counts.nlargest(10).sort_index()
    top_10_dates.index = pd.to_datetime(top_10_dates.index)
    fig, (ax1,ax2) =plt.subplots(2, 1,figsize=(10,12))
    fig.suptitle("Traffic Analysis", fontsize=16)
    top_10_dates.plot(kind="bar", ax=ax1)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Frequency')
    ax1.set_title("TOP 10 Busiest Days")
    ax1.set_xticks(range(len(top_10_dates.index)))
    ax1.set_xticklabels(top_10_dates.index.strftime('%Y-%m-%d'),rotation=45,ha='right')
    top_10_hostnames.plot(kind="bar",ax=ax2)
    ax2.set_xlabel('Hostname')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Top 10 Most Visited Hostnames')
    ax2.set_xticks((range(len(top_10_hostnames.index))))
    ax2.set_xticklabels(top_10_hostnames.index,rotation=45,ha='right')
    plt.subplots_adjust(hspace=.5)
    plt.show()
def check_errors(e):
    print(e)
    print("do you have the correct filetype?")
def check_input_file(args):
    if os.path.exists(args.file[0]) and os.access(args.file[0], os.R_OK) and os.access(args.file[0], os.W_OK):
        pass
    else:
        print("input file is not accessible...exiting")
        exit()

def process_file(args):
    if args.type == 'firefox':
        parse_firefox(args)
    elif args.type == 'chrome':
        parse_chrome(args)
    elif args.type == 'edge':
        parse_edge(args)
def parse_firefox(args):
    try:
        db_conn = sqlite3.connect(args.file[0])
    except sqlite3.OperationalError:
        print(f"unable to open database at {args.file[0]}")
        exit()
    cursor= db_conn.cursor()
    query='''
    SELECT
        
        datetime(moz_historyvisits.visit_date / 1000000, 'unixepoch', 'localtime') AS VisitTime,
        moz_places.url AS URL,
        moz_places.visit_count AS TotalNumberOfVisits
    FROM
        moz_historyvisits
    JOIN
        moz_places ON moz_historyvisits.place_id = moz_places.id
    GROUP BY
        VisitTime, URL
    ORDER BY
        TotalNumberOfVisits DESC;
    '''
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        check_errors(e)
        exit()
        

    result= cursor.fetchall()
    with open(args.output_file[0], 'w', newline='') as file:
        writer = csv.writer(file)
        fields= ["date", "url", "visits"]
        writer.writerow(fields)
        for row in result:
            
            writer.writerow([row[0], row[1],row[2]])

    db_conn.close()
    
def parse_chrome(args):
    try:
        db_conn = sqlite3.connect(args.file[0])
    except sqlite3.OperationalError:
        print(f"unable to open database at {args.file[0]}")
        exit()
    cursor= db_conn.cursor()
    query='''SELECT datetime((visits.visit_time/ 1000000) - 11644473600, 'unixepoch','localtime') AS VisitDate,
urls.url as URL, urls.visit_count as NumberOfVisits
FROM urls
INNER JOIN
visits ON urls.id = visits.url
ORDER BY 
urls.visit_count DESC;'''
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        check_errors(e)
        exit
    result = cursor.fetchall()
    with open(args.output_file[0], 'w', newline='') as file:
        writer = csv.writer(file)
        fields = ["date","url","visits"]
        writer.writerow(fields)
        for row in result:
            writer.writerow([row[0],row[1],row[2]])
    db_conn.close()
def parse_edge(args):
    try:
        db_conn = sqlite3.connect(args.file[0])
    except sqlite3.OperationalError:
        print(f"unable to open database at {args.file[0]}")
        exit()
    cursor= db_conn.cursor()
    query='''
select  datetime(visits.visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') AS VisitDate,
urls.url as URL, urls.visit_count as NumberOfVisits
FROM urls 
INNER JOIN
visits ON urls.id = visits.url
ORDER BY
urls.visit_count DESC;'''
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        check_errors(e)
        exit
    result = cursor.fetchall()
    with open(args.output_file[0], 'w', newline='') as file:
        writer = csv.writer(file)
        fields = ["date","url","visits"]
        writer.writerow(fields)
        for row in result:
            writer.writerow([row[0],row[1],row[2]])
    db_conn.close()
    
if __name__ == "__main__":
    parser= argparse.ArgumentParser(description="Simple CSV Browser History Parser for Google Chrome, Firefox and Microsoft Edge")
    parser.add_argument("type",type=str, choices=TYPES,help="type of history file to parse")
    parser.add_argument("-f", "--file", type=str,nargs=1,help="path to browser history database, i.e History(Chrome,Edge), places.sqlite3(Firefox)",required=True)
    parser.add_argument("-o", "--output-file", type=str,nargs=1,help="path to output file (csv)", required=True)
    parser.add_argument("-g","--graph", action='store_true',help="create graph of top 10 dates and destinations")
    parsed_args=parser.parse_args()
    
    check_input_file(parsed_args)
    
    process_file(parsed_args)
    if (parsed_args.graph):
        create_graphs(parsed_args.output_file[0])
    
    
    