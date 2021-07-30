from django.core.paginator import Paginator
from django.db.models import Q, Count  # 조회용 Query 객체 생성
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):  # request는 장고에 의해 자동으로 전달되는 HTTP요청 객체이다.
    # request는 사용자가 전달한 데이터를 확인할 때 사용된다.

    """
    pybo 목록 출력
    """

    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get("kw", "")  # 검색어
    so = request.GET.get("so", "recent")  # 정렬기준

    # 정렬
    if so == "recommend":
        question_list = Question.objects.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-create_date"
        )
    elif so == "popular":
        question_list = Question.objects.annotate(num_answer=Count("answer")).order_by(
            "-num_answer", "-create_date"
        )
    else:  # recent
        question_list = Question.objects.order_by("-create_date")

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw)
            | Q(content__icontains=kw)  # 제목검색
            | Q(author__username__icontains=kw)  # 내용검색
            | Q(answer__author__username__icontains=kw)  # 질문 글쓴이검색  # 답변 글쓴이검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj, "page": page, "kw": kw, "so": so}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(
        Question, pk=question_id
    )  # 키워드 인자는 매개변수도 키워드인자의 키워드와 이름이 같아야한다.
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)
