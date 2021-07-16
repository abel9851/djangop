from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)  # 글자수 제한이 있는 데이터
    content = models.TextField()  # 글자수 제한이 없는 데이터
    create_date = models.DateTimeField()  # 시간 관련 속성

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()