from django.db import models

class fileDoc(models.Model):
    '''
    model for storing temporarily the
    metadata of files user selected for upload
    '''
    id = models.AutoField(primary_key=True)
    file_id = models.CharField(max_length=256) #unique id for the file fetched from non-local sources
    name=models.CharField(max_length=256,null=True) #name of the file
    size=models.IntegerField()  #size of the bile in bytes
    url=models.CharField(max_length=256) #url of the file fetched fron non-local sources

    def __str__(self):
        return self.name
