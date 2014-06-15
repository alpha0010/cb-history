import xml.etree.ElementTree as ET
import datetime as DT
import cgi
import json
import codecs
import re
import math

bugTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bug $$NUMBER$$ - Code::Blocks History</title>

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


bugListTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bugs - Code::Blocks History</title>

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
            <li class="active"><a>Bugs</a></li>
            <li><a href="features.html">Features</a></li>
            <li><a href="patches.html">Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
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

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""

bugEntryTemplate = r"""<tr><td>$$NUMBER$$</td><td><a href="bugs/$$SHORT_NAME$$.html">$$SUMMARY$$</a></td><td>$$CATEGORY$$</td><td>$$PLATFORM$$</td><td>$$STATUS$$</td><td>$$OPEN_DATE$$</td><td>$$ASSIGNED$$</td><td>$$AUTHOR$$</td></tr>"""

urlRe = re.compile(ur'(((ht|f)tp(s?)\:\/\/)|(www\.))(([a-zA-Z0-9\-\._]+(\.[a-zA-Z0-9\-\._]+)+)|localhost)(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?([\d\w\.\/\%\+\-\=\&amp;\?\:\\\&quot;\'\,\|\~\;]*)')

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
docTree = ET.parse('bs_bugs_0.1.xml')

userIdDict = {}
for ticket in docTree.getroot():
    for prop in ticket:
        if prop.tag == "submitted_by":
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]
        elif prop.tag == "assigned_to" and prop.attrib["name"] != "none":
            userIdDict[ prop.attrib["id"] ] = prop.attrib["name"]

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
            ticketOut["$$SHORT_NAME$$"] = ticket.attrib["id"] + "-"
            for ch in prop.text:
                if len(ticketOut["$$SHORT_NAME$$"]) > 18:
                    ticketOut["$$SHORT_NAME$$"] = ticketOut["$$SHORT_NAME$$"].rstrip("_")
                    break
                if ch.isalnum():
                    ticketOut["$$SHORT_NAME$$"] += ch
                elif not ticketOut["$$SHORT_NAME$$"].endswith("_") and not ticketOut["$$SHORT_NAME$$"].endswith("-"):
                    ticketOut["$$SHORT_NAME$$"] += "_"

        elif prop.tag == "details":
            if len(prop.text) > 2000 or "===================================================================" in prop.text:
                lastIdx = 0
                para = ""
                for match in urlRe.finditer(prop.text):
                    para += cgi.escape(prop.text[lastIdx:match.start()])
                    para += '<a href="' + cgi.escape(match.group(0)) + '">' + cgi.escape(match.group(0)) + '</a>'
                    lastIdx = match.end()
                if ticketOut["$$NUMBER$$"] == "18988": # HACK
                    para += prop.text[lastIdx:]
                else:
                    para += cgi.escape(prop.text[lastIdx:])
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
                        lineTxt += cgi.escape(para[lastIdx:match.start()])
                        lineTxt += '<a href="' + cgi.escape(match.group(0)) + '">' + cgi.escape(match.group(0)) + '</a>'
                        lastIdx = match.end()
                    lineTxt += cgi.escape(para[lastIdx:])
                    ticketOut["$$DETAILS$$"] += "<p>" + lineTxt.strip() + "</p>"

        elif prop.tag == "date":
            ticketOut["$$OPEN_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")
            lastMod = max(lastMod, int(prop.text))

        elif prop.tag == "close_date":
            if int(prop.text) > 0:
                ticketOut["$$CLOSE_DATE$$"] = DT.datetime.utcfromtimestamp(int(prop.text)).isoformat(" ")
            else:
                ticketOut["$$CLOSE_DATE$$"] = "&nbsp;"

        elif prop.tag == "history" and prop[0].text == "details":
            if "HISTORY" not in ticketOut:
                ticketOut["HISTORY"] = []
            post = { "$$COMMENTS$$": "",
                     "$$AUTHOR$$": (cgi.escape(userIdDict[ prop[2].text ]) if prop[2].text in userIdDict else "ID_" + prop[2].text),
                     "$$TIME_STAMP$$": DT.datetime.utcfromtimestamp(int(prop[3].text)).isoformat(" ") }
            if len(prop[1].text) > 2000 or "===================================================================" in prop[1].text:
                lastIdx = 0
                para = ""
                for match in urlRe.finditer(prop[1].text):
                    para += cgi.escape(prop[1].text[lastIdx:match.start()])
                    para += '<a href="' + cgi.escape(match.group(0)) + '">' + cgi.escape(match.group(0)) + '</a>'
                    lastIdx = match.end()
                para += cgi.escape(prop[1].text[lastIdx:])
                post["$$COMMENTS$$"] = '<pre class="pre-scrollable">' + para + '</pre>'
            else:
                for para in prop[1].text.split("\n"):
                    if len(para) > 0 and not para.isspace():
                        if len(post["$$COMMENTS$$"]) > 0:
                            post["$$COMMENTS$$"] += "\n          "
                        lastIdx = 0
                        lineTxt = ""
                        for match in urlRe.finditer(para):
                            lineTxt += cgi.escape(para[lastIdx:match.start()])
                            lineTxt += '<a href="' + cgi.escape(match.group(0)) + '">' + cgi.escape(match.group(0)) + '</a>'
                            lastIdx = match.end()
                        lineTxt += cgi.escape(para[lastIdx:])
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

    if "HISTORY" not in ticketOut:
        ticketOut["$$HISTORY$$"] = ""
    ticketsOut.append(ticketOut)

    debugLimit -= 1
    #if debugLimit <= 0:
    #    break

for ticket in ticketsOut:
    ticketHTML = bugTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
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
    f = codecs.open("static_web/bugs/" + ticket["$$SHORT_NAME$$"] + ".html", "w+", "utf-8")
    f.write(ticketHTML)
    f.close()


ticketsOut = sorted(ticketsOut, key=lambda tk: -int(tk["$$NUMBER$$"]))
bugList = ""

numPages = int(math.ceil(len(ticketsOut) / 50.0))
numPerPage = int(math.ceil(len(ticketsOut) / (numPages + 0.0)))
numOutput = 0

def getPagination():
    pagination = "<li"
    if numOutput / numPerPage == 1:
        pagination += ' class="disabled"><span>&laquo;</span></li>'
    elif numOutput / numPerPage == 2:
        pagination += '><a href="bugs.html">&laquo;</a></li>'
    else:
        pagination += '><a href="bugs' + str(numOutput / numPerPage - 1) + '.html">&laquo;</a></li>'
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
            pagination += '<li><a href="bugs.html">1</a></li>'
        else:
            pagination += '<li><a href="bugs' + str(i) + '.html">' + str(i) + '</a></li>'
    if numOutput / numPerPage == numPages:
        pagination += '<li class="disabled"><span>&raquo;</span></li>'
    else:
        pagination += '<li><a href="bugs' + str(numOutput / numPerPage + 1) + '.html">&raquo;</a></li>'
    return pagination

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
        bugList = bugListTemplate.replace("$$BUGS$$", bugList)
        bugList = bugList.replace("$$PAGINATION$$", getPagination())
        flExt = ".html"
        if numOutput / numPerPage > 1:
            flExt = str(numOutput / numPerPage) + flExt
        f = codecs.open("static_web/bugs" + flExt, "w+", "utf-8")
        f.write(bugList)
        f.close()
        bugList = ""
if len(bugList) > 0:
    numOutput = numPerPage * numPages
    bugList = bugListTemplate.replace("$$BUGS$$", bugList)
    bugList = bugList.replace("$$PAGINATION$$", getPagination())
    flExt = ".html"
    if numOutput / numPerPage > 1:
        flExt = str(numOutput / numPerPage) + flExt
    f = open("static_web/bugs" + flExt, "w+")
    f.write(bugList)
    f.close()

