from django.db import models
import numpy as np

import json


class model_data(models.Model):
    user_name  = models.CharField(max_length=255)
    user_id = models.IntegerField()
    model_weights = models.JSONField()

    @property
    def array(self):
        return np.array(json.loads(self.model_weights))
    
    @array.setter
    def array(self, model_weights):
        self.model_weights = json.dumps(model_weights.tolist())