from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm


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
