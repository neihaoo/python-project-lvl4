"""Labels application forms."""

from django.forms import ModelForm

from labels.models import Label


class LabelForm(ModelForm):
    """Label form."""

    class Meta(object):
        model = Label
        fields = ('name',)
