from django.core import paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


def index(request):  # request는 장고에 의해 자동으로 전달되는 HTTP요청 객체이다.
    # request는 사용자가 전달한 데이터를 확인할 때 사용된다.

    """
    pybo 목록 출력
    """
    page = request.GET.get("page", "1")  # 페이지

    question_list = Question.objects.order_by("-create_date")

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj}
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


def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()
    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)  # 아래의 form과 id는 다른 것이라고 추측, 같을 수도 있고.

        if form.is_valid():  # post로 받은 데이터가 유효한지 검사.
            question = form.save(commit=False)  # 임시저장. 이유는 create_date가 비어있어서.
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {"form": form}
    return render(
        request, "pybo/question_form.html", context
    )  # render는 했지만, html 탬플릿파일에서 form.as_p와 같이 form직접 쓰지 않았기 때문에 html 템플릿파일에 쓴 form태그 안에 있는 코드가 적용된다.
