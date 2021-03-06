import xml.etree.ElementTree as ET
import datetime as DT
import cgi
import codecs
import re
import math
import bz2
import os
import shutil

bugTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bug $$NUMBER$$ - Code::Blocks History</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css">
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
            <li class="active"><a href="../bugs.html">Bugs</a></li>
            <li><a href="../features.html">Features</a></li>
            <li><a href="../patches.html">Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
      <div class="row">
        <div class="col-sm-8">
          <h3>Bug #$$NUMBER$$ <small>$$OPEN_DATE$$</small></h3>
          <h4>$$AUTHOR$$</h4>
          <p class="lead">$$SUMMARY$$</p>
          $$DETAILS$$
        </div>
        <div class="col-sm-4">
          <dl class="dl-horizontal">
            <dt>Category</dt><dd>$$CATEGORY$$</dd>
            <dt>Group</dt><dd>$$GROUP$$</dd>
            <dt>Status</dt><dd>$$STATUS$$</dd>
            <dt>Close date</dt><dd>$$CLOSE_DATE$$</dd>
            <dt>Assigned to</dt><dd>$$ASSIGNED$$</dd>
          </dl>
        </div>
      </div>
      <h4 class="page-header">History</h4>
      $$HISTORY$$
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>$$SCRIPT$$
  </body>
</html>
"""

commentTemplate = r"""<div class="panel panel-default">
        <div class="panel-heading">$$AUTHOR$$ $$TIME_STAMP$$</div>
        <div class="panel-body">
          $$COMMENTS$$
        </div>
      </div>"""


bugListTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bugs - Code::Blocks History</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css">
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
            <li class="active"><a>Bugs</a></li>
            <li><a href="features.html">Features</a></li>
            <li><a href="patches.html">Patches</a></li>
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
          <tr><th>Bug ID</th><th>Summary</th><th>Category</th><th>Platform</th><th>Status</th><th>Date</th><th>Assigned To</th><th>Submitted By</th></tr>
        </thead>
        <tbody>
          $$BUGS$$
        </tbody>
      </table>
      <ul class="pagination">
        $$PAGINATION$$
      </ul>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  </body>
</html>
"""

bugEntryTemplate = r"""<tr><td>$$NUMBER_STAT$$</td><td><a href="bugs/$$NUMBER$$.html">$$SUMMARY$$</a></td><td>$$CATEGORY$$</td><td>$$PLATFORM$$</td><td>$$STATUS$$</td><td>$$OPEN_DATE$$</td><td>$$ASSIGNED$$</td><td>$$AUTHOR$$</td></tr>"""

assignedFilterTemplate = r"""<li><a tabindex="-1" href="$$URL$$">$$NAME$$</a></li>"""

spaceRe = re.compile(ur'        .*\n.*        ', re.DOTALL)

urlRe = re.compile(ur'(((ht|f)tp(s?)\:\/\/)|(www\.))(([a-zA-Z0-9\-\._]+(\.[a-zA-Z0-9\-\._]+)+)|localhost)(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?([\d\w\.\/\%\+\-\=\&amp;\?\:\\\&quot;\'\,\|\~\;]*)')

bugRe     = re.compile(ur'bug_id=([0-9]+)')
featureRe = re.compile(ur'feature_id=([0-9]+)')
patchRe   = re.compile(ur'patch_id=([0-9]+)')
forumsRe  = re.compile(ur'forums\.codeblocks\.org\S+?topic[=,]([0-9]+)')

linkTipDict = {}
for line in open("data/linkTips.txt"):
    parts = line.strip().split(" ", 1)
    linkTipDict[parts[0]] = parts[1]

