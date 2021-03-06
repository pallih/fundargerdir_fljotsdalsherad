# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import requests
import urlparse
from dateutil import parser

BASE_URL = "http://www.fljotsdalsherad.is"
DATA_URL = "http://www.fljotsdalsherad.is/is/stjornsysla/fundargerdir"

r = requests.get(DATA_URL)
root = lxml.html.fromstring(r.text)
items = root.xpath("//div[@id='meetingContent']/ul/li/a")

data = []
for item in items:
    meeting = {}
    date, committee = item.text.split("-", 1)
    meeting["titill"] = item.text
    meeting["url"] = urlparse.urljoin(BASE_URL, item.attrib["href"])
    meeting["dagsetning"] = date.strip()
    meeting["date"] = parser.parse(date.strip())
    meeting["nefnd"] = committee.strip()
    data.append(meeting)
scraperwiki.sqlite.save(unique_keys=['url'],
                        data=data)
