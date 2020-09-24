from django.db import models


class StudyGroup(models.Model):
    # 각각의 변수 / 보여지는 단어 로 이루어진 튜플을 가진 dict를 다음과 같이 생성
    field = models.CharField(max_length=80,verbose_name='분야')
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.CharField(max_length=100, verbose_name='작성자')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    image = models.ImageField(upload_to='studyGroups/image/', null=True, blank=True, verbose_name='이미지')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Book(models.Model):
    field = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    image_url = models.CharField(max_length=500)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.title