def getMappedUrl(url):
    if "group_id=5358" in url:
        urlMatch = re.search(bugRe, url)
        if urlMatch:
            return [urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(featureRe, url)
        if urlMatch:
            return ["../features/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(patchRe, url)
        if urlMatch:
            return ["../patches/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
    if "forums" in url:
        urlMatch = re.search(forumsRe, url)
        if urlMatch:
            return [url, linkTipDict["forums=" + urlMatch.group(1)]]
    if url in linkTipDict:
        return [url, linkTipDict[url]]
    return [url, ""]

def makeLink(url):
    urlDat = getMappedUrl(url)
    if urlDat[1] == "":
        return '<a href="' + cgi.escape(urlDat[0]) + '">' + cgi.escape(url) + '</a>'
    else:
        return '<a href="' + urlDat[0] + '" data-toggle="tooltip" title="' + urlDat[1] + '">' + cgi.escape(url) + '</a>'


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
    if "bug_id=5695" in url: # oops, regex found something it shouldn't
        return matches.group(0)
    elif "bug_id=16654" in url: # what? ... missing from data dump?
        return matches.group(0)
    url = getMappedUrl(url)
    return '<a href="' + url[0] + '" data-toggle="tooltip" title="' + url[1] + '">' + matches.group(0) + '</a>'


categoryDict = { "100": "&nbsp;",
                 "1381": "Application::Crash",
                 "1383": "Application::Editor",
                 "1387": "Application::Error",
                 "1382": "Application::Interface",
                 "1386": "Application::Localisation",
                 "1390": "Application::WrongBehaviour",
                 "1391": "Compiler",
                 "1392": "Debugger",
                 "1389": "Plugin::Any",
                 "1384": "Plugin::CodeCompletion",
                 "1388": "Plugin::SourceFormatter",
                 "1385": "Plugin::wxSmith" }

groupDict = { "100": "&nbsp;",
              "1000": "Platform:Linux",
              "1001": "Platform:Mac",
              "1002": "Platform:Windows",
              "1003": "Platform:All" }

# just groupDict without the "Platform"
platformDict = { "100": "&nbsp;",
                "1000": "Linux",
                "1001": "Mac",
                "1002": "Windows",
                "1003": "All" }

statusDict = { "100": "&nbsp;",
               "1": "Open",
               "3": "Closed" }

ticketsOut = []
fHandle = bz2.BZ2File("data/bs_bugs_0.1.xml.bz2", "r")
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

debugLimit = 1 # limit ticket conversion for debugging

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

        elif prop.tag == "details":
            if len(prop.text) > 2000 or "===================================================================" in prop.text or spaceRe.search(prop.text):
                lastIdx = 0
                para = ""
                for match in urlRe.finditer(prop.text):
                    para += ticketRe.sub(ticketLinker, cgi.escape(prop.text[lastIdx:match.start()]))
                    para += makeLink(match.group(0))
                    lastIdx = match.end()
                if ticketOut["$$NUMBER$$"] == "18988": # HACK
                    para += prop.text[lastIdx:]
                else:
                    para += ticketRe.sub(ticketLinker, cgi.escape(prop.text[lastIdx:]))
                ticketOut["$$DETAILS$$"] = '<pre class="pre-scrollable">' + para + '</pre>'
                continue
            ticketOut["$$DETAILS$$"] = ""
            for para in prop.text.split("\n"):
                if len(para) > 0 and not para.isspace():
                    if len(ticketOut["$$DETAILS$$"]) > 0:
                        ticketOut["$$DETAILS$$"] += "\n          "
                    lastIdx = 0
                    lineTxt = ""
                    for match in urlRe.finditer(para):
                        lineTxt += ticketRe.sub(ticketLinker, cgi.escape(para[lastIdx:match.start()]))
                        lineTxt += makeLink(match.group(0))
                        lastIdx = match.end()
                    lineTxt += ticketRe.sub(ticketLinker, cgi.escape(para[lastIdx:]))
                    ticketOut["$$DETAILS$$"] += "<p>" + lineTxt.strip() + "</p>"

        elif prop.tag == "date":
            ticketOut["$$OPEN_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")[:-3]
            lastMod = max(lastMod, int(prop.text))

        elif prop.tag == "close_date":
            if int(prop.text) > 0:
                ticketOut["$$CLOSE_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")[:-3]
            else:
                ticketOut["$$CLOSE_DATE$$"] = "&nbsp;"

        elif prop.tag == "history" and prop[0].text == "details":
            if "HISTORY" not in ticketOut:
                ticketOut["HISTORY"] = []
            post = { "$$COMMENTS$$": "",
                     "$$AUTHOR$$": (cgi.escape(userIdDict[ prop[2].text ]) if prop[2].text in userIdDict else "ID_" + prop[2].text),
                     "$$TIME_STAMP$$": DT.datetime.utcfromtimestamp(int(prop[3].text)).isoformat(" ")[:-3] }
            if len(prop[1].text) > 2000 or "===================================================================" in prop[1].text or spaceRe.search(prop[1].text):
                lastIdx = 0
                para = ""
                for match in urlRe.finditer(prop[1].text):
                    para += ticketRe.sub(ticketLinker, cgi.escape(prop[1].text[lastIdx:match.start()]))
                    para += makeLink(match.group(0))
                    lastIdx = match.end()
                para += ticketRe.sub(ticketLinker, cgi.escape(prop[1].text[lastIdx:]))
                post["$$COMMENTS$$"] = '<pre class="pre-scrollable">' + para + '</pre>'
            else:
                for para in prop[1].text.split("\n"):
                    if len(para) > 0 and not para.isspace():
                        if len(post["$$COMMENTS$$"]) > 0:
                            post["$$COMMENTS$$"] += "\n          "
                        lastIdx = 0
                        lineTxt = ""
                        for match in urlRe.finditer(para):
                            lineTxt += ticketRe.sub(ticketLinker, cgi.escape(para[lastIdx:match.start()]))
                            lineTxt += makeLink(match.group(0))
                            lastIdx = match.end()
                        lineTxt += ticketRe.sub(ticketLinker, cgi.escape(para[lastIdx:]))
                        post["$$COMMENTS$$"] += "<p>" + lineTxt.strip() + "</p>"
            ticketOut["HISTORY"].append(post)
            lastMod = max(lastMod, int(prop[3].text))

        elif prop.tag == "bug_group_id":
            ticketOut["$$GROUP$$"] = groupDict[prop.text]
            ticketOut["$$PLATFORM$$"] = platformDict[prop.text]

        elif prop.tag == "category_id":
            ticketOut["$$CATEGORY$$"] = categoryDict[prop.text]

        elif prop.tag == "status_id":
            ticketOut["$$STATUS$$"] = statusDict[prop.text]
            if ticketOut["$$STATUS$$"] == "Open":
                openCnt += 1

    if "HISTORY" not in ticketOut:
        ticketOut["$$HISTORY$$"] = ""
        ticketOut["$$NUMBER_STAT$$"] = ticketOut["$$NUMBER$$"]
    else:
        ticketOut["$$NUMBER_STAT$$"] = '<table style="width:100%%"><tr><td>%s</td><td class="text-right"><span class="badge">%d</span></td></tr></table>' % (ticketOut["$$NUMBER$$"], len(ticketOut["HISTORY"]))
    ticketsOut.append(ticketOut)

    debugLimit -= 1
    #if debugLimit <= 0:
    #    break

if not os.path.isdir("static_web"):
    os.mkdir("static_web")
if not os.path.isdir("static_web/bugs"):
    os.mkdir("static_web/bugs")
shutil.copy("data/index.html", "static_web/index.html")

for ticket in ticketsOut:
    ticketHTML = bugTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
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
    f = codecs.open("static_web/bugs/" + ticket["$$NUMBER$$"] + ".html", "w+", "utf-8")
    f.write(ticketHTML)
    f.close()


ticketsOut = sorted(ticketsOut, key=lambda tk: -int(tk["$$NUMBER$$"]))
bugList = ""

numPages = int(math.ceil(len(ticketsOut) / 50.0))
numPerPage = int(math.ceil(len(ticketsOut) / (numPages + 0.0)))
numOutput = 0

def getPagination(fileBrand):
    pagination = "<li"
    if numOutput / numPerPage == 1:
        pagination += ' class="disabled"><span>&laquo;</span></li>'
    elif numOutput / numPerPage == 2:
        pagination += '><a href="bugs' + fileBrand + '.html">&laquo;</a></li>'
    else:
        pagination += '><a href="bugs' + fileBrand + str(numOutput / numPerPage - 1) + '.html">&laquo;</a></li>'
    skipMin = 0
    skipMax = 0
    if numPages > 25:
        skipDelta = int(min(numPages / 3, numPages - 22))
        if numOutput / numPerPage < numPages / 2:
            skipMax = numPages - 2
            skipMin = skipMax - skipDelta
        else:
            skipMin = 3
            skipMax = skipMin + skipDelta
    for i in range(1, numPages + 1):
        if i == skipMin:
            pagination += '<li class="disabled"><span>&middot;&middot;&middot;</span></li>'
        elif i > skipMin and i <= skipMax:
            continue
        elif i == numOutput / numPerPage:
            pagination += '<li class="active"><span>' + str(i) + '</span></li>'
        elif i == 1:
            pagination += '<li><a href="bugs' + fileBrand + '.html">1</a></li>'
        else:
            pagination += '<li><a href="bugs' + fileBrand + str(i) + '.html">' + str(i) + '</a></li>'
    if numOutput / numPerPage == numPages:
        pagination += '<li class="disabled"><span>&raquo;</span></li>'
    else:
        pagination += '<li><a href="bugs' + fileBrand + str(numOutput / numPerPage + 1) + '.html">&raquo;</a></li>'
    return pagination

def getAssignedOpts(curDev):
    opts = ""
    if curDev != "Any":
        opts += r"""<li><a tabindex="-1" href="bugs.html">Any</a></li>
            <li class=divider></li>"""
    for devNm in sorted(devList):
        if devNm == curDev:
            continue
        if len(opts) > 0:
            opts += "\n            "
        row = assignedFilterTemplate.replace("$$NAME$$", devNm)
        opts += row.replace("$$URL$$", "bugs_" + devNm + ".html")
    return opts

def writeBugList(status, statusAlt, statusAltUrl, curDev, fileBrand):
    global bugList
    bugList = bugListTemplate.replace("$$BUGS$$", bugList)
    bugList = bugList.replace("$$PAGINATION$$", getPagination(fileBrand))
    bugList = bugList.replace("$$FILTER_STATUS$$", status)
    bugList = bugList.replace("$$FILTER_STATUS_ALT$$", statusAlt)
    bugList = bugList.replace("$$FILTER_STATUS_ALT_URL$$", statusAltUrl)
    bugList = bugList.replace("$$FILTER_ASSIGNED$$", curDev)
    bugList = bugList.replace("$$ASSIGNED_OPTIONS$$", getAssignedOpts(curDev))
    flExt = ".html"
    if numOutput / numPerPage > 1:
        flExt = str(numOutput / numPerPage) + flExt
    f = codecs.open("static_web/bugs" + fileBrand + flExt, "w+", "utf-8")
    f.write(bugList)
    f.close()
    bugList = ""

# the full listing
for ticket in ticketsOut:
    ticketHTML = bugEntryTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
    if len(bugList) > 0:
        bugList += "\n          "
    bugList += ticketHTML
    numOutput += 1
    if numOutput % numPerPage == 0:
        writeBugList("Any", "Open", "bugs_open.html", "Any", "")
if len(bugList) > 0:
    numOutput = numPerPage * numPages
    writeBugList("Any", "Open", "bugs_open.html", "Any", "")

# only open bugs
numPages = int(math.ceil(openCnt / 50.0))
numPerPage = int(math.ceil(openCnt / (numPages + 0.0)))
numOutput = 0
for ticket in ticketsOut:
    if ticket["$$STATUS$$"] != "Open":
        continue
    ticketHTML = bugEntryTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
    if len(bugList) > 0:
        bugList += "\n          "
    bugList += ticketHTML
    numOutput += 1
    if numOutput % numPerPage == 0:
        writeBugList("Open", "Any", "bugs.html", "Any", "_open")
if len(bugList) > 0:
    numOutput = numPerPage * numPages
    writeBugList("Open", "Any", "bugs.html", "Any", "_open")

# only bugs assigned to dev XXX
for devNm in devList:
    numPages = int(math.ceil(devList[devNm] / 50.0))
    numPerPage = int(math.ceil(devList[devNm] / (numPages + 0.0)))
    numOutput = 0
    for ticket in ticketsOut:
        if ticket["$$ASSIGNED$$"] != devNm:
            continue
        ticketHTML = bugEntryTemplate
        for key in ticket:
            if key.startswith("$$"):
                ticketHTML = ticketHTML.replace(key, ticket[key])
        if len(bugList) > 0:
            bugList += "\n          "
        bugList += ticketHTML
        numOutput += 1
        if numOutput % numPerPage == 0:
            writeBugList("Any", "Open", "bugs_open.html", devNm, "_" + devNm)
    if len(bugList) > 0:
        numOutput = numPerPage * numPages
        writeBugList("Any", "Open", "bugs_open.html", devNm, "_" + devNm)
