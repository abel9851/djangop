from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Question, Answer
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


@login_required(login_url="common:login")
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()
    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)  # 아래의 form과 id는 다른 것이라고 추측, 같을 수도 있고.

        if form.is_valid():  # post로 받은 데이터가 유효한지 검사.
            question = form.save(commit=False)  # 임시저장. 이유는 create_date가 비어있어서.
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {"form": form}
    return render(
        request, "pybo/question_form.html", context
    )  # render는 했지만, html 탬플릿파일에서 form.as_p와 같이 form직접 쓰지 않았기 때문에 html 템플릿파일에 쓴 form태그 안에 있는 코드가 적용된다.


@login_required(login_url="common:login")
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("pybo:detail", question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect("pybo:detail", question_id=question.id)

    else:
        form = QuestionForm(instance=question)
    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, question_id):

    """
    질문 삭제
    """

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("pybo:detail", question_id=question.id)
    else:
        question.delete()
    return redirect("pybo:index")


@login_required(login_url="common:login")
def answer_modify(request, answer_id):

    """
    pybo 답변수정
    """

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("pybo:detail", question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("pybo:detail", question_id=answer.question.id)

    else:
        form = AnswerForm(instance=answer)
    context = {"answer": answer, "form": form}
    return render(request, "pybo/answer_form.html", context)


@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없습니다.")
    else:
        answer.delete()
    return redirect("pybo:detail", question_id=answer.question.id)
