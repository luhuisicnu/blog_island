import sys
import os


sys.path.append('/root/blog_island')
sys.path.append('/root/blog_island/venv/lib/python2.6/site-packages')


environ = {
    'HISTTIMEFORMAT': '%Y-%m-%d %H:%M:%S ', 
    'LESSOPEN': '|/usr/bin/lesspipe.sh %s',
    'CVS_RSH': 'ssh', 
    'LOGNAME': 'apache', 
    'USER': 'apache', 
    'QTDIR': '/usr/lib64/qt-3.3', 
    'PATH': '/usr/local/erlang/bin:/usr/local/mysql/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/python34/bin:/root/bin:/usr/local/bin', 
    'MAIL_USERNAME': 'luhuisicnu@163.com', 
    'LANG': 'en_US.UTF-8', 
    'QTLIB': '/usr/lib64/qt-3.3/lib', 
    'TERM': 'xterm', 
    'SHELL': '/bin/bash', 
    'QTINC': '/usr/lib64/qt-3.3/include', 
    'G_BROKEN_FILENAMES': '1', 
    'HISTSIZE': '1000', 
    'FLASKY_ADMIN': 'luhuisicnu@163.com', 
    'JAVA_HOME': '/usr/java/java', 
    'HOME': '/root/blog_island', 
    'HISTFILESIZE': '100000', 
    'BLOG_ISLAND_MAIL_SENDER': 'Blog Island Admin <luhuisicnu@163.com>', 
    'SHLVL': '1', 
    'CLASSPATH': '.:/usr/java/java/lib:/usr/java/java/jre/lib', 
    'JRE_HOME': '/usr/java/java/jre', 
    '_': '/usr/bin/python', 
    'GREP_OPTIONS': '--color=auto', 
    'MAIL_PASSWORD': '1uhuisicnu163', 
    'HOSTNAME': '10-9-21-98', 
    'BLOG_ISLAND_MAIL_PASSWORD': '1uhuisicnu163', 
    'HISTCONTROL': 'ignoredups', 
    'BLOG_ISLAND_MAIL_USERNAME': 'luhuisicnu@163.com', 
    'PWD': '/root/blog_island', 
}
for key in environ:
    os.environ[key] = environ[key]


from manage import app as application
