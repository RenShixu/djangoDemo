from django.db import models
#from datetime import datetime
from datetime import datetime

# Create your models here.
class Pictures(models.Model):
    title = models.CharField(max_length=32)
    p_url = models.CharField(max_length=100)
    thumb_p_url = models.CharField(max_length=100)
    addtime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "title:"+self.title+"|p_url:"+self.p_url+"|thumb_p_url:"+self.thumb_p_url+"|addtime:"+str(self.addtime)

    class Meta:
        db_table = "pictures"