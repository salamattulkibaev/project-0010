from django.db import models
from Whym import settings
from locations.models import City
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import  pre_save
from django.utils.text import slugify
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

class Category(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Status(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(status=2).filter(updated_at__lte=timezone.now())

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return ' %s' % (self.name)

    class Meta:
        db_table = 'subcategory'
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, verbose_name="Автор", default=3)
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    slug = models.SlugField(unique = True)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        verbose_name = "Фото",
        upload_to = upload_location,
        height_field = 'height_field',
        width_field = 'width_field',
        blank=True)
    height_field = models.IntegerField(verbose_name="Высота", default=0)
    width_field = models.IntegerField(verbose_name="Ширина", default=0)
    category = models.ForeignKey(Subcategory,on_delete = models.CASCADE , verbose_name="Категория", default=15)
    city = models.ForeignKey(City,on_delete=models.SET_NULL, verbose_name="Город", null=True)
    status = models.ForeignKey(Status, default = 1, on_delete=models.CASCADE, verbose_name="Статус")
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время обновления", auto_now=True)

    objects = PostManager()

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"slug": self.slug})

    class Meta:
        db_table = "post"
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ['-updated_at']

    @property
    def comments(self):
        instance    = self
        qs          = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


