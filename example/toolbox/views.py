from django.shortcuts import render
from collections import defaultdict
from calaccess_processed.models import OCDElectionProxy



def election_list(request):
    object_list = OCDElectionProxy.objects.all()
    group_dict = defaultdict()
    for obj in object_list:
        group_dict.setdefault(obj.date.year, []).append(obj)
    group_list = sorted(group_dict.items(), key=lambda x:x[0], reverse=True)
    context = dict(object_list=object_list, group_list=group_list)
    template = "election_list.html"
    return render(request, template, context)


def election_detail(request, id):
    obj = OCDElectionProxy.objects.get(id=id)
    context = dict(object=obj)
    template = "election_detail.html"
    return render(request, template, context)
