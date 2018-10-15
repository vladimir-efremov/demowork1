from django.db import models




class HardwareModule(models.Model):
	name = models.CharField(max_length=250)
	must_be = models.IntegerField(default=0)
	count = models.IntegerField(default=0)
	arrive = models.IntegerField(default=0)
	need = models.IntegerField(default=0)
    
	def __str__(self):
		return self.name

