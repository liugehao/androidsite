# Scrapy settings for androidscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os


BOT_NAME = 'androidscrapy'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['androidscrapy.spiders']
NEWSPIDER_MODULE = 'androidscrapy.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['androidscrapy.pipelines.DjangoPipeline']


def setup_django_env(path):
    import imp, os
    from django.core.management import setup_environ
     
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)
     
    setup_environ(project)
    import sys
    sys.path.append(os.path.abspath(os.path.join(path, os.path.pardir)))
 
current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
setup_django_env(os.path.join(current_dir, '../android/android/'))
