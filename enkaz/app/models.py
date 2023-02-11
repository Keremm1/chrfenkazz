from django.db import models
# Create your models here.

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    help_count = models.PositiveIntegerField(default=0, editable=False)
    can_count = models.PositiveIntegerField(default=0, editable=False)
    

    def __str__(self):
        return self.name

class HelpModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,blank=False, null=False,related_name='help_user')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,blank=False, null=False,related_name='help_model')
    description = models.TextField(max_length=5000,blank=False, null=False)
    city = models.CharField(max_length=100,blank=False, null=False)
    town = models.CharField(max_length=100,blank=False, null=False)
    street = models.CharField(max_length=100,blank=False, null=False)
    neighbourhood = models.CharField(max_length=200,blank=False, null=False)
    username = models.CharField(max_length=100,blank=False, null=False)
    phone = models.CharField(max_length=100,blank=False, null=False)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.category.help_count += 1
        self.category.save()
    def delete(self, *args, **kwargs):
        self.category.help_count -= 1
        self.category.save()
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.category.name + str(self.category.help_count)

class CanModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,blank=False, null=False,related_name='can_user')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,blank=False, null=False,related_name='can_model')
    description = models.TextField(max_length=5000,blank=False, null=False)
    city = models.CharField(max_length=100,blank=False, null=False)
    town = models.CharField(max_length=100,blank=False, null=False)
    street = models.CharField(max_length=100,blank=False, null=False)
    neighbourhood = models.CharField(max_length=200,blank=False, null=False)
    phone = models.CharField(max_length=100,blank=False, null=False)
    username = models.CharField(max_length=100,blank=False, null=False)
    ip = models.GenericIPAddressField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.category.can_count += 1
        self.category.save()
    def delete(self, *args, **kwargs):
        self.category.can_count -= 1
        self.category.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.category.name + str(self.category.can_count)