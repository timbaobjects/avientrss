import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, make_response
import PyRSS2Gen
import os

URI = 'https://zeus.avient.aero/trackandtrace.aspx'


def retrievePage(awb_prefix, awb_number):
    payload = {
        'TextBox1': awb_prefix,
        'TextBox2': awb_number,
        'Button1': 'Track and Trace',
        '__EVENTVALIDATION': '/wEWBALbm8qqCwLs0bLrBgLs0fbZDAKM54rGBoU3gPiyt+gyP37IknYl6tMjxOpp',
        '__VIEWSTATE': '/wEPDwUJNzQwMzI3OTUwD2QWAgIDD2QWAgIPDzwrAA0AZBgBBQlHcmlkVmlldzEPZ2QWHTsBCfKToIb33Zc5OTKlTn+7zA=='
    }
    headers = {
        'referer': 'https://zeus.avient.aero/trackandtrace.aspx'
    }
    try:
        response = requests.post("https://zeus.avient.aero/trackandtrace.aspx", data=payload, headers=headers)
    except Exception:
        pass
    return response


def parseSchedule(doc):
    soup = BeautifulSoup(doc)
    schedule = []

    for row in soup.find_all('tr')[1:]:
        cells = row.find_all('td')
        schedule.append({
            'status': cells[0].text.strip(),
            'station': cells[1].text.strip(),
            'date': datetime.strptime(cells[2].text.strip(), '%d/%m/%Y %H:%M:%S'),
            'desc': cells[3].text.strip(),
            'pcs': int(cells[4].text.strip()),
            'pallets': cells[5].text.strip()
        })
    return schedule


def generateRss(schedule):
    rss = PyRSS2Gen.RSS2(
        title="Avient Track and Trace",
        link=URI,
        description="An RSS feed for Avient's shipment tracking service",
        lastBuildDate=datetime.utcnow(),
        items=[
            PyRSS2Gen.RSSItem(
                title=item['desc'],
                link=URI,
                description=item['desc'],
                pubDate=item['date'],
            )
            for item in schedule
        ])
    return rss.to_xml()

app = Flask(__name__)


@app.route("/")
def smile():
    return ":)"


@app.route("/rss/<int:awb_prefix>/<int:awb_number>")
def avient_rss(awb_prefix, awb_number):
    rss = generateRss(parseSchedule(retrievePage(awb_prefix, awb_number).text))
    response = make_response(rss, 200)
    response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
