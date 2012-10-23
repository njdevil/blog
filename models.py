from django.db import models

class Tag(models.Model):
        tag=models.CharField(max_length=40)
        class Meta:
                ordering=('tag',)

        def __unicode__(self):
                return self.tag

class Post(models.Model):
	category=models.ForeignKey(Category)
	date=models.DateTimeField(auto_now_add=True)
	title=models.CharField(max_length=200, unique=True)
	slug=models.CharField(max_length=200, unique=True)
	content=models.TextField()
	tags=models.ManyToManyField(Tag)
	viewable=models.NullBooleanField()

	def __unicode__(self):
		return self.title


class Comment(models.Model):
	title=models.ForeignKey(Post)
	date=models.DateTimeField(auto_now_add=True)
	content=models.TextField()
	approved=models.NullBooleanField()

	class Meta:
		ordering=('title',)
	
	def __unicode__(self):
		return u'%s %s' % (self.user, self.date)

