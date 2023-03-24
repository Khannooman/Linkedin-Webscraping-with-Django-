from django.db import models

# Create your models here.
from django.db import models
import json

# Create your models here.
class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    Company = models.TextField(max_length=500, null = True)
    Location = models.TextField(max_length=500, null =True)
    JD = models.TextField(max_length=20000, null = True)
    posted = models.TextField(max_length=500, null = True)
    link = models.TextField(max_length=10000, null = True)
    @staticmethod
    def insert_from_json(filename):
        with open(filename) as f:
            data = json.load(f)
        for i in range(len(data["company"])):
            ID = data["PK"][i]
            Company = data["company"][i]
            Location = data["Location"][i]
            JD = data["Job Description"][i]
            posted = data["Posted_date"][i]
            link = data["Link"][i]
            Job.objects.create(id = ID, Company=Company, Location=Location, JD=JD, posted=posted, link=link)

# Job.insert_from_json("C:/Users/NOOMAN KHAN/Downloads/Final_data.json")