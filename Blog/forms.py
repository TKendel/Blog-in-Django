from django import forms
from django.core.validators import validate_email
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post,Tag,Settings,Category,Comment
from .validators import validate_small_length,validate_description,validate_number


class PostForm(ModelForm):
	#multiple choice checkbox for tags
	tags = ModelMultipleChoiceField(	#generirira input filed u formu prema MChoiceFile classi
		queryset = Tag.objects.all(), #skup objekta sa kojim ocu napraviti odabir vise dijelova
		widget = CheckboxSelectMultiple, #koji widget ocu da se koristi u ovome
		required = False #da user netreba izabrat tag( VJEROJATNO CE TREBAT PROMJENITI )
	)

	#validation
	title = forms.CharField( validators=[validate_small_length], required = True)
	#validators=[validate_description] ak ce trebat
	description = forms.CharField(widget=SummernoteWidget())

	#model data
	class Meta: #meta odreduje sta se automatski generira sto ovis o tome sto se u njoj nalazi
		model = Post #tablicaa sa kojom forma radi
		fields = ["title","description","thumbnail","category","tags"] #fielodivi sa kojima radi iz definiranog modela
		labels = {
			'title': _("The title of the post"),
		}


class CommentForm(forms.ModelForm):

	text = forms.CharField(widget=SummernoteWidget(),validators=[validate_description])
	class Meta:
		model = Comment
		fields = ["author","text"]

 	
class CategoryForm(ModelForm):
	name = forms.CharField(validators=[validate_small_length], required=True )
	class Meta:
		model = Category
		fields = ["name"]


class TagForm(ModelForm):
	name = forms.CharField(validators=[validate_small_length], required=True )
	class Meta:
		model = Tag
		fields = ["name"]


class SettingsForm(ModelForm):
	siteName = forms.CharField(validators =[validate_small_length])
	contact_number = forms.CharField(validators=[validate_number])
	contact_address = forms.CharField(validators=[validate_small_length])
	email = forms.EmailField()
	class Meta:
		model = Settings
		fields = ["siteName","contact_number","contact_address","email"]


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ["first_name", "last_name", "email"]