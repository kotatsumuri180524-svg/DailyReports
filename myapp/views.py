import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Report, ReportAttachment


@login_required
def index(request):
    # --- 保存処理 (POST) ---
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        attachments = request.FILES.getlist("attachments")
        image = None
        upload_file = None

        for attachment in attachments:
            content_type = (attachment.content_type or "").lower()
            if image is None and content_type.startswith("image/"):
                image = attachment
            elif upload_file is None:
                upload_file = attachment

        report = Report.objects.create(
            title=title,
            content=content,
            author=request.user,
            image=image,
            upload_file=upload_file,
        )

        for attachment in attachments:
            ReportAttachment.objects.create(report=report, file=attachment)

        return redirect("index")

    # --- データの取得と検索処理 ---
    reports = (
        Report.objects.prefetch_related(
            Prefetch("attachments", queryset=ReportAttachment.objects.order_by("uploaded_at"))
        )
    )
    if not request.user.is_staff:
        reports = reports.filter(author=request.user)

    search_word = request.GET.get("search")
    if search_word:
        reports = reports.filter(
            Q(title__icontains=search_word)
            | Q(content__icontains=search_word)
            | Q(author__username__icontains=search_word)
        )

    search_date = request.GET.get("date")
    if search_date:
        reports = reports.filter(created_at__date=search_date)

    reports = reports.order_by("-created_at")

    return render(request, "myapp/index.html", {"reports": reports})


@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.author == request.user or request.user.is_staff:
        report.delete()
    return redirect("index")


@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if report.author != request.user and not request.user.is_staff:
        return redirect("index")

    if request.method == "POST":
        report.title = request.POST.get("title")
        report.content = request.POST.get("content")
        report.save()
        return redirect("index")

    return render(request, "myapp/edit.html", {"report": report})


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv; charset=cp932")
    response["Content-Disposition"] = 'attachment; filename="nippo_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "担当者", "タイトル", "内容", "投稿日時"])

    if request.user.is_staff:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(author=request.user)

    for r in reports.order_by("-created_at"):
        author_name = r.author.username if r.author else "不明"
        writer.writerow([r.id, author_name, r.title, r.content, r.created_at.strftime("%Y/%m/%d %H:%M")])

    return response
