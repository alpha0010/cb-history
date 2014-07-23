import xml.etree.ElementTree as ET
import datetime as DT
import cgi
import json
import codecs
import re
import math
import bz2
import os

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
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>$$SCRIPT$$
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
      <ul class="nav nav-pills">
        <li class="dropdown">
          <a data-toggle="dropdown" href="#">Status: $$FILTER_STATUS$$ <b class="caret"></b></a>
          <ul class="dropdown-menu" role="menu">
            <li><a tabindex="-1" href="$$FILTER_STATUS_ALT_URL$$">$$FILTER_STATUS_ALT$$</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a data-toggle="dropdown" href="#">Assigned To: $$FILTER_ASSIGNED$$ <b class="caret"></b></a>
          <ul class="dropdown-menu" role="menu">
            $$ASSIGNED_OPTIONS$$
          </ul>
        </li>
      </ul>

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

patchEntryTemplate = r"""<tr><td>$$NUMBER$$</td><td><a href="patches/$$NUMBER$$.html">$$SUMMARY$$</a></td><td>$$CATEGORY$$</td><td>$$STATUS$$</td><td>$$OPEN_DATE$$</td><td>$$ASSIGNED$$</td><td>$$AUTHOR$$</td></tr>"""

assignedFilterTemplate = r"""<li><a tabindex="-1" href="$$URL$$">$$NAME$$</a></li>"""

urlRe = re.compile(ur'(((ht|f)tp(s?)\:\/\/)|(www\.))(([a-zA-Z0-9\-\._]+(\.[a-zA-Z0-9\-\._]+)+)|localhost)(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?([\d\w\.\/\%\+\-\=\&amp;\?\:\\\&quot;\'\,\|\~\;]*)')

bugRe     = re.compile(ur'bug_id=([0-9]+)')
featureRe = re.compile(ur'feature_id=([0-9]+)')
patchRe   = re.compile(ur'patch_id=([0-9]+)')

linkTipDict = {}
for line in open("data/linkTips.txt"):
    parts = line.strip().split(" ", 1)
    linkTipDict[parts[0]] = parts[1]

