#coding=utf-8
from django.db import models
from os.path import getsize, join
from django.conf import settings

# Create your models here.
#
#

    
class Archive(models.Model):
    title = models.CharField(u'名称', max_length=100, db_index=True)
    version = models.CharField(u'版本', max_length=10)
    category = models.CharField(u'类别', max_length=10)
    star = models.SmallIntegerField(u'star', default=0, blank=True)
    androidversion = models.CharField(u'安卓版本', max_length=150)
    screen = models.CharField(u'分辨率', max_length=200)
    author = models.CharField(u'作者', max_length=50)
    description = models.TextField()
    url = models.CharField(max_length=255, db_index=True)
    db_time = models.DateTimeField(u'发布时间', auto_now_add=True)    
    hits = models.IntegerField(u'点击次数',default=0, )
    downloads = models.IntegerField(u'下载',default=0)
    
    def __unicode__(self):
        return "%s[version:%s]" % (self.title, self.version)


class Upfile(models.Model):
    CATEGORY_CHOICES = (
                   (0, u'logo'), 
                   (1, u'图片'),
                   (2, u'文件'),                   
    )
    archive = models.ForeignKey(Archive)
    pic = models.FileField(u'文件', upload_to='media')
    length = models.IntegerField(u'大小', max_length=10, blank=True)
    category = models.IntegerField(u'类别', choices=CATEGORY_CHOICES)
    
#    def save(self, *args, **kwargs):
#        self.length = self.pic.size
#        super(Upfile, self).save(*args, **kwargs)
#        
    def __unicode__(self):
        return self.pic.name
    
    