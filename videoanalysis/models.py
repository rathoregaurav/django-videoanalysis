# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class VideoAnaylysis(models.Model):
    total_frames=models.CharField(max_length=20)
    total_duration_sec=models.CharField(max_length=20)
    total_analysed_duration = models.CharField(max_length=35)
    video_path = models.FileField(upload_to='video_to_analysis',null=True,blank=True, verbose_name='Video Analysis')
    total_time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')
    
      