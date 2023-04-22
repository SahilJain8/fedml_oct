from django.db import models

# Create your models here.

import numpy as np

class MyCollection(models.Model):
    user_name = models.CharField(max_length=100)
    user_id = models.IntegerField()
    model_weights = models.BinaryField()
    time = models.DateTimeField()

    def set_weights(self, weights):
        self.model_weights = np.array(weights).tobytes()
        
    def get_weights(self):
        return np.frombuffer(self.model_weights)