def getMappedUrl(url):
    if "group_id=5358" in url:
        urlMatch = re.search(bugRe, url)
        if urlMatch:
            return ["../bugs/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(featureRe, url)
        if urlMatch:
            return ["../features/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(patchRe, url)
        if urlMatch:
            return [urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
    return [url, ""]

ticketRe = re.compile(ur'\b(patch|bug|features? +requests?|features?|requests?) *(?::|is|fix)? *#? *(\d{3,6})\b', re.IGNORECASE)

def ticketLinker(matches):
    url = "group_id=5358"
    if matches.group(1).lower() == "patch":
        url += "patch"
    elif matches.group(1).lower() == "bug":
        url += "bug"
    else:
        url += "feature"
    url += "_id=" + matches.group(2).lstrip("0")
    if "bug_id=6607" in url: # sorry, this bug does not exist
        return matches.group(0)
    url = getMappedUrl(url)
    return '<a href="' + url[0] + '" data-toggle="tooltip" title="' + url[1] + '">' + matches.group(0) + '</a>'

fHandle = bz2.BZ2File("data/berlios.json.bz2", "r")
lookupDb = json.load(fHandle)
fHandle.close()
# hardcode a few (known) values that are not in the older dump by Jens with ForgePlucker
statusDb = { 3523: {"status": "Accepted", "category": "Application::Bugfix"},
             3524: {"status": "Open", "category": "Application::Refinement"},
             3529: {"status": "Open", "category": "Application::FeatureAdd"},
             3552: {"status": "Open", "category": "Plugin::Refinement"},
             3553: {"status": "Open", "category": "Lexer"},
             3554: {"status": "Open", "category": "Application::FeatureAdd"},
             3555: {"status": "Open", "category": "Application::FeatureAdd"},
             3556: {"status": "Accepted", "category": "Application::Refinement"},
             3557: {"status": "Open", "category": "Plugin::Refinement"},
             3558: {"status": "Open", "category": "Plugin::Refinement"},
             3559: {"status": "Open", "category": "Plugin::Refinement"},
             3560: {"status": "Open", "category": "Plugin::Refinement"},
             3561: {"status": "Open", "category": "Plugin::FeatureAdd"},
             3563: {"status": "Open", "category": "Plugin::Bugfix"},
             3564: {"status": "Open", "category": "Plugin::Refinement"},
             3565: {"status": "Open", "category": "Plugin::Refinement"},
             3566: {"status": "Open", "category": "Plugin::Bugfix"} }
for patch in lookupDb["trackers"]["patches"]["artifacts"]:
    categ = "&nbsp;" if patch["category"] == "None" else patch["category"]
    statusDb[patch["id"]] = { "status": patch["status"], "category": categ }

ticketsOut = []
fHandle = bz2.BZ2File("data/bs_patches_0.1.xml.bz2", "r")
docTree = ET.parse(fHandle)
fHandle.close()

userIdDict = {}
devList = {}
for ticket in docTree.getroot():
    for prop in ticket:
        if prop.tag == "submitted_by":
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]
        elif prop.tag == "assigned_to" and prop.attrib["name"] != "none":
            if prop.attrib["name"] in devList:
                devList[prop.attrib["name"]] += 1
            else:
                devList[prop.attrib["name"]] = 1
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]
openCnt = 0

debugLimit = 60 # limit ticket conversion for debugging

for ticket in docTree.getroot():
    ticketOut = { "$$NUMBER$$": ticket.attrib["id"] }
    lastMod = 0
    for prop in ticket:
        if prop.tag == "submitted_by":
            ticketOut["$$AUTHOR$$"] = cgi.escape(prop.attrib["name"])

        elif prop.tag == "assigned_to":
            if prop.attrib["name"] == "none":
                ticketOut["$$ASSIGNED$$"] = "&nbsp;"
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
                ticketOut["$$CLOSE_DATE$$"] = "&nbsp;"
            if int(ticket.attrib["id"]) in statusDb:
                if statusDb[int(ticket.attrib["id"])]["status"] != "Open": # statusDb *might* be out of date
                    ticketOut["$$STATUS$$"] = statusDb[int(ticket.attrib["id"])]["status"]
                ticketOut["$$CATEGORY$$"] = statusDb[int(ticket.attrib["id"])]["category"]
            if ticketOut["$$STATUS$$"] == "Open":
                openCnt += 1

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
                        urlDat = getMappedUrl(urlMatch.group(0))
                        if urlDat[1] == "":
                            para = para.replace(urlMatch.group(0), '<a href="' + urlDat[0] + '">' + urlMatch.group(0) + '</a>')
                        else:
                            para = para.replace(urlMatch.group(0), '<a href="' + urlDat[0] + '" data-toggle="tooltip" title="' + urlDat[1] + '">' + urlMatch.group(0) + '</a>')
                    para = ticketRe.sub(ticketLinker, para)
                    post["$$COMMENTS$$"] += "<p>" + para + "</p>"
            ticketOut["HISTORY"].append(post)
            lastMod = max(lastMod, int(prop[3].text))

        elif prop.tag == "code": #and prop.text != "InvalidBinaryFile":
            ticketOut["code"] = prop.text

    if "HISTORY" not in ticketOut:
        ticketOut["$$HISTORY$$"] = ""
    ticketsOut.append(ticketOut)

    debugLimit -= 1
#    if debugLimit <= 0:
#        break

if not os.path.isdir("static_web/patches"):
    os.mkdir("static_web/patches")

for ticket in ticketsOut:
    ticketHTML = patchTemplate
    for key in ticket:
        if key == "$$SUMMARY$$":
            ticketHTML = ticketHTML.replace(key, ticketRe.sub(ticketLinker, ticket[key]))
        elif key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
        elif key == "code":
            f = codecs.open("static_web/patches/" + ticket["$$SHORT_NAME$$"] + ".patch", "w+", "utf-8")
            f.write(ticket[key])
            f.close()
        else:
            history = ""
            for comment in sorted(ticket[key], key=lambda cm: cm["$$TIME_STAMP$$"]):
                cmt = commentTemplate
                for cmtKey in comment:
                    cmt = cmt.replace(cmtKey, comment[cmtKey])
                if len(history) > 0:
                    history += "\n      "
                history += cmt
            ticketHTML = ticketHTML.replace("$$" + key + "$$", history)
    if "data-toggle=\"tooltip\"" in ticketHTML:
        ticketHTML = ticketHTML.replace("$$SCRIPT$$", """
    <script>
      $(document).ready(function() {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });
      });
    </script>""")
    else:
        ticketHTML = ticketHTML.replace("$$SCRIPT$$", "")
    f = codecs.open("static_web/patches/" + ticket["$$NUMBER$$"] + ".html", "w+", "utf-8")
    f.write(ticketHTML)
    f.close()


ticketsOut.sort(key=lambda tk: -int(tk["$$NUMBER$$"]))
patchList = ""

numPages = int(math.ceil(len(ticketsOut) / 50.0))
numPerPage = int(math.ceil(len(ticketsOut) / (numPages + 0.0)))
numOutput = 0

def getPagination(fileBrand):
    pagination = "<li"
    if numOutput / numPerPage == 1:
        pagination += ' class="disabled"><span>&laquo;</span></li>'
    elif numOutput / numPerPage == 2:
        pagination += '><a href="patches' + fileBrand + '.html">&laquo;</a></li>'
    else:
        pagination += '><a href="patches' + fileBrand + str(numOutput / numPerPage - 1) + '.html">&laquo;</a></li>'
    for i in range(1, numPages + 1):
        if i == numOutput / numPerPage:
            pagination += '<li class="active"><span>' + str(i) + '</span></li>'
        elif i == 1:
            pagination += '<li><a href="patches' + fileBrand + '.html">1</a></li>'
        else:
            pagination += '<li><a href="patches' + fileBrand + str(i) + '.html">' + str(i) + '</a></li>'
    if numOutput / numPerPage == numPages:
        pagination += '<li class="disabled"><span>&raquo;</span></li>'
    else:
        pagination += '<li><a href="patches' + fileBrand + str(numOutput / numPerPage + 1) + '.html">&raquo;</a></li>'
    return pagination

def getAssignedOpts(curDev):
    opts = ""
    if curDev != "Any":
        opts += r"""<li><a tabindex="-1" href="patches.html">Any</a></li>
            <li class=divider></li>"""
    for devNm in sorted(devList):
        if devNm == curDev:
            continue
        if len(opts) > 0:
            opts += "\n            "
        row = assignedFilterTemplate.replace("$$NAME$$", devNm)
        opts += row.replace("$$URL$$", "patches_" + devNm + ".html")
    return opts

def writePatchList(status, statusAlt, statusAltUrl, curDev, fileBrand):
    global patchList
    patchList = patchListTemplate.replace("$$PATCHES$$", patchList)
    patchList = patchList.replace("$$PAGINATION$$", getPagination(fileBrand))
    patchList = patchList.replace("$$FILTER_STATUS$$", status)
    patchList = patchList.replace("$$FILTER_STATUS_ALT$$", statusAlt)
    patchList = patchList.replace("$$FILTER_STATUS_ALT_URL$$", statusAltUrl)
    patchList = patchList.replace("$$FILTER_ASSIGNED$$", curDev)
    patchList = patchList.replace("$$ASSIGNED_OPTIONS$$", getAssignedOpts(curDev))
    flExt = ".html"
    if numOutput / numPerPage > 1:
        flExt = str(numOutput / numPerPage) + flExt
    f = open("static_web/patches" + fileBrand + flExt, "w+")
    f.write(patchList)
    f.close()
    patchList = ""

# the full listing
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
        writePatchList("Any", "Open", "patches_open.html", "Any", "")
if len(patchList) > 0:
    numOutput = numPerPage * numPages
    writePatchList("Any", "Open", "patches_open.html", "Any", "")

# only open patches
numPages = int(math.ceil(openCnt / 50.0))
numPerPage = int(math.ceil(openCnt / (numPages + 0.0)))
numOutput = 0
for ticket in ticketsOut:
    if ticket["$$STATUS$$"] != "Open":
        continue
    ticketHTML = patchEntryTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
    if len(patchList) > 0:
        patchList += "\n          "
    patchList += ticketHTML
    numOutput += 1
    if numOutput % numPerPage == 0:
        writePatchList("Open", "Any", "patches.html", "Any", "_open")
if len(patchList) > 0:
    numOutput = numPerPage * numPages
    writePatchList("Open", "Any", "patches.html", "Any", "_open")

# only patches assigned to dev XXX
for devNm in devList:
    numPages = int(math.ceil(devList[devNm] / 50.0))
    numPerPage = int(math.ceil(devList[devNm] / (numPages + 0.0)))
    numOutput = 0
    for ticket in ticketsOut:
        if ticket["$$ASSIGNED$$"] != devNm:
            continue
        ticketHTML = patchEntryTemplate
        for key in ticket:
            if key.startswith("$$"):
                ticketHTML = ticketHTML.replace(key, ticket[key])
        if len(patchList) > 0:
            patchList += "\n          "
        patchList += ticketHTML
        numOutput += 1
        if numOutput % numPerPage == 0:
            writePatchList("Any", "Open", "patches_open.html", devNm, "_" + devNm)
    if len(patchList) > 0:
        numOutput = numPerPage * numPages
        writePatchList("Any", "Open", "patches_open.html", devNm, "_" + devNm)
