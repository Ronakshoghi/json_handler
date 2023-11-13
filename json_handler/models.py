from django.db import models


class JSONData(models.Model):
    upload = models.FileField(upload_to='json_files/')
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.upload.name
