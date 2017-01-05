#!/usr/bin/python3

import argparse
import sys
import os
import subprocess
import pip

class FileContent(object):
    def __init__(self):
        self.app = (
            '#!/usr/bin/python\n'
            'from flask import Flask, render_template\n'
            '\n'
            'app = Flask(__name__)\n'
            '\n'
            '@app.route("/")\n'
            '\n'
            'def home():\n'
               '    return render_template("index.html", title="Home")'
        )
        self.run = (
            '#!/usr/bin/python -B\n'
            '# -*- coding: utf-8 -*-\n'
            '#\n'
            '#  run.py\n'
            '#\n'
            '#  Redistribution and use in source and binary forms, with or without\n'
            '#  modification, are permitted provided that the following conditions are\n'
            '#  met:\n'
            '#\n'
            '#  * Redistributions of source code must retain the above copyright\n'
            '#    notice, this list of conditions and the following disclaimer.\n'
            '#  * Redistributions in binary form must reproduce the above\n'
            '#    copyright notice, this list of conditions and the following disclaimer\n'
            '#    in the documentation and/or other materials provided with the\n'
            '#    distribution.\n'
            '#  * Neither the name of the  nor the names of its\n'
            '#    contributors may be used to endorse or promote products derived from\n'
            '#    this software without specific prior written permission.\n'
            '#\n'
            '#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n'
            '#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n'
            '#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\n'
            '#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT\n'
            '#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\n'
            '#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\n'
            '#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\n'
            '#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY\n'
            '#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n'
            '#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n'
            '#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
            'import argparse\n'
            'import os\n'
            '\n'
            'def main():\n'
            '    parser = argparse.ArgumentParser(description=\'OCT\', conflict_handler=\'resolve\')\n'
            '    parser.add_argument(\'-v\', \'--version\', action=\'version\', version=parser.prog + \' Version: 1.0\')\n'
            '    subparsers = parser.add_subparsers(dest=\'action\', help=\'action\')\n'
            '\n'
            '    parser_serve = subparsers.add_parser(\'serve\', help=\'start a development server\')\n'
            '    parser_serve.add_argument(\'-a\', \'--address\', dest=\'address\', default=None, help=\'the address to bind to\')\n'
            '    parser_serve.add_argument(\'-p\', \'--port\', dest=\'port\', default=5000, type=int, help=\'the port to bind to\')\n'
            '\n'
            '    arguments = parser.parse_args()\n'
            '    ## Important! Make sure you\'re importing the right application!\n'
            '    import app\n'
            '    if arguments.action == \'serve\':\n'
            '        if os.environ.get(\'DISPLAY\'):\n'
            '            if not \'X-RUN-CHILD\' in os.environ:\n'
            '                os.system("gvfs-open http://{0}:{1}/".format(arguments.address or \'localhost\', arguments.port))\n'
            '                os.environ[\'X-RUN-CHILD\'] = \'X\'\n'
            '        app.app.run(host=arguments.address, port=arguments.port, debug=True)\n'
            '    return 0\n'
            '\n'
            'if __name__ == \'__main__\':\n'
            '    main()\n'
        )
        self.template = (
            '<!DOCTYPE html>\n'
            '<html>\n'
            '    <head>\n'
            '       <title>{{title}}</title>\n'
            '       <meta name="viewport" content="width=device-width, initial-scal=1.0">\n'
            '       <link href="../static/styles/style.css" rel="stylesheet">\n'
            '    </head>\n'
            '    <body>\n'
            '       <div class="container">\n'
            '          <div class="header">\n'
            '          <ul class="navbar">\n'
            '             <a href="./index.html">home</a> / \n'
            '             <a href="./about.html">about</a>\n'
            '          </ul>\n'
            '       </div>\n'
            '       <div class="content">\n'
            '        {% block content  %}{% endblock  %}\n'
            '           </div>\n'
            '           <div class="clear"></div>\n'
            '           <div class="footer">\n'
            '          <span>Connect:</span>\n'
            '              <a href="http://twitter.com" target="_blank"><img src="http://www.budget.com/budgetWeb/images/common/twitter1.png" style="width:25px" /></a> / \n'
            '              <a href="http://facebookcom" target="_blank"><img src="https://www.budget.com/budgetWeb/images/common/facebook1.png" style="width:25px" /></a> /\n'
            '              <a href="http://linkedin.com" target="_blank"><img src="https://cdn3.iconfinder.com/data/icons/free-social-icons/67/linkedin_circle_color-512.png" style="width:25px" /></a> /\n'
		    '      			</div>'
            '       </div>\n'
            '    <body>\n'
        )
        self.index = (
            '{% extends "template.html" %}\n'
            '{% block content %}\n'
            '\n'
            '<h3>This is my index page!!!</h3>\n'
            '<p>Blah blah blibity blah</p>\n'
            '\n'
            '{% endblock %}\n'
        )
        self.styles = (
            '.container { position:relative; width:900px; margin:0 auto; background:#FFF; box-shadow:3px 3px 3px; }\n'
            '.content { margin:0px auto; }\n'
            '.header{ height:178px; margin:0 0 0 -5px; padding:5px; text-align:center; width:900px; background:url(\'https://www.hdwallpapers.net/images/batman-artwork-wallpaper-for-twitter-header-49-621.jpg\') center; background-size: cover;  }\n'
            '.footer {width:900px; background:#000; color:#CCC; margin:10px auto; box-shadow:3px 3px 3px #000; text-align:left; }\n'
            '.footer img { width:25px; height:25px;}\n'
            '.navbar { margin:160px auto; list-style-type:none; padding:5px; text-align:center; background:#777; color:#FFF; text-transform:uppercase; }\n'
            '.navbar li { display:inline; margin:5px; }\n'
            '.navbar a { color:#FFF; text-decoration:none; font-weight:bold; }\n'
            '.navbar a:hover { color:#000; text-decoration:underline; }\n'
            '.clear {clear:both;}%                   \n'
        )
    def __return__(self):
        if file_name == 'app':
        	return self.app
        elif file_name == 'run':
        	return self.run
        elif file_name == 'template':
        	return self.template
        elif file_name == 'index':
        	return self.index
        else:
        	return self.styles

