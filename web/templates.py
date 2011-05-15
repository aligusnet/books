from __future__ import unicode_literals
html = """
<html>
<head>
<title>&Beta;&iota;&beta;&lambda;&iota;&alpha;</title>
<base href="%s" />
</head>
<body>
	<form method="get" action="search">
		<p>
			&Beta;&iota;&beta;&lambda;&iota;&alpha; <input type="text" name="keywords"/>
		</p>
	</form>
	%s
</body>
</html>
"""

result = """
<h3>%(keywords)s, found %(ndocs)d books</h3>
%(rows)s
%(pagerefs)s
"""

entry = """
<p><a href="description/%(id)d/"><b>%(title)s</b></a><br />
%(author)s.<br />
&rarr;&nbsp;<a href='book/%(id)d/%(title)s.epub'>download book</a><br />
</p>
"""

pageref = " <a href=search?keywords=%(keywords)s&page=%(page)d>%(page)d</a> |"
page = " <big>%(page)d</big> |"

description = """
<html>
<head>
<title>&Beta;&iota;&beta;&lambda;&iota;&omicron;: %(short_title)s</title>
<base href="%(app_url)s" />
<head>
<body>
	<p>%(author)s</p>
	<p><b>%(title)s</b></p>
	<p>%(description)s</p>
	<p><a href='book/%(id)d/%(title)s.epub'>download book</a></p>
	%(image)s
</body>
</html>
"""

image = """
<img src=image/%(id)d/%(cover)s />
"""

move = """
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="%s">here</a>.</p>
<hr>
</body></html>
"""
