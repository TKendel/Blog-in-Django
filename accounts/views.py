from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login

from Blog.models import Settings
# Create your views here.


class SignUp(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'SignUp.html'

	#ovako mozes email field i formi(username u trenutnom slucaju) prije nego sto se otvori stvarna forma za popunu
	def post(self, request, *args, **kwargs):
		settings = Settings.objects.get(id=1)
		Title = settings.siteName
		#ako se nalazi welcomeemail u POST metodi
		if "WelcomeUsername" in request.POST:
			#popuni Usercreationform,tj, username filed sa incijalnim podacima
			form = UserCreationForm(initial = {"username" : request.POST["WelcomeEmail"]})
			return render(request, "SignUp.html", {
					"form":form,
					"Title":Title,
				})
		else:
			return super(SignUp, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    settings = Settings.objects.get(id = 1)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = settings.siteName
	    return context


