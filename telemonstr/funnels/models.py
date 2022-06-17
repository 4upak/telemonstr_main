from django.db import models

# Create your models here.
class Funnel(models.Model):

    funnel_name = models.CharField(max_length = 250, null=False, unique=True)


class Funnel_message(models.Model):

    index_id = models.IntegerField(default = 0)
    text_message = models.TextField()
    json_data = models.JSONField()
    answer_to = models.IntegerField(null = False)
    user_id = models.IntegerField(null = False)
    delay_before = models.IntegerField(default = 0)
    delay_after = models.IntegerField(default = 0)
    message_photo = models.ImageField(upload_to='funnels_images/', height_field=None, width_field=None, max_length=100)
    funnel = models.ForeignKey('Funnel', on_delete=models.CASCADE)

