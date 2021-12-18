#!/usr/bin/python
import requests
import csv
import json
import email.utils
import smtplib
import email.message
from libs.argument_manager import ArgumentManager
from google.cloud import bigquery
from google.oauth2 import service_account
from email.mime.base import MIMEBase
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
import os
import pytz
import subprocess

last_hour_date_time = datetime.now(pytz.timezone('Turkey')) - timedelta(hours = 1)
dayandhour=last_hour_date_time.strftime('%A-%H:%M:%S')
day=dayandhour.split('-')[0]
hour=dayandhour.split('-')[-1]



def send_mail(path,passw,messages):
    print("send mail")
    sender = 'alert@test.com'
    receivers = 'mail@test.com'
    filetosend = path
    name = filetosend.split('/')[-1]
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = "Subject: Event Checker"
    with open(filetosend, 'rt') as file:
        msg.attach(MIMEApplication(file.read(), Name=f"{name}"))
    smtpObj = smtplib.SMTP('${mailserver}', ${serverport})
    smtpObj.connect('${mailserver}', ${serverport})
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login('alert@test.com', passw)
    smtpObj.sendmail(sender, receivers, msg.as_string())


def opsgeniealert(name,message,priority):
    url = "${opsgenieurl}"
    payloads = {
    "message": f"{message}",
    "alias": f'{name}',
    "description":"Alert",
    "tags": ["environment:Production","Event"],
    "entity":f'{name}',
    "priority":f"{priority}"
    }
    response = requests.post(url, data=json.dumps(payloads), headers={'Authorization': "GenieKey ${key}",
                                           'Content-Type': 'application/json'}, verify=True)
    response = response.json()
    print(response)


def addlinecsvfile(path,name,team,per,count,average,state,type): 
    #this section need to create control csv file to developer
    with open(path, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([day,hour,name, team,per,count,average,state,type])

def get_bq_count(passw,query,name,path):
    credentials = service_account.Credentials.from_service_account_file("{credentials}")
    queryfile = open(query,"r")
    myquery = queryfile.read()
    client = bigquery.Client(credentials=credentials)
    job = client.query(myquery)
    result = job.result()
    for row in result:
        message=""
        try:
            if (row.per > 100 and row.per < 200):
                percent = row.per % 100
            elif row.per < 100:
                percent = 100 - row.per
            else:
                percent = row.per
            if row.value == 'false':
                if hasattr(row, "type"):
                    opsgeniealias = name + " " + row.team + " " + row.type
                    msg = f'Alert to {name}  {row.team} {row.state} {row.type}. Mean value percentage: {percent} .Count:{row.Count},Average:{row.average}'
                    #addlinecsvfile(path, name, row.team, percent, row.Count, row.average, row.state, row.type)
                elif hasattr(row, "state"):
                    opsgeniealias = name + " " + row.team + " " + row.state
                    msg = f'Alert to {name}  {row.team} {row.state}. Mean value percentage: {percent}. Count:{row.Count},Average:{row.average}'
                    #addlinecsvfile(path, name, row.team, percent, row.Count, row.average, row.state)
                else:
                    opsgeniealias = name + " " + row.team
                    msg = f'Alert to {name}  {row.team}. Mean value percentage: {percent}. Count:{row.Count},Average:{row.average}'
                    #addlinecsvfile(path, name, row.team, percent, row.Count, row.average)
                priority = 'P3'
                #opsgeniealert(opsgeniealias, msg, priority)
                #send_mail(path,percent, value, passw,msg)
        except AttributeError as error:
            print(error)



if __name__ == '__main__':
    args = ArgumentManager().get_arguments()
    password = args.password
    path = args.path
    query = args.query
    id = args.id
    name = query.strip('./')
    path = f'{path}/{name}{id}.csv'
    with open(path, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["day","hour","name", "team", "per", "Count", "average", "state", "type"])
    get_bq_count(password,query,name,path)

