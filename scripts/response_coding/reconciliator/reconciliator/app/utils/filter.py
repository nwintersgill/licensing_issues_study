
from app.models import *
from django.db.models import Q

def getQuestions():
    selections = Terms.objects.values("qid").distinct()
    return [x["qid"] for x in selections]

def getTerms(question):
    terms = Terms.objects.filter(qid=question)
    return terms.order_by("term")

def getResponse(qid, pid):
    response = Responses.objects.filter(qid=qid).filter(pid=pid)
    if len(response) > 0:
        return response[0]
    return []

def getQuestionText(question):
    return Questions.objects.get(qid=question).text

def getCodes(qid, pid):
    response = ResponseCodes.objects.filter(qid=qid).filter(pid=pid)
    if len(response) > 0:
        response = response[0]
        codes = {}
        codes["codes_r1"] = response.r0.split()
        codes["codes_r2"] = response.r1.split()
        codes["codes_r3"] = response.r2.split()
        codes["codes_r1r2"] = response.r0r1.split()
        codes["codes_r1r3"] = response.r0r2.split()
        codes["codes_r2r3"] = response.r1r2.split()
        codes["codes_all"] = response.r0r1r2.split()
        return codes
    return None

def getValidPids(qid):
    pids = ResponseCodes.objects.filter(qid=qid)

    cr0 = ~Q(r0__isnull=True) & ~Q(r0__exact='')
    cr1 = ~Q(r1__isnull=True) & ~Q(r1__exact='')
    cr2 = ~Q(r2__isnull=True) & ~Q(r2__exact='')
    cr0r1 = ~Q(r0r1__isnull=True) & ~Q(r0r1__exact='')
    cr0r2 = ~Q(r0r2__isnull=True) & ~Q(r0r2__exact='')
    cr1r2 = ~Q(r1r2__isnull=True) & ~Q(r1r2__exact='')
    cr0r1r2 = ~Q(r0r1r2__isnull=True) & ~Q(r0r1r2__exact='')

    combined_condition = cr0 | cr1 | cr2 | cr0r1 | cr0r2 | cr1r2 | cr0r1r2

    pids = pids.filter(combined_condition).values("pid").distinct()
    return [x["pid"] for x in pids]

def getDefinition(term, qid):
    terms = Terms.objects.filter(qid=qid).filter(term=term)
    if len(terms) > 0:
        return terms[0].definition
    else:
        return "TERM NOT IN DICTIONARY"