def main():
    #check if flask and jinja packages are installed
    try:
        import flask
        print ("[+] Flask version " + flask.__version__ + " is installed." )
    except ImportError:
        print ("[-] Flask not installed, Run 'python3 -m pip install flask.")
        return 0
    try:
        import jinja2
        print ("[+] Jinja2 version " + jinja2.__version__ + " is installed.")
    except ImportError:
        print ("[-] Jinja2 isn't installed. Run 'python3 -m pip install jinja2'.")
        return 0

    # Set up arguments
    parser = argparse.ArgumentParser(description='Put description here')
    parser.add_argument('-d', '--directory', default='$HOME', help='home directory to build jinja site' )
    parser.add_argument('-n', '--name', help='name of the jinja site')
    parser.add_argument('-v', '--verbose', help='show verbose output', action='store_true')
    # add additional arguments here

    # Parse arguments
    args = parser.parse_args()
    home_dir = args.directory
    site_name = args.name

    # Define directories
    site_directory = home_dir + '/' + site_name
    template_directory = site_directory +'/templates'
    static_directory = site_directory +'/static'
    images_directory = static_directory + '/images'
    styles_directory = static_directory + '/styles'
    scripts_directory = static_directory + '/scripts'
    folder = [ site_directory, template_directory, static_directory, images_directory, styles_directory, scripts_directory ]
    
    #Define Files
    app_file = site_directory + '/app.py'
    run_file = site_directory + '/run.py'
    template_file = template_directory + '/template.html'
    index_file = template_directory + '/index.html'
    styles_file = styles_directory +'/styles.css'
    files = [ app_file, run_file, template_file, index_file, styles_file ]


    #Do Stuff
    make_dirs(folder, site_name)
    build_files(files)

def make_dirs (folder, site_name):
    username = os.getlogin()

    #used to make the necessary folders for the directory
    for i, val in enumerate(folder):
        subprocess.check_output([ 'mkdir', '-p', val ])
    print("[+] Directories Made")
    
    #changing permissions as necessary
    subprocess.check_output([ 'chown', '-R', username , site_name ])
    subprocess.check_output([ 'chmod', '-R', "755", site_name])
    print("[+] Appropriate permissions set")

def build_files(files):
    # Iterate through the files variable to create and populate files using 
    # the FileContent class
    for i, val in enumerate(files):
        writepath = val
        file = writepath.rsplit('/', 1)[1]
        content = FileContent()
        with open (writepath, 'w') as f:
            if file == 'app.py':
                f.write(content.app)
            elif file == 'run.py':
                f.write(content.run)
            elif file == 'template.html':
            	f.write(content.template)
            elif file == "index.html":
            	f.write(content.index)
            else:
            	f.write(content.styles)
            pass
        subprocess.check_output([ 'chmod', '-R', "755", writepath])
        print ("[+] New file \"" + file + "\" Created")

if __name__ == '__main__':
    main()