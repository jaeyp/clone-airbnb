from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, DetailView
from users import models as user_models
from . import models, forms

# Create your views here.


def go_conversation(request, host_pk, guest_pk):
    """ if conversation between two users exists, return conversation id
        else create a new conversation and return it
    """
    # host = user_models.User.objects.get_or_none(pk=host_pk)
    # guest = user_models.User.objects.get_or_none(pk=guest_pk)
    host = user_models.User.objects.get(pk=host_pk)
    guest = user_models.User.objects.get(pk=guest_pk)
    if host is not None and guest is not None:
        """ This is inefficient cause it access database twice.
        """
        # conversation = models.Conversation.objects.filter(participants=host).filter(participants=guest)

        """ Instead, use Q objects
            https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects
        """

        # TODO: Check queryset2sql for debugging
        # bug fix - Q object doesn't workd with & operator for many to many field
        #
        # try:
        #     conversation = models.Conversation.objects.get(Q(participants=host) & Q(participants=guest))
        #     # conversation = models.Conversation.objects.filter(participants__in=[host, guest])
        #     # conversation = models.Conversation.objects.filter(participants=host).filter(participants=guest)
        # except models.Conversation.DoesNotExist:
        #     conversation = models.Conversation.objects.create()
        #     # add(*objs, bulk=True, through_defaults=None)
        #     # *objs: we can pass multiple objs as argument like add(host, guest)
        #     conversation.participants.add(host, guest)
        # return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))

        # Solution:
        conversation = models.Conversation.objects.filter(participants=host).filter(participants=guest)[:1].get()
        if conversation is None:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))

        # conversation = None
        # qs_conversations = models.Conversation.objects.filter(Q(participants=guest))
        # print(qs_conversations)
        # for c in qs_conversations:
        #     qs_participants = c.participants.all()
        #     print(qs_participants)
        #     for p in qs_participants:
        #         if p.id == host.id:
        #             conversation = c
        # if conversation is None:
        #     conversation = models.Conversation.objects.create()
        #     conversation.participants.add(host, guest)
        # return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


""" class ConversationDetailView(DetailView):

    model = models.Conversation
    template_name = "conversations/detail.html" """


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get(pk=pk)
        if not conversation:
            raise Http404(0)
        # form = forms.AddCommentForm()  # we don't use form anymore for conversation detail view
        return render(
            # self.request, "conversations/detail.html", {"conversation": conversation, "form": form}
            self.request,
            "conversations/detail.html",
            {"conversation": conversation},  # we don't use form anymore for conversation detail view
        )  # you can skip "kwargs=" for the third parameters

    def post(self, *args, **kwargs):
        """  we don't use form anymore for conversation detail view
        form = forms.AddCommentForm(self.request.POST)
        print(form)
        """
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get(pk=pk)
        if message is not None:
            models.Message.objects.create(message=message, user=self.request.user, conversation=conversation)
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
