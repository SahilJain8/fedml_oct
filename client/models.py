from django.db import models
import numpy as np


class client_model_weights(models.Model):
    user_name = models.CharField(max_length=255)
    user_id = models.IntegerField()


