SB Blog
=======
A very simple blog "engine" for django, originally based on the blog project from the book "Practical Django Projects" by James Bennett (http://apress.com/book/view/9781590599969).  Released and licensed under the MIT license (http://www.opensource.org/licenses/mit-license.php).

It is a very simple blog designed to get someone up and running quickly, with the ability to customise it easily.  All the existing blog solutions seemed to require a lot of work to get running.  This blog should be up and running pretty quickly, with a very minimal set of dependencies.  I make no claims to this being the best blog "engine" for django, nor the most secure.  Its just there to be used as a starting point.  I'm currently using the blog and developing it as I go along

Install
=======
Dependencies:
 * django-tagging-0.3.1.tar.gz  (http://code.google.com/p/django-tagging/)
 * Markdown-2.0.3.zip (http://www.freewisdom.org/projects/python-markdown/)

Install the dependencies.

Get copy of sbblog::

    pip install django-sbblog

Add following three lines to the INSTALLED_APPS section of your settings.py::

    'django.contrib.comments',
    'tagging',
    'sbblog',


Add the following to the TEMPLATES section of your settings.py::

    '<path to sbblog>/templates'


For spam protection get a key for Akismet from http://akismet.com/ and then add the key to your settings.py::

    AKISMET_API_KEY = '<key>'


The default install takes posts in the Markdown syntax and generates the HTML.  The blog can be used with the TinyMCE editor if it is installed, or with straight HTML entered into the entry box, you just need to add an extra setting to the settings.py::

    HTML_ENTRY = True


Now run:: 

    python manage.py syncdb


This will setup all the tables needed.  Now setup the urls needed.  Add the following to your urls.py::

    (r'^tags/', include('sbblog.urls.tags')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'', include('sbblog.urls.entries')),


Now it should be installed and ready to run.  
