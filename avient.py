import mechanize as mc
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, make_response
import PyRSS2Gen
import os

URI = 'https://zeus.avient.aero/trackandtrace.aspx'
browser = mc.Browser()
browser.set_handle_robots(False)


def retrievePage(awb_prefix, awb_number):
    '''
    Retrieve the web document containing the tracking information
    '''
    try:
        browser.open(URI)
        browser.select_form("form1")
        browser.form['TextBox1'] = str(awb_prefix)
        browser.form['TextBox2'] = str(awb_number)
        response = browser.submit().read()
        return response
    except Exception:
        return ""


def parseSchedule(doc):
    '''
    Parse the document containing the tracking information into
    a structured format
    '''
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

    schedule.reverse() # return the list in a reversed order
    return schedule


def generateRss(schedule):
    '''
    Takes the structured shipping schedule and generates an RSS feed from it
    '''
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
    rss = generateRss(parseSchedule(retrievePage(awb_prefix, awb_number)))
    response = make_response(rss, 200)
    response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
