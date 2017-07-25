from django.shortcuts import render
from collections import defaultdict
from calaccess_processed.models import OCDElectionProxy



def election_list(request):
    object_list = OCDElectionProxy.objects.all()
    group_list = defaultdict()
    for obj in object_list:
        group_list.setdefault(obj.date.year, []).append(obj)
    context = dict(object_list=object_list, group_list=group_list)
    template = "election_list.html"
    return render(request, template, context)
