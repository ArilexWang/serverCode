from django.db import models
import django.utils.timezone as timezone
from datetime import datetime
# Create your models here.


class test(models.Model):
	name = models.CharField(max_length=8,default="")

class teacher(models.Model):
	email = models.CharField(primary_key=True,max_length=32,default="")
	name = models.CharField(max_length=8,default="")
	password = models.CharField(max_length=16,default="")
class course(models.Model):
	name = models.CharField(max_length=16,default="")
	grade = models.CharField(max_length=9,default="")
	group_num = models.IntegerField(default=0)
	time = models.CharField(max_length=16,default="")
	create_time = models.DateTimeField(default=datetime.now,blank=True)

class teaches(models.Model):
	teacher = models.ForeignKey(teacher)
	course = models.ForeignKey(course)
class T_Img_Item(models.Model):
	teaches = models.ForeignKey(teaches)
	create_time = models.CharField(max_length=32,default="")
	img_path = models.CharField(max_length=128,default="")
	content = models.CharField(max_length=256,default="")
class student(models.Model):
	name = models.CharField(max_length=8,default="")
	email = models.CharField(primary_key=True,max_length=30,default="")
	password = models.CharField(max_length=16,default="")
class takes(models.Model):
	student = models.ForeignKey(student)
	course = models.ForeignKey(course)
class S_Img_Item(models.Model):
	course = models.ForeignKey(course,null=True)
	student = models.ForeignKey(student,null=True)
	create_time = models.CharField(max_length=32,default="")
	img_path = models.CharField(max_length=128,default="")
	content = models.CharField(max_length=256,default="")
class group(models.Model):
	course = models.ForeignKey(course,null=True)
class group_member(models.Model):
	group = models.ForeignKey(group,null=True)
	student = models.ForeignKey(student,null=True)

class un_group_member(models.Model):
	student = models.ForeignKey(student,null=True)
	course = models.ForeignKey(course,null=True)

class section(models.Model):
	course = models.ForeignKey(course,null=True)
	content = models.CharField(max_length=256,default="")
	homework_ddl = models.CharField(max_length=64,default="")
	create_time = models.CharField(max_length=64,default="")

class homework(models.Model):
	student = models.ForeignKey(student,null=True)
	section = models.ForeignKey(section,null=True)
	group = models.ForeignKey(group,null=True)
	content = models.CharField(max_length=256,default="")
	img_path = models.CharField(max_length=128,default="")
	create_time = models.CharField(max_length=32,default="")
	get_star = models.IntegerField(default=0)

