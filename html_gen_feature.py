#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as DT
import cgi
import json
import codecs
import re
import math


timeRe = re.compile(r'([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+):.*')

def fromisotime(timeStr):
    timeMatch = re.search(timeRe, timeStr)
    if timeMatch:
        return DT.datetime(int(timeMatch.group(1)), int(timeMatch.group(2)), int(timeMatch.group(3)), int(timeMatch.group(4)), int(timeMatch.group(5)))


featureTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Feature $$NUMBER$$ - Code::Blocks History</title>

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
            <li class="active"><a href="../features.html">Features</a></li>
            <li><a href="../patches.html">Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
      <div class="row">
        <div class="col-sm-8">
          <h3>Feature #$$NUMBER$$ <small>$$OPEN_DATE$$</small></h3>
          <h4>$$AUTHOR$$</h4>
          <p class="lead">$$SUMMARY$$</p>
          $$DETAILS$$
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


featureListTemplate = r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Features - Code::Blocks History</title>

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
            <li class="active"><a>Features</a></li>
            <li><a href="patches.html">Patches</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container" role="main">
      <table class="table table-hover table-condensed">
        <thead>
          <tr><th>Feature ID</th><th>Summary</th><th>Category</th><th>Status</th><th>Date</th><th>Assigned To</th><th>Submitted By</th></tr>
        </thead>
        <tbody>
          $$FEATURES$$
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

featureEntryTemplate = r"""<tr><td>$$NUMBER$$</td><td><a href="features/$$NUMBER$$.html">$$SUMMARY$$</a></td><td>$$CATEGORY$$</td><td>$$STATUS$$</td><td>$$OPEN_DATE$$</td><td>$$ASSIGNED$$</td><td>$$AUTHOR$$</td></tr>"""

urlRe = re.compile(ur'(((ht|f)tp(s?)\:\/\/)|(www\.))(([a-zA-Z0-9\-\._]+(\.[a-zA-Z0-9\-\._]+)+)|localhost)(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?([\d\w\.\/\%\+\-\=\&amp;\?\:\\\&quot;\'\,\|\~\;]*)')

bugRe     = re.compile(ur'bug_id=([0-9]+)')
featureRe = re.compile(ur'feature_id=([0-9]+)')
patchRe   = re.compile(ur'patch_id=([0-9]+)')

linkTipDict = {}
for line in open("linkTips.txt"):
    parts = line.strip().split(" ", 1)
    linkTipDict[parts[0]] = parts[1]

