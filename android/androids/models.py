#coding=utf-8
from django.db import models
from os.path import getsize, join
from django.conf import settings

    
class Archive(models.Model):
    title = models.CharField(u'名称', max_length=100, db_index=True)
    version = models.CharField(u'版本', max_length=30)
    category = models.CharField(u'类别', max_length=20)
    star = models.DecimalField(u'星级', max_digits=2, decimal_places=1, default=0, blank=True)
    androidversion = models.CharField(u'安卓版本', max_length=200)
    screen = models.CharField(u'分辨率', max_length=200)
    author = models.CharField(u'作者', max_length=150)
    language = models.CharField(u'语言', max_length=30, blank=True)
    up_dt = models.DateField(u'更新时间', blank=True)
    powerconsumption = models.CharField(u'耗电', max_length=30, blank=True)
    price = models.CharField(u'资费', max_length=30, blank=True)
    description = models.TextField(u'简介')
    url = models.CharField(max_length=255, db_index=True)
    db_time = models.DateTimeField(u'发布时间', auto_now_add=True)    
    hits = models.IntegerField(u'点击次数',default=0, )
    
    
    def __unicode__(self):
        return "%s[version:%s]" % (self.title, self.version)


class Upfile(models.Model):
    CATEGORY_CHOICES = (
                   (0, u'logo'), 
                   (1, u'图片'),
                   (2, u'文件'),                   
    )
    archive = models.ForeignKey(Archive)
    path = models.FileField(u'文件', upload_to='media')
    length = models.IntegerField(u'大小', max_length=10, blank=True)
    category = models.IntegerField(u'类别', choices=CATEGORY_CHOICES)
    url = models.CharField(max_length=255, db_index=True)
     
#    def save(self, *args, **kwargs):
#        self.length = self.pic.size
#        super(Upfile, self).save(*args, **kwargs)
#        
    def __unicode__(self):
        return self.path.name
    
    
