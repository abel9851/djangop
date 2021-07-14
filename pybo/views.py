from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):  # request는 장고에 의해 자동으로 전달되는 HTTP요청 객체이다.
    # request는 사용자가 전달한 데이터를 확인할 때 사용된다.

    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by("-create_date")
    context = {"question_list": question_list}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(
        Question, id=question_id
    )  # 키워드 인자는 매개변수도 키워드인자의 키워드와 이름이 같아야한다.
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)
