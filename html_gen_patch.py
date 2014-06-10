import xml.etree.ElementTree as ET
import datetime as DT
import cgi
import json
import codecs
import re
import math

patchTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Patch $$NUMBER$$ - Code::Blocks History</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body role="document">
    <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="http://www.codeblocks.org/">Code::Blocks</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../bugs.html">Bugs</a></li>
            <li><a href="../features.html">Features</a></li>
            <li class="active"><a href="../patches.html">Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
      <div class="row">
        <div class="col-sm-8">
          <h3>Patch #$$NUMBER$$ <small>$$OPEN_DATE$$</small></h3>
          <h4>$$AUTHOR$$</h4>
          $$SUMMARY$$
          <dl class="dl-horizontal">
            <dt>Download</dt>
            <dd><a href="$$SHORT_NAME$$.patch">$$SHORT_NAME$$.patch</a></dd>
          </dl>
        </div>
        <div class="col-sm-4">
          <dl class="dl-horizontal">
            <dt>Category</dt><dd>$$CATEGORY$$</dd>
            <dt>Status</dt><dd>$$STATUS$$</dd>
            <dt>Close date</dt><dd>$$CLOSE_DATE$$</dd>
            <dt>Assigned to</dt><dd>$$ASSIGNED$$</dd>
          </dl>
        </div>
      </div>
      <h4 class="page-header">History</h4>
      $$HISTORY$$
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
  </body>
