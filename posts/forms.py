from posts.models import PostModel
from django import forms


class StyleFormMixin:
    """Form stylization"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class PostModelForm(StyleFormMixin, forms.ModelForm):
    """Form for model PostModel"""

    class Meta:
        model = PostModel
        fields = ("title", "description", "is_free", "image")
