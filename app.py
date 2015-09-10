import subprocess
import tempfile
import json
import os.path

from flask import Flask, request
app = Flask(__name__)

INDEX = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Index</title>
</head>
<body>
<h1>Index</h1>
<ul>
<li><a href="static/final.pdf">final.pdf</a></li>
<li><a href="static/draft.pdf">draft.pdf</a></li>
</ul>
</body>
</html>
"""

STATIC = "/home/pierre/mffapp/static"

@app.route("/")
def hello():
    return INDEX

@app.route("/build")
def build():
    dir = tempfile.mkdtemp()
    out = subprocess.check_output(['pwd'], cwd=dir, stderr=subprocess.STDOUT)
    # git clone
    # make -B final
    # make -B draft
    # cp final.pdf draft.pdf static path
    out2 = subprocess.check_output(['rm', '-rf', dir], stderr=subprocess.STDOUT)
    return out

@app.route("/github", methods=["POST"])
def github():
    data = json.loads(request.data.decode('utf-8'))
    git_url = data['repository']['html_url']
    dir = tempfile.mkdtemp()
    repo = os.path.join(dir, 'fet-open-promane-2015')
    out = subprocess.check_output(['git', 'clone', git_url], cwd=dir)
    out2 = subprocess.check_output(['make', '-B', 'final', 'draft'], cwd=repo)
    out3 = subprocess.check_output(['mv', os.path.join(repo, 'final.pdf'), os.path.join(repo, 'draft.pdf'), STATIC ], stderr=subprocess.STDOUT)
    out4 = subprocess.check_output(['rm', '-rf', dir], stderr=subprocess.STDOUT)
    return ''

if __name__ == "__main__":
    app.run()

