from client.models import Client
from client.models import Comment as ClientComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from team.models import Team

from .forms import AddCommentForm, AddFileForm, AddLeadForm
from .models import Lead


class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    context_object_name = "leads"

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, converted_to_client=False
        )


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    queryset = Lead.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        context["fileform"] = AddFileForm()

        return context

    def get_queryset(self):
        return self.queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get("pk")
        )


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy("leads:list")

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get("pk")
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = AddLeadForm
    success_url = reverse_lazy("leads:list")

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get("pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить"
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = AddLeadForm
    success_url = reverse_lazy("leads:list")

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get("pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context["team"] = team
        context["title"] = "Добавить"

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.active_team
        self.object.save()

        return redirect(self.success_url)


class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = self.request.user.userprofile.active_team
            file.lead_id = pk
            file.created_by = request.user
            file.save()

        return redirect("leads:detail", pk=pk)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.active_team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect("leads:detail", pk=pk)


class ConvertToClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = self.request.user.userprofile.active_team

        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team,
        )
        lead.converted_to_client = True
        lead.save()

        messages.success(request, "Стал клиентом")

        return redirect("leads:list")


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team,
    )
    lead.converted_to_client = True
    lead.save()

    # Конвертируем лид комменты в клиент комменты

    comments = lead.comments.all()

    for comment in comments:
        ClientComment.objects.create(
            client=client,
            content=comment.content,
            created_by=comment.created_by,
            team=team,
        )

    messages.success(request, "Стал клиентом")

    return redirect("leads:list")
