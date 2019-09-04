from django.db import models


class Picture(models.Model):
    
    picture = models.ImageField(upload_to="images", default=None, blank=True)
    content_type = models.CharField(max_length=50)

    def __unicode__(self):
        return 'id=' + str(self.id)

