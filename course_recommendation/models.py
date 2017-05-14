from django.db import models

class jobs(models.Model):
    company=  models.CharField(max_length=50,null=True)
    Jobtitle = models.CharField(max_length=50,null=True)
    domain = models.CharField(max_length=100, default='Others')
    location= models.CharField(max_length=50,null=True)
    description=models.CharField(max_length=10000,null=True)
    latitude = models.FloatField(max_length=150,null=True)
    longitude = models.FloatField(max_length=150,null=True)
    url = models.URLField(max_length=300,null=True)


    def __str__(self):
        return self.Jobtitle+'-'+self.company+'-'+self.location+'-'+self.url

class courses(models.Model):
    number=models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    department = models.CharField(max_length=45)
    program = models.CharField(max_length=45)
    url = models.URLField(max_length=100,null=True)

    def __str__(self):
        return self.number+'-' +self.name+'-'+self.description+'-'+self.program+'-'+self.url

class services(models.Model):
    name=models.CharField(max_length=50)
    url=models.URLField(max_length=100)
    number=models.CharField(max_length=20)

    def __str__(self):
        return self.name + '-' + self.number + '-' + self.url

# f=open('montgomery.txt','r')
# xyz=f.read()
# xyz=eval(xyz)
# j=0
# k=[]
# for i in xyz:
#     abc = jobs.objects.filter(latitude=i.get('latitude'),longitude=i.get('longitude'))
#     if abc is None:
#         a_j=jobs(company=i.get('company'),Jobtitle=i.get('jobtitle'),location=i.get('location'),latitude=i.get('latitude'),longitude=i.get('longitude'),url=i.get('url'),description=i.get('description2'))
#         k.append(a_j)
#         j+=1
# for job in k:
#     job.save()
