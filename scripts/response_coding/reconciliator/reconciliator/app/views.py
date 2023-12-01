from django.shortcuts import render
from .utils import filter
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):

    qid = request.GET.get("qid") or "D3"
    qid = qid.upper()
    pid = request.GET.get("pid") or None
    pids = filter.getValidPids(qid)
    if pid == None or not pid.isdigit() or not int(pid) in pids:
        pid = pids[0]
    pid = int(pid)
    question_text = filter.getQuestionText(qid)
    terms = filter.getTerms(qid)
    response = filter.getResponse(qid, pid)
    codes = filter.getCodes(qid, pid)
    
    valid_pids = "-".join([str(i) for i in pids])
    final_pid = int(valid_pids.split("-")[-1])
    start_pid = int(valid_pids.split("-")[0])

    all_codes = []
    for c in codes.values():
        all_codes.extend(c)
    all_codes = "|".join(all_codes)

    questions = filter.getQuestions()
    
    return render(request, "index.html", {"question_text":question_text, 
                                          "qid":qid,
                                          "pid":pid,
                                          "response":response,
                                          "codes":codes,
                                          "valid_pids":valid_pids,
                                          "final_pid":final_pid,
                                          "start_pid":start_pid,
                                          "all_codes":all_codes,
                                          "questions": questions,
                                          "pids": pids})

def get_popup_content(request, question_id, content_id):
    print(question_id)
    content = filter.getDefinition(content_id, question_id)
    return render(request, 'popup_content.html', {'term':content_id,'content': content})

def dictionaryPage(request):
    question = request.GET.get("qid") or "D3"
    terms = filter.getTerms(question.upper())
    questions = filter.getQuestions()
    return render(request, "glossary.html", {"qid":question, "terms":terms, 
                                             "questions":questions})

@csrf_exempt
def update_content(request):
    if request.method == 'POST':

        qid = request.POST.get('selected_question')
        terms = filter.getTerms(qid.upper())

        updated_content = f'<ul>'
        for term in terms:
            updated_content += f"<li><span class=\"term\">{term.term}:</span> {term.definition}</li>"
        updated_content += "</ul>"

        return JsonResponse({'updated_content': updated_content})