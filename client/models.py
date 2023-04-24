from django.db import models
import numpy as np
# Create your models here.

class client_model_weights(models.Model):
    user_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    model_weights = models.JSONField(default=list)
    
    def set_array(self, array):
        self.array_field = array.tolist()

    def get_array(self):
        return np.array(self.array_field)