def getMappedUrl(url):
    if "group_id=5358" in url:
        urlMatch = re.search(bugRe, url)
        if urlMatch:
            return ["../bugs/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(featureRe, url)
        if urlMatch:
            return [urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
        urlMatch = re.search(patchRe, url)
        if urlMatch:
            return ["../patches/" + urlMatch.group(1) + ".html", linkTipDict[urlMatch.group(0)]]
    return [url, ""]

def makeLink(url):
    urlDat = getMappedUrl(url)
    if urlDat[1] == "":
        return '<a href="' + urlDat[0] + '">' + url + '</a>'
    else:
        return '<a href="' + urlDat[0] + '" data-toggle="tooltip" title="' + urlDat[1] + '">' + url + '</a>'

fHandle = open("old_dump/berlios.json", "r")
lookupDb = json.load(fHandle)
fHandle.close()

# some known values from my 30-4-2014 web scrape
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5709,
    "summary": "Saving order of tabs in 'Management'",
    "assigned_to": "None",
    "category": "Interface",
    "status": "Open",
    "comments": [ {"date": "2013-11-25T17:00:00Z", "submitter": {"nick": "szmitek"}, "comment": "Date: 2013-Nov-25 17:00\nSender: szmitek\nLogged In: YES \nuser_id=63601\nBrowser: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0\n\nI think Code::Blocks should save the sequence of tabs\nin a panel \'Management\'. Currently, when you move the\ntab \'Symbols\' before the tab \'Projects\' and the tab\n\'Files\' after the tab \'Resource\' and restart the\nprogram, tabs are distributed in the order as before:\n\'Projects \', \'Symbols \', \'Files\', \'Resources\'\n(Code::Blocks 12.11 in MS Windows 8.1). In my opinion,\nthe possibility of permanent displacement of most used\ntabs, so that they are next to each other, would be\nuseful. Tabs \'Projects\' and \'Resources\' are more needed\nthan tabs \'Symbols\' and \'Files\' when modifying the\ninterface of application using wxWidgets library. After\ndisplacement of the tabs, you can narrow the panel\nhiding less frequently used tabs.\n\nAlternatively, the tabs of the panel \'Management\' would\nbe distributed vertically (preferably with the ability\nto auto-hide) like in NetBeans and MS Visual Studio.\n\nThis feature may fit better as a bug."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5714,
    "summary": "Common keyboard shortcuts on watch edit",
    "assigned_to": "tpetrov",
    "category": "Debugging",
    "status": "Open",
    "comments": [ {"date": "2013-12-18T06:11:00Z", "submitter": {"nick": "zeroth"}, "comment": "Date: 2013-Dec-18 06:11\nSender: zeroth\nLogged In: YES \nuser_id=62982\nBrowser: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0\n\nIn short, trying to \"select all\" via the CTRL+A key\ncombo while a watch text area has keyboard focus,\ninstead the main edit window gets everything selected.\nSame thing for CTRL+V to paste, etc.\n\nI\'ve been using CodeBlocks for several years now, and\nthis is still something that really bothers me. When\ndebugging, and adding a manual watch (such as to\ndereference a pointer of a specified type and a\nspecified memory address), common keyboard shortcuts do\nnot work - rather, they do, but they affect the main\nedit window (the source code). It\'s maddening..."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5716,
    "summary": "Open files list per project and target",
    "assigned_to": "None",
    "category": "Plugins",
    "status": "Open",
    "comments": [ {"date": "2013-12-23T12:53:00Z", "submitter": {"nick": "eranon"}, "comment": "Date: 2013-Dec-23 12:53\nSender: eranon\nLogged In: YES \nuser_id=62833\nBrowser: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko\n\nAccording to the forum thread at \nhttp://forums.codeblocks.org/index.php/topic,18700.0.html, does someone could write a plugin (if not \ndirectly implementable in C::B) to keep track of \nopened files per project or target, this being optionnal \nand configurable through check or radio boxes.\n\nThis would be useful to, at least, three users (me, \nscarphin and cacb ; even if he wants more:)."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5718,
    "summary": "Help plugin enhancement",
    "assigned_to": "tpetrov",
    "category": "Plugins",
    "status": "Open",
    "comments": [ {"date": "2014-01-07T09:34:00Z", "submitter": {"nick": "gd_on"}, "comment": "Date: 2014-Jan-07 09:34\nSender: gd_on\nLogged In: YES \nuser_id=34606\nBrowser: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0\n\nWhen you use the help plugin on a man page, you can\nobtain a very long displayed result : as for example a\nhelp on gcc or gfortran.\nIf you want to look at a particular option it\'s quite\nhard to find it, and more, to find it\'s development\nbecause it may be very far.\nexample : in gcc try to find the option -mthreads and\nit\'s developpement or explanation.\nIt could be nice to add in this plugin a search\nfunction to find particular words in the displayed window.\nThanks"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5719,
    "summary": "More than one Memory View",
    "assigned_to": "None",
    "category": "Debugging",
    "status": "Open",
    "comments": [ {"date": "2014-01-14T15:25:00Z", "submitter": {"nick": "joedm"}, "comment": "Date: 2014-Jan-14 15:25\nSender: joedm\nLogged In: YES \nuser_id=54142\nBrowser: Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nI often need watch more than one memory location at \nthe same time during debugging. Is this possible to \nadd a possibility to open more than one Memory View?  \nWith only one Memory View I have to change memory \nlocations on every step which is time consuming and \nunconvenient.\nIf such a possibility exists, please let me know.\nThank you!"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5720,
    "summary": "Support for Objective-C on Mac",
    "assigned_to": "None",
    "category": "Programming Languages",
    "status": "Open",
    "comments": [ {"date": "2014-01-23T18:27:00Z", "submitter": {"nick": "jimp"}, "comment": u"Date: 2014-Jan-23 18:27\nSender: jimp\nLogged In: YES \nuser_id=24948\nBrowser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\n\nSupport for Objective-C on Mac\n\nI have recently set up CodeBlocks 13.12 on Mac to work\nwith Objective-C source. No program changes were\nnecessary. With a few changes it could be done\nautomatically. Without Objective-C there is limited\ncapability on the Mac. \n\nObjective-C can also be used on Windows or Linux with\nthe addition of the GNUstep package. But it only works\nwith compilers that support Objective-C. The ones I\nknow of outside of Mac are MinGW and GCC. And the\nObjective-C compiler package must be installed on\nthese. I don\u2019t know how useful it would be outside of Mac.\n\nThe following describes the changes that were necessary\nto set up Objective-C on Mac. The LLVM Clang compiler\nwas used. I assume it would work the same with GCC.\n\nAfter creating a project containing Objective-C source\ncode, I tried to open an Objective-C file in\nCodeBlocks. It didn’t recognize the file extension of\n“.m”. I selected “Open it inside the CodeBlocks\neditor”. Then right clicked on the Objective-C file\nname and selected “Properties”. Check the “Compile\nfile” and “Link file” options. This is all that was\nneeded to compile and run the program.\n\nThe syntax highlighting needs to be changed also.\nObjective-C has an “.m” extension which is currently\nassigned to Matlib. It must be removed from Matlib and\nadded to Objective-C. Then the syntax highlighting\nseemed to be the same as C/C++ without any changes.\n\nThis is all that was necessary to use Objective-C on\nthe Mac.\n\nThere seems to be quite a few people who don\u2019t like\nXcode. It would be good to have a cross-platform IDE\nlike CodeBlocks that could be used with Objective-C on\nthe Mac. And it looks like the changes would not be\nextensive."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5728,
    "summary": "Ease of adding new line",
    "assigned_to": "None",
    "category": "Editing",
    "status": "Open",
    "comments": [ {"date": "2014-02-16T03:02:00Z", "submitter": {"nick": "mr5"}, "comment": "Date: 2014-Feb-16 03:02\nSender: mr5\nLogged In: YES \nuser_id=65251\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0\n\nHello and Good day!\n\nI would like to know first if there\'s an existing\nfeature as \"adding-hotkey-then-perform-certain-operation\" ?\n\nCertain operation would be, of-course, user-defined,\nlike adding characters/strings/ into the text-editor by\npressing keys or hovering into a certain variable\nduring debugging then do some work.\n\nFor example, I would like to have a CTRL + ENTER w/c\nwill enter a new line above the current line where the\ncursor lies.\n\nThanks and regards!"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5729,
    "summary": "Support for retina macs",
    "assigned_to": "None",
    "category": "Interface",
    "status": "Open",
    "comments": [ {"date": "2014-02-21T06:57:00Z", "submitter": {"nick": "wolearyc"}, "comment": "Date: 2014-Feb-21 06:57\nSender: wolearyc\nLogged In: YES \nuser_id=65272\nBrowser: Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1\n(KHTML, like Gecko) CriOS/33.0.1750.14 Mobile/11B554a Safari/9537.53\n\nOn a retina mac, the entire window is blurry. Blurry icons are workable, \nbut the blurry text is very difficult to read! I believe wxwidgets supports \nretina displays.\n\nThanks!"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5730,
    "summary": "Add Ctrl+C key for copy from log windows",
    "assigned_to": "None",
    "category": "Interface",
    "status": "Open",
    "comments": [ {"date": "2014-02-24T19:36:00Z", "submitter": {"nick": "davidallen"}, "comment": "Date: 2014-Feb-24 19:36\nSender: davidallen\nLogged In: YES \nuser_id=64756\nBrowser: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nAdd support for Ctrl+C keystroke to copy selected text within log windows \n(Build Log, Debugger, etc...)\n\nIt is possible to copy using the options in the context menu, however it is \nusually expected to also be able to use the CTRL+C key combination to \ncopy to clipboard.\n\nAdmittedly this is a very minor issue, but would help to make the UI more \npolished."},
                  {"date": "2014-02-24T20:18:00Z", "submitter": {"nick": "davidallen"}, "comment": "Date: 2014-Feb-24 20:18\nSender: davidallen\nLogged In: YES \nuser_id=64756\nBrowser: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nPatch # 003554 submitted :\n\nFix for the infopane.cpp - added a KeyUp event handler and if CTRL+C then call \nthe OnCopy."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5731,
    "summary": "Find Files in search path",
    "assigned_to": "None",
    "category": "Editing",
    "status": "Open",
    "comments": [ {"date": "2014-02-24T20:27:00Z", "submitter": {"nick": "davidallen"}, "comment": "Date: 2014-Feb-24 20:27\nSender: davidallen\nLogged In: YES \nuser_id=64756\nBrowser: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nThe FindReplace dialog has a textbox for the search path.  It is a minor \nsnag but it would be nice if it was a combobox so can support multiple \nsearch paths, and remembers your previous entries.\n\nI have a few search paths I like to use to help narrow the search and \nspeed it up, so would be helpful to not have to keep re-entering them.\n\nMany IDEs (e.g. Netbeans) will have a combobox instead of textbox.\n\nSuggested Code Changes\n\n1) Change the search path textbox (\"txtSearchPath\") to a combobox \n(\"cmbSearchPath\").\n\n2) Store the search masks in the ConfigManager under key \n\"search_path\" (which is now a string array).\n\n3) Added migration for old config setting (\"search_path\") to new key \n\"search_paths\"."},
                  {"date": "2014-02-24T20:32:00Z", "submitter": {"nick": "davidallen"}, "comment": "Date: 2014-Feb-24 20:32\nSender: davidallen\nLogged In: YES \nuser_id=64756\nBrowser: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nNote: I raised a similar request # 005693 related to the search masks....  I will try and create a similar fix for this new request #005731"},
                  {"date": "2014-02-25T20:59:00Z", "submitter": {"nick": "davidallen"}, "comment": "Date: 2014-Feb-25 20:59\nSender: davidallen\nLogged In: YES \nuser_id=64756\nBrowser: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/31.0.1650.63 Safari/537.36\n\nPatch # 0003555 submitted to address this feature request.\n\nThanks,\nDavid"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5733,
    "summary": "Projects Management - Folder Option",
    "assigned_to": "None",
    "category": "Interface",
    "status": "Open",
    "comments": [ {"date": "2014-03-04T04:41:00Z", "submitter": {"nick": "johnconner"}, "comment": "Date: 2014-Mar-04 04:41\nSender: johnconner\nLogged In: YES \nuser_id=65317\nBrowser: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/33.0.1750.117 Safari/537.36\n\nI just thought I would make a request, I had been \nusing visual studio 2013 to write my C programs, and \nif y\'all added this feature I imagine it would make \nbeginner C programmer\'s lives a lot easier. Visual \nStudio gives the option for the user to add a folder \nwithin their work-space where they can then put \nprojects inside of, this makes it easier and more user-\nfriendly for beginners like me who are working their \nway through 800+ page books with tons of exercises. \nNormally what I do is I create a folder and label it \nChapter_7 and I then create the projects inside of \nthat folder and add the main.c files under those \nprojects. This allows me to jump back and forth to \nolder exercises from chapter\'s I have already covered \nin case I find myself having trouble remembering how \nto write a specific code out properly. If you would add \nthat feature I would really appreciate it."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5734,
    "summary": "Code completion: constructor parameters",
    "assigned_to": "None",
    "category": "Plugins",
    "status": "Open",
    "comments": [ {"date": "2014-03-05T09:12:00Z", "submitter": {"nick": "carra"}, "comment": "Date: 2014-Mar-05 09:12\nSender: carra\nLogged In: YES \nuser_id=65322\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0\n\nCode::Blocks should provide autocompletion of a\nconstructor\'s parameters within its initialization\nlist. For instance, take this code:\n\n    ListCell::ListCell( P_Object First_, P_Object Rest_ )\n\n    // - - - - - - - - - - - - - - - - - -\n\n    :   First( First_ )  // <-- cursor HERE\n\n    ,   Rest( Rest_ )\n\n    // - - - - - - - - - - - - - - - - - -\n\n    {\n\n        // (do nothing)\n\n    }\n\nWhen the cursor is inside the braces, CC correctly\nhandles First_ and Rest_. But if the cursor is on the\nline with the arrow, I am offered completion for First\n(i.e. the class attribute), but not for First_."},
                  {"date": "2014-04-02T16:54:00Z", "submitter": {"nick": "ollydbg"}, "comment": "Date: 2014-Apr-02 16:54\nSender: ollydbg\nLogged In: YES \nuser_id=50205\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:28.0) Gecko/20100101 Firefox/28.0\n\nIndeed, this is a feature request. Thanks."} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5742,
    "summary": "Search and replace",
    "assigned_to": "None",
    "category": "Editing",
    "status": "Open",
    "comments": [ {"date": "2014-03-30T08:58:00Z", "submitter": {"nick": "ojhew"}, "comment": "Date: 2014-Mar-30 08:58\nSender: ojhew\nLogged In: YES \nuser_id=65424\nBrowser: Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0\n\nSometimes you want to change a variable name that you\nhave been using. Currently you can search for test in\nthe a file but it would be nice if you could find and\nreplace all instances with a single query. \n\nIf this function is already available please let me\nknow where to find it..thx"},
                  {"date": "2014-04-02T16:51:00Z", "submitter": {"nick": "ollydbg"}, "comment": "Date: 2014-Apr-02 16:51\nSender: ollydbg\nLogged In: YES \nuser_id=50205\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:28.0) Gecko/20100101 Firefox/28.0\n\nCTRL + R is your solution, right?"} ],
    "history": []
})
lookupDb["trackers"]["feature"]["artifacts"].append({
    "id": 5743,
    "summary": "dependencies",
    "assigned_to": "None",
    "category": "Programming Languages",
    "status": "Open",
    "comments": [ {"date": "2014-04-01T00:47:00Z", "submitter": {"nick": "tele"}, "comment": "Date: 2014-Apr-01 00:47\nSender: tele\nLogged In: YES \nuser_id=65430\nBrowser: Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0\n\n\n1 . I Just learning to program only, but\nwhen I using in Linux \n\nexample :\n\n#include \"mainwindow.h\"\n\n#include <gtkmm/application.h>\n\nI need add paths  this libs in \nSettings -> Search directories ( tab )->  Compiler (tab)\n\nexample in :\n\n/usr/include/atk-1.0/atk\n/usr/include/gdk-pixbuf-2.0/gdk-pixbuf\n/usr/lib64/gtk-2.0/include\n/usr/include/glib-2.0\n/usr/include/gtk-2.0\n\nThis is boring, example when I trying run code from\ntutorials.\n\n\nAll headers are in /usr  folder\ngoogle is not good tool to find this derectory, because \npaths are diffrend\nso I use for example \nmate-search-tool to find this libs\n\n- Tool to find libs in /usr or from other dir will be\ngood for code blocks\n\n2. when I use some well-known \n(when command found in lib ,  lib is is known )\n  or frequently used commands\nit should me propose for example:\n\n#include \"mainwindow.h\"\n\n#include <gtkmm/application.h>"},
                  {"date": "2014-04-02T16:49:00Z", "submitter": {"nick": "ollydbg"}, "comment": "Date: 2014-Apr-02 16:49\nSender: ollydbg\nLogged In: YES \nuser_id=50205\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:28.0) Gecko/20100101 Firefox/28.0\n\nI don\'t know what does this feature request titled\n\"dependencies\" means, can you explain? Also, I don\'t know\nwhat you two sections means? You need to explain what is the\nexpect behavior C::B should do.\nThanks."},
                  {"date": "2014-04-04T11:23:00Z", "submitter": {"nick": "tele"}, "comment": "Date: 2014-Apr-04 11:23\nSender: tele\nLogged In: YES \nuser_id=65430\nBrowser: Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0\n\n\" dependencies \"  are libs for project\n\n#include \"mainwindow.h\"\n\n#include <gtkmm/application.h>\n\nto compile project I need add paths this libs in\nSettings-> Compiler->Search directories->Linker\n\nI found other way,\nI added from website new code lite for fedora.\nI found plugin inside \" Library finder \"\nProbably this plugin [ SOLVED ]  my problem.\n\nThanks ,  please moderator add [Solved] to this topic :)"} ],
    "history": []
})

# find the index
#for index, ticket in enumerate(lookupDb["trackers"]["feature"]["artifacts"]):
#    if ticket["id"] == 5639:
#        print index
#        break

# tweak the split url; TODO: fix the un-splitter algorithm (instead of this hack)
lookupDb["trackers"]["feature"]["artifacts"][25]["comments"][1]["comment"] = "Logged In: YES \nuser_id=59186\r\nBrowser: Mozilla/5.0 (Windows NT 5.1; rv:19.0) Gecko/20100101 Firefox/19.0\n\nSorry for the mess, I have uploaded the patch here:\nhttps://developer.berlios.de/patch/index.php?func=detailpatch&patch_id=3449&group_id=5358"


ticketsOut = []

debugLimit = 5 # limit ticket conversion for debugging

for ticket in lookupDb["trackers"]["feature"]["artifacts"]:
    ticketOut = { "$$NUMBER$$": str(ticket["id"]),
                  "$$SUMMARY$$": cgi.escape(ticket["summary"]),
                  "$$ASSIGNED$$": cgi.escape(ticket["assigned_to"]),
                  "$$CATEGORY$$": cgi.escape(ticket["category"]),
                  "$$STATUS$$": cgi.escape(ticket["status"]) }
    if ticketOut["$$ASSIGNED$$"] == "None":
        ticketOut["$$ASSIGNED$$"] = "&nbsp;"
    if ticketOut["$$CATEGORY$$"] == "None":
        ticketOut["$$CATEGORY$$"] = "&nbsp;"
    comments = sorted(ticket["comments"], key=lambda cm: fromisotime(cm["date"]))
    for comment in comments:
        text = comment["comment"]
        idx = text.find("\n\n")
        if idx != -1:
            text = text[idx + 2:]
        lastIdx = 0
        textProc = ""
        for match in urlRe.finditer(text):
            textProc += cgi.escape(text[lastIdx:match.start()])
            url = cgi.escape(match.group(0))
            if url.endswith(".") or url.endswith(","):
                textProc += makeLink(url[:-1]) + url[-1:]
            else:
                textProc += makeLink(url)
            lastIdx = match.end()
        textProc += cgi.escape(text[lastIdx:])
        if len(text) > 2000:
            textProc = '<pre class="pre-scrollable">' + textProc + '</pre>'
        else:
            textProc = textProc.replace("\n\n", "\r")
            textProc = textProc.replace("\n", " ")
            paraComb = ""
            for para in textProc.split("\r"):
                if len(para) > 0 and not para.isspace():
                    if len(paraComb) > 0:
                        paraComb += "\n          "
                    paraComb += "<p>" + para.strip() + "</p>"
            textProc = paraComb
        if "$$DETAILS$$" in ticketOut:
            if "HISTORY" not in ticketOut:
                ticketOut["HISTORY"] = []
            post = { "$$COMMENTS$$": textProc,
                     "$$AUTHOR$$": cgi.escape(comment["submitter"]["nick"]),
                     "$$TIME_STAMP$$": fromisotime(comment["date"]).isoformat(" ") }
            ticketOut["HISTORY"].append(post)
        else:
            ticketOut["$$DETAILS$$"] = textProc
            ticketOut["$$AUTHOR$$"] = cgi.escape(comment["submitter"]["nick"])
            ticketOut["$$OPEN_DATE$$"] = fromisotime(comment["date"]).isoformat(" ")
    for change in ticket["history"]:
        if change["field"] == "status" and change["new"] != "Open":
            ticketOut["$$CLOSE_DATE$$"] = fromisotime(change["date"]).isoformat(" ")

    if "HISTORY" not in ticketOut:
        ticketOut["$$HISTORY$$"] = ""
    if "$$CLOSE_DATE$$" not in ticketOut:
        ticketOut["$$CLOSE_DATE$$"] = "&nbsp;"
    ticketsOut.append(ticketOut)

    debugLimit -= 1
#    if debugLimit <= 0:
#        break

for ticket in ticketsOut:
    ticketHTML = featureTemplate
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
    if "data-toggle=\"tooltip\"" in ticketHTML:
        ticketHTML = ticketHTML.replace("$$SCRIPT$$", """
    <script>
      $(document).ready(function() {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });
      });
    </script>""")
    else:
        ticketHTML = ticketHTML.replace("$$SCRIPT$$", "")
    f = codecs.open("static_web/features/" + ticket["$$NUMBER$$"] + ".html", "w+", "utf-8")
    f.write(ticketHTML)
    f.close()


ticketsOut = sorted(ticketsOut, key=lambda tk: -int(tk["$$NUMBER$$"]))
featureList = ""

numPages = int(math.ceil(len(ticketsOut) / 50.0))
numPerPage = int(math.ceil(len(ticketsOut) / (numPages + 0.0)))
numOutput = 0

def getPagination():
    pagination = "<li"
    if numOutput / numPerPage == 1:
        pagination += ' class="disabled"><span>&laquo;</span></li>'
    elif numOutput / numPerPage == 2:
        pagination += '><a href="features.html">&laquo;</a></li>'
    else:
        pagination += '><a href="features' + str(numOutput / numPerPage - 1) + '.html">&laquo;</a></li>'
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
            pagination += '<li><a href="features.html">1</a></li>'
        else:
            pagination += '<li><a href="features' + str(i) + '.html">' + str(i) + '</a></li>'
    if numOutput / numPerPage == numPages:
        pagination += '<li class="disabled"><span>&raquo;</span></li>'
    else:
        pagination += '<li><a href="features' + str(numOutput / numPerPage + 1) + '.html">&raquo;</a></li>'
    return pagination

for ticket in ticketsOut:
    ticketHTML = featureEntryTemplate
    for key in ticket:
        if key.startswith("$$"):
            ticketHTML = ticketHTML.replace(key, ticket[key])
    if len(featureList) > 0:
        featureList += "\n          "
    featureList += ticketHTML
    numOutput += 1
    if numOutput % numPerPage == 0:
        featureList = featureListTemplate.replace("$$FEATURES$$", featureList)
        featureList = featureList.replace("$$PAGINATION$$", getPagination())
        flExt = ".html"
        if numOutput / numPerPage > 1:
            flExt = str(numOutput / numPerPage) + flExt
        f = codecs.open("static_web/features" + flExt, "w+", "utf-8")
        f.write(featureList)
        f.close()
        featureList = ""
if len(featureList) > 0:
    numOutput = numPerPage * numPages
    featureList = featureListTemplate.replace("$$FEATURES$$", featureList)
    featureList = featureList.replace("$$PAGINATION$$", getPagination())
    flExt = ".html"
    if numOutput / numPerPage > 1:
        flExt = str(numOutput / numPerPage) + flExt
    f = open("static_web/features" + flExt, "w+")
    f.write(featureList)
    f.close()
