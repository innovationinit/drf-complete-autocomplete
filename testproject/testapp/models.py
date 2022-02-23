from django.db import models


class Country(models.Model):

    name = models.CharField(max_length=200)


class Region(models.Model):

    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def get_name(self):
        return self.name


class Post(models.Model):

    name = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Address(models.Model):

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
