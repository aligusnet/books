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
<h3>%(keywords)s</h3>
<table>
%(rows)s
</table>
"""

entry = """
<tr><td>%(id)d.</td> <td><a href="description/%(id)d/"> %(author)s. <b>%(title)s</b></td></tr>
"""

description = """
<html>
<body>
	<p>%(author)s</p>
	<p><b>%(title)s</b></p>
	<p>%(description)s</p>
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
