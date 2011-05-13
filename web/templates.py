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
<tr><td>%(id)d.</td> <td><a href="description?id=%(id)d"> %(author)s. <b>%(title)s</b></td></tr>
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
<img src=image?id=%(id)d />
"""
