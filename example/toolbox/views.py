from django.db import ProgrammingError
from django.shortcuts import render
from collections import defaultdict
# from calaccess_processed_campaignfinance.proxies import (
#     OCDCommitteeProxy,
#     OCDFilingProxy,
#     OCDFilingActionProxy
# )
from calaccess_processed_elections.proxies import (
    OCDPostProxy,
    OCDPersonProxy,
    OCDElectionProxy,
    OCDCandidacyProxy,
    OCDPartyProxy
)
from opencivicdata.elections.models import CandidateContest
from django.views.generic import DetailView, ListView


def index(request):
    return render(request, "index.html")


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


class CandidateContestDetail(DetailView):
    model = CandidateContest
    template_name = 'candidatecontest_detail.html'

    def get_context_data(self, object=None):
        context = super(CandidateContestDetail, self).get_context_data()
        context['candidate_list'] = OCDCandidacyProxy.objects.filter(contest=context['object'])
        return context


class PostDetail(DetailView):
    model = OCDPostProxy
    template_name = "post_detail.html"


class PersonList(ListView):
    model = OCDPersonProxy
    template_name = "person_list.html"


class PersonDetail(DetailView):
    model = OCDPersonProxy
    template_name = "person_detail.html"

    def get_context_data(self, object=None):
        context = super(PersonDetail, self).get_context_data()
        context['candidate_list'] = OCDCandidacyProxy.objects.filter(person=context['object'])
        return context


class PartyList(ListView):
    model = OCDPartyProxy
    template_name = "party_list.html"


class PartyDetail(DetailView):
    model = OCDPartyProxy
    template_name = "party_detail.html"


class CandidateNoPartyList(ListView):
    """
    Lists all the OCD candidates with an unknown party.
    """
    template_name = "candidatenoparty_list.html"

    def get_queryset(self):
        try:
            return OCDCandidacyProxy.objects.filter(party__in=[
                OCDPartyProxy.objects.unknown()
            ])
        except (OCDPartyProxy.DoesNotExist, ProgrammingError):
            return OCDCandidacyProxy.objects.none()


class PrimaryNoPartyList(ListView):
    """
    Lists all the OCD partisan primaries with an unknown party.
    """
    template_name = "electionnoparty_list.html"

    def get_queryset(self):
        primary_list = OCDElectionProxy.partisan_primaries.all()
        contest_list = CandidateContest.objects.filter(election__in=primary_list)
        try:
            return contest_list.filter(party__in=[
                OCDPartyProxy.objects.unknown(),
                OCDPartyProxy.objects.get(name="NO PARTY PREFERENCE")
            ])
        except OCDPartyProxy.DoesNotExist:
            return CandidateContest.objects.none()


class CommitteeList(ListView):
    model = OCDCommitteeProxy
    template_name = "committee_list.html"


class CommitteeDetail(DetailView):
    model = OCDCommitteeProxy
    template_name = "committee_detail.html"


class FilingDetail(DetailView):
    model = OCDFilingProxy
    template_name = "filing_detail.html"


class FilingActionDetail(DetailView):
    model = OCDFilingActionProxy
    template_name = "filingaction_detail.html"