</html>"""

commentTemplate = r"""<div class="panel panel-default">
        <div class="panel-heading">$$AUTHOR$$ $$TIME_STAMP$$</div>
        <div class="panel-body">
          $$COMMENTS$$
        </div>
      </div>"""


patchListTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Patches - Code::Blocks History</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body role="document">
    <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="http://www.codeblocks.org/">Code::Blocks</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="index.html">Home</a></li>
            <li><a href="bugs.html">Bugs</a></li>
            <li><a href="features.html">Features</a></li>
            <li class="active"><a>Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
      <table class="table table-hover table-condensed">
        <thead>
          <tr><th>Patch ID</th><th>Summary</th><th>Category</th><th>Status</th><th>Date</th><th>Assigned To</th><th>Submitted By</th></tr>
        </thead>
        <tbody>
          $$PATCHES$$
        </tbody>
      </table>
      <ul class="pagination">
        $$PAGINATION$$
      </ul>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""

patchEntryTemplate = r"""<tr><td>$$NUMBER$$</td><td><a href="patches/$$SHORT_NAME$$.html">$$SUMMARY$$</a></td><td>$$CATEGORY$$</td><td>$$STATUS$$</td><td>$$OPEN_DATE$$</td><td>$$ASSIGNED$$</td><td>$$AUTHOR$$</td></tr>"""

urlRe = re.compile(ur'(((ht|f)tp(s?)\:\/\/)|(www\.))(([a-zA-Z0-9\-\._]+(\.[a-zA-Z0-9\-\._]+)+)|localhost)(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?([\d\w\.\/\%\+\-\=\&amp;\?\:\\\&quot;\'\,\|\~\;]*)')

fHandle = open("old_dump/berlios.json", "r")
lookupDb = json.load(fHandle)
fHandle.close()
statusDb = {}
for patch in lookupDb["trackers"]["patches"]["artifacts"]:
    statusDb[patch["id"]] = { "status": patch["status"], "category": patch["category"] }

ticketsOut = []
docTree = ET.parse('bs_patches_0.1.xml')

userIdDict = {}
for ticket in docTree.getroot():
    for prop in ticket:
        if prop.tag == "submitted_by":
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]
        elif prop.tag == "assigned_to" and prop.attrib["name"] != "none":
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]

debugLimit = 60 # limit ticket conversion for debugging

for ticket in docTree.getroot():
    ticketOut = { "$$NUMBER$$": ticket.attrib["id"] }
    lastMod = 0
    for prop in ticket:
        if prop.tag == "submitted_by":
            ticketOut["$$AUTHOR$$"] = cgi.escape(prop.attrib["name"])

        elif prop.tag == "assigned_to":
            if prop.attrib["name"] == "none":
                ticketOut["$$ASSIGNED$$"] = ""
            else:
                ticketOut["$$ASSIGNED$$"] = cgi.escape(prop.attrib["name"])

        elif prop.tag == "summary":
            ticketOut["$$SUMMARY$$"] = cgi.escape(prop.text)
            ticketOut["$$SHORT_NAME$$"] = ticket.attrib["id"] + "-"
            for ch in prop.text:
                if len(ticketOut["$$SHORT_NAME$$"]) > 18:
                    ticketOut["$$SHORT_NAME$$"] = ticketOut["$$SHORT_NAME$$"].rstrip("_")
                    break
                if ch.isalnum():
                    ticketOut["$$SHORT_NAME$$"] += ch
                elif not ticketOut["$$SHORT_NAME$$"].endswith("_") and not ticketOut["$$SHORT_NAME$$"].endswith("-"):
                    ticketOut["$$SHORT_NAME$$"] += "_"

        elif prop.tag == "open_date":
            ticketOut["$$OPEN_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")
            lastMod = max(lastMod, int(prop.text))

        elif prop.tag == "close_date":
            if int(prop.text) > 0:
                ticketOut["$$STATUS$$"] = "Closed"
                lastMod = max(lastMod, int(prop.text))
                ticketOut["$$CLOSE_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")
            else:
                ticketOut["$$STATUS$$"] = "Open"
                ticketOut["$$CLOSE_DATE$$"] = ""
            if int(ticket.attrib["id"]) in statusDb:
                ticketOut["$$STATUS$$"] = statusDb[int(ticket.attrib["id"])]["status"]
                ticketOut["$$CATEGORY$$"] = statusDb[int(ticket.attrib["id"])]["category"]

        elif prop.tag == "history" and prop[0].text == "details":
            if "HISTORY" not in ticketOut:
                ticketOut["HISTORY"] = []
            post = { "$$COMMENTS$$": "",
                     "$$AUTHOR$$": (cgi.escape(userIdDict[ prop[2].text ]) if prop[2].text in userIdDict else "ID_" + prop[2].text),
                     "$$TIME_STAMP$$": DT.datetime.utcfromtimestamp(int(prop[3].text)).isoformat(" ") }
            for para in prop[1].text.split("\n"):
                if len(para) > 0 and not para.isspace():
                    if len(post["$$COMMENTS$$"]) > 0:
                        post["$$COMMENTS$$"] += "\n          "
                    para = cgi.escape(para.strip())
                    urlMatch = re.search(urlRe, para)
                    if urlMatch:
                        para = para.replace(urlMatch.group(0), '<a href="' + urlMatch.group(0) + '">' + urlMatch.group(0) + '</a>')
                    post["$$COMMENTS$$"] += "<p>" + para + "</p>"
            ticketOut["HISTORY"].append(post)
            lastMod = max(lastMod, int(prop[3].text))

        elif prop.tag == "code": #and prop.text != "InvalidBinaryFile":
            ticketOut["code"] = prop.text

#    ticketOut["mod_date"] = DT.datetime.utcfromtimestamp(lastMod + 1).isoformat(" ") + ".000000"
    ticketsOut.append(ticketOut)

    debugLimit -= 1
#    if debugLimit <= 0:
#        break

for ticket in ticketsOut:
    ticketHTML = patchTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
        elif key == "code":
            f = codecs.open("static_web/patches/" + ticket["$$SHORT_NAME$$"] + ".patch", "w+", "utf-8")
            f.write(ticket[key])
            f.close()
        else:
            history = ""
            for comment in ticket[key]:
                cmt = commentTemplate
                for cmtKey in comment:
                    cmt = cmt.replace(cmtKey, comment[cmtKey])
                if len(history) > 0:
                    history += "\n      "
                history += cmt
            ticketHTML = ticketHTML.replace("$$" + key + "$$", history)
    f = codecs.open("static_web/patches/" + ticket["$$SHORT_NAME$$"] + ".html", "w+", "utf-8")
    f.write(ticketHTML)
    f.close()


ticketsOut = sorted(ticketsOut, key=lambda tk: -int(tk["$$NUMBER$$"]))
patchList = ""

numPages = int(math.ceil(len(ticketsOut) / 50.0))
numPerPage = int(math.ceil(len(ticketsOut) / (numPages + 0.0)))
numOutput = 0

def getPagination():
    pagination = "<li"
    if numOutput / numPerPage == 1:
        pagination += ' class="disabled"><span>&laquo;</span></li>'
    elif numOutput / numPerPage == 2:
        pagination += '><a href="patches.html">&laquo;</a></li>'
    else:
        pagination += '><a href="patches' + str(numOutput / numPerPage - 1) + '.html">&laquo;</a></li>'
    for i in range(1, numPages + 1):
        if i == numOutput / numPerPage:
            pagination += '<li class="active"><span>' + str(i) + '</span></li>'
        elif i == 1:
            pagination += '<li><a href="patches.html">1</a></li>'
        else:
            pagination += '<li><a href="patches' + str(i) + '.html">' + str(i) + '</a></li>'
    if numOutput / numPerPage == numPages:
        pagination += '<li class="disabled"><span>&raquo;</span></li>'
    else:
        pagination += '<li><a href="patches' + str(numOutput / numPerPage + 1) + '.html">&raquo;</a></li>'
    return pagination

for ticket in ticketsOut:
    ticketHTML = patchEntryTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
    if len(patchList) > 0:
        patchList += "\n          "
    patchList += ticketHTML
    numOutput += 1
    if numOutput % numPerPage == 0:
        patchList = patchListTemplate.replace("$$PATCHES$$", patchList)
        patchList = patchList.replace("$$PAGINATION$$", getPagination())
        flExt = ".html"
        if numOutput / numPerPage > 1:
            flExt = str(numOutput / numPerPage) + flExt
        f = open("static_web/patches" + flExt, "w+")
        f.write(patchList)
        f.close()
        patchList = ""
if len(patchList) > 0:
    numOutput = numPerPage * numPages
    patchList = patchListTemplate.replace("$$PATCHES$$", patchList)
    patchList = patchList.replace("$$PAGINATION$$", getPagination())
    flExt = ".html"
    if numOutput / numPerPage > 1:
        flExt = str(numOutput / numPerPage) + flExt
    f = open("static_web/patches" + flExt, "w+")
    f.write(patchList)
    f.close()

