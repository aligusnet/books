from __future__ import unicode_literals
html = """
<html>
<body>
	<form method="get" action="search">
		<p>
			books: <input type="text" name="keywords">
		</p>
	</form>
	%s
</body>
</html>
"""

result = """
<h3>%(keywords)s, found %(ndocs)d books</h3>
<table>
%(rows)s
</table>
%(pagerefs)s
"""

entry = """
<tr><td>%(id)d.</td> <td><a href="description/%(id)d/"> %(author)s. <b>%(title)s</b></td></tr>
"""

pageref = " <a href=search?keywords=%(keywords)s&page=%(page)d>%(page)d</a> |"
page = " <big>%(page)d</big> |"

description = """
<html>
<body>
	<p>%(author)s</p>
	<p><b>%(title)s</b></p>
	<p>%(description)s</p>
	<p><a href='%(app_path)sbook/%(id)d/%(title)s.epub'>download book</p>
	%(image)s
</body>
</html>
"""

image = """
<img src=%(app_path)simage/%(id)d/%(cover)s />
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
