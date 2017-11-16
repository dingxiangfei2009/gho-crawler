from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return "Country ID: %d, %s" % (self.id, self.name)

class StatisticItem(models.Model):
    name = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='')
    description = models.TextField(default='')

    def __str__(self):
        return "Statistic Item ID: %d, %s, %s" % (self.id, self.name, self.type)

class Statistics(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.ForeignKey(StatisticItem, on_delete=models.CASCADE)
    numeric_value = models.FloatField(null=True)
    int_value = models.BigIntegerField(null=True)
    json_value = JSONField(null=True)
    binary_value = models.BinaryField(null=True)
    datetime_value = models.DateTimeField(null=True)
    string_value = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    serial = models.CharField(max_length=255,default='')
    date = models.DateTimeField(null=True)

    def __str__(self):
        return "Statistic ID: %d, Statistic %d, Country %d, values: ..." % (
               self.id, self.name.pk, self.country.pk
        )