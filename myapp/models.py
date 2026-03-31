from django.contrib.auth.models import User
from django.db import models


class Report(models.Model):
    # 誰が書いたか（User）を紐付ける。Userが消えたら日報も消える設定
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="photos/", null=True, blank=True)
    upload_file = models.FileField(upload_to="uploads/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.title}"


class ReportAttachment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.split("/")[-1]

    @property
    def is_image(self):
        name = self.file.name.lower()
        return name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"))
