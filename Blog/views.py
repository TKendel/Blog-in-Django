from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.utils.text import slugify
from django.forms import Textarea
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #provjerava dali je user logiran prije nego sto pokrene view
from django.contrib.auth.models import User
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import FormView,CreateView,UpdateView,DeleteView

from .models import Post,Category,Tag,Settings,Profile,Comment
from .forms import PostForm,CategoryForm,TagForm,SettingsForm,UserForm,CommentForm


#----POST----
def ShowPosts(request):

	allPosts = Post.objects.all()
	return render(request, "Blog/Post/ShowPosts.html", {"allPosts":allPosts})

class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = "Blog/Post/CreatePost.html"
	
	#ovo napravi prije nego sto saveas
	def form_valid(self, form):
		# pospremi u Post.slug title koji ti je trenutno u formi
		form.instance.slug = slugify(form.instance.title)
		#uzmi id trenutnog logiranog usera
		user_id = self.request.user.id
		#dohavti querryset trenutno logirano usera
		user = User.objects.get(id = user_id )
		#savaj querry set u user filed od post modela( treba biti objekt a ne samo id )
		form.instance.user = user
		#save
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    settings = Settings.objects.get(id = 1)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = settings.siteName
	    return context

class UpdatePost(UpdateView):
	model = Post
	form_class = PostForm
	template_name = "Blog/Post/EditPost.html"
	
	#ovo napravi prije nego sto saveas
	def form_valid(self, form):
		#tu pospremi u Post.slug title koji ti je tretno u formi
		form.instance.slug = slugify(form.instance.title)
		#save
		return super().form_valid(form)

	#get context data se izvrsava poslje get/post pa zato mozemo korstiti objekte iz requesta
	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = self.object.title
	    return context

class DeletePost(DeleteView):
	model = Post
	success_url = reverse_lazy("Posts:Welcome")
	template_name = "Blog/Post/DeletePost.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    return context
	#nauči kak post radi-----------------------------------
	def post(self, request, *args, **kwargs):
		#ako je Cancle u postu koju smo poslali(Cancle je ime buttona inputa)
		if "Cancel" in request.POST:
			#vrati natrag
			#get_object pretrazuje url kwargove za id
			PostID = self.get_object().id
			return redirect("Posts:Single", pk = PostID)
		else:
			#inace pokreni ispocetka deletePost clasu
			return super(DeletePost, self).post(request, *args, **kwargs)

#----COMMENT SECTION----
def AddComment(request,pk):
	post = Post.objects.get(pk = pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.post = post
			comment.save()
			return redirect("Posts:Single", pk = post.pk)
	else:
		form = CommentForm()
	return render(request, 'Blog/Comments/index.html', { "form":form })

@login_required
def CommentApprove(request,pk):
	comment = Comment.objects.get(pk = pk)
	comment.approved()
	return redirect("Posts:Single", pk = comment.post.pk)

@login_required
def CommentRemove(request,pk):
	comment = Comment.objects.get(pk = pk)
	comment.delete()
	return redirect("Posts:Single", pk = comment.post.pk)


#----CATEGORY----
def ShowCategories(request):
	allCategories = Category.objects.all()
	settings = Settings.objects.get( id = 1 )
	Title = settings.siteName
	return render(request, "Blog/Category/ShowCategories.html", 
		{
			"allCategories":allCategories,
			"Settings":settings,
			"Title":Title,
		})

class CategoryCreate(LoginRequiredMixin, CreateView):
	model = Category
	form_class = CategoryForm
	template_name = "Blog/Category/CreateEditCategory.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    settings = Settings.objects.get(id = 1)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = settings.siteName
	    return context

class UpdateCategory(UpdateView):
	model = Category
	form_class = CategoryForm
	template_name = "Blog/Category/CreateEditCategory.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    context['Title'] = self.object.name
	    return context

class DeleteCategory(DeleteView):
	model = Category
	success_url = reverse_lazy("Posts:ShowCategories")
	template_name = "Blog/Category/DeleteCategory.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = self.object.name
	    return context

	def post(self, request, *args, **kwargs):
		#ako je Cancle u postu koju smo poslali(Cancle je ime buttona inputa)
		if "Cancel" in request.POST:
			#vrati natrag
			return HttpResponseRedirect("/blog/ShowCategories/")
		else:
			#inace pokreni ispocetka deletePost clasu
			return super(DeleteCategory, self).post(request, *args, **kwargs)


#----TAGS----
def ShowTags(request):
	settings = Settings.objects.get( id = 1 )
	Title = settings.siteName
	allTags = Tag.objects.all()
	return render(request, "Blog/Tag/ShowTags.html", 
		{
			"allTags" : allTags,
			"Settings":settings,
			"Title":Title,
		})

class CreateTag(LoginRequiredMixin, CreateView):
	model = Tag
	form_class = TagForm
	template_name = "Blog/Tag/CreateEditTag.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    settings = Settings.objects.get(id = 1)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = settings.siteName
	    return context

class UpdateTag(UpdateView):
	model = Tag
	form_class = TagForm
	template_name = "Blog/Category/CreateEditCategory.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    context['Title'] = self.object.name
	    return context

class DeleteTag(DeleteView):
	model = Tag
	success_url = reverse_lazy("Posts:ShowTags")
	template_name = "Blog/Tag/DeleteTag.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = self.object.name
	    return context

	def post(self, request, *args, **kwargs):
		#ako je Cancle u postu koju smo poslali(Cancle je ime buttona inputa)
		if "Cancel" in request.POST:
			#vrati natrag
			return HttpResponseRedirect("/blog/ShowTags/")
		else:
			#inace pokreni ispocetka deletePost clasu
			return super(DeleteTag, self).post(request, *args, **kwargs)


#----SETTINGS----
class SiteSettings(LoginRequiredMixin, UpdateView):
	model = Settings
	form_class = SettingsForm
	template_name = "Blog/Settings/index.html"

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['Settings'] = Settings.objects.get(id = 1)
	    #ovako izvuces trenutni objekt koji se editira
	    context['Title'] = self.object.siteName
	    return context

			

#----USERS----
def UserPage(request):
	settings = Settings.objects.get(id = 1)
	Title = settings.siteName
	allUsers = User.objects.all() #User je djangov User model
	regUser = request.user

	return render(request, "Blog/User/index.html", 
		{
			"allUsers":allUsers, 
			"current_user":regUser,
			"Settings":settings,
			"Title":Title
		})

def MakeAdmin(request,pk):
	user = User.objects.get(id = pk)
	if request.user.is_staff == 1 and user.is_staff == True:
		user.is_staff = False
		user.save()
		return HttpResponseRedirect("/blog/UserPage/")
	elif request.user.is_staff == 1 and user.is_staff == False:
		user.is_staff = True
		user.save()
		return HttpResponseRedirect("/blog/UserPage/")
	else:
		raise PermissionDenied

def DeactivateUser(request,pk):
	user = User.objects.get(id = pk)
	if request.user.is_staff == 1 and user.is_active == True:
		user.is_active = False
		user.save()
		return HttpResponseRedirect("/blog/UserPage/")
	elif request.user.is_staff == 1 and user.is_active == False:
		user.is_active = True
		user.save()
		return HttpResponseRedirect("/blog/UserPage/")
	else:
		raise PermissionDenied

@login_required
def ProfileSettings(request,pk):
	settings = Settings.objects.get(id = 1)
	Title = settings.siteName

	user = User.objects.get(pk = pk) #daj mi usera sa tim id-om
	user_form = UserForm(instance = user)#popuni UserForm sa podacima iz var user
	#PROUCI INLINEFORMSET
	#inlineformset nam omogucuje editranje dvaju modela odjednom. U ovom slucaju uzimamo 
	#user model i na njega spajamo profile model sa odredenim fieldovima i stvaramo jednu formu 
	ProfileUserFormset = inlineformset_factory(User, Profile, fields = ("about","link","avatar"))
	formset = ProfileUserFormset(instance = user) #popuni formu napravljenu od user i profile modela sa user podacima
	# ako je user logiran i ako je trenutno logiran user id jednak sa userprofile id-om
	if request.user.id == user.id and request.user.is_authenticated:
		if request.method == "POST":
			#popunimo oboje forme sa POST podacima
			user_form = UserForm(request.POST, request.FILES, instance = user)
			formset = ProfileUserFormset(request.POST, request.FILES, instance = user)
			#posto zapravo radimo sa dvije forme onda i radimo validaciju na oboje njih
			if user_form.is_valid():
				created_user = user_form.save(commit = False)# posto nam jos trebaju user podaci za profile onda ih jos ne savamo
				formset = ProfileUserFormset(request.POST, request.FILES, instance = created_user)

				if formset.is_valid():
					created_user.save()
					formset.save()
					return HttpResponseRedirect("/blog/Welcome/")
		# ako user oce popuniti svoj profil renderja template sa napravljenim dictonarijom
		# dictonary se satoji od user forma(user model fielodvi) i fromseta koji je zapravo profile model
		return render(request, "Blog/Profile/index.html", 
			{
				"user":pk, 
				"user_form":user_form,
				"formset":formset,
				"Settings":settings,
				"Title":Title,
			})		
	else:
		raise PermissionDenied


#----WELCOME PAGE----
def Welcome(request):
	user = request.user
	categories = Category.objects.all()
	settings = Settings.objects.get(id = 1)
	title = settings.siteName
	latestPost = Post.objects.latest("created_at")# izabere zadnji napravljeni entry po danom fieldu
	allPosts = Post.objects.all()[:4]
	ProgramingCategoryID = Category.objects.get(id = 2)
	ProgramingCategory = ProgramingCategoryID.post_set.all()[:4]
	StylingCategoryID = Category.objects.get(id = 3)
	StylingCategory = StylingCategoryID.post_set.all()[:4]
	SecondLatestPostID = Post.objects.all().order_by("created_at")
	SecondLatestPost = SecondLatestPostID[2]

	return render(request, "Blog/Welcome.html", 
		{
			"User":user,
			"Categories":categories,
			"Settings":settings,
			"latestPost":latestPost,
			"SecondLatestPost":SecondLatestPost,
			"allPosts":allPosts,
			"ProgramingCategory":ProgramingCategory,
			"StylingCategory":StylingCategory,
			"ProgramingCategoryID":ProgramingCategoryID,
			"StylingCategoryID":StylingCategoryID,
			"Title":title,
		})

#----SINGLE PAGE----
def Single(request,pk):
	user = request.user
	tags = Tag.objects.all()
	post = Post.objects.get(id = pk)
	title = post.title
	settings = Settings.objects.get(id = 1)


	return render(request, "Blog/Single.html", 
		{
			"User":user,
			"Tags":tags,
			"Post":post,
			"Title":title,
			"Settings":settings,
		})

def CategoryPage(request,pk):
	category = Category.objects.get(id = pk)
	Title = category.name
	settings = Settings.objects.get(id = 1)


	return render(request, "Blog/Category.html", 
		{
			"Category":category,
			"Title":Title,
			"Settings":settings,
		})

def TagPage(request,pk):
	tag = Tag.objects.get(id = pk)
	Title = tag.name
	settings = Settings.objects.get(id = 1)
	

	return render(request, "Blog/Tag.html", 
		{
			"Tag":tag,
			"Title":Title,
			"Settings":settings,
		})


#----SEARCH----
def Search(request):
	settings = Settings.objects.get(id = 1)
	title = settings.siteName

	if request.method == "GET":
		searchQuerry = request.GET.get('Querry')#ovako izvlacimo iz search forme input pod imenom Querry
		#zatim pretrazujemo Post DB gdje filtriramo titlove Postova na nacin da provjeravamo dali sadrze Querry koji smo unjeli
		SearchResults = Post.objects.filter(title__icontains = searchQuerry)

		return render(request, "Blog/Search.html", 
			{
				"Search":SearchResults,
				"SearchQuerry":searchQuerry,
				"Settings":settings,
				"Title":title,
			})



########################TEST##############################

def test2(request):
	return render(request, "Blog/test.html")


"""class PostDetail(DetailView):
	template_name = "Blog/Post/test.html"
	model = Post
	context_object_name = "Posts"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["post_list"] = Post.objects.all()
		return context"""

class PostDetail(DetailView):
	template_name = "Blog/Post/test.html"
	queryset = Post.objects.all()
	context_object_name = "detail"

	def get_object(self):
		#get_object, ako je zadan queryset, ce pogledat pk argument url da
		#pretrazi queryset prema njemu
		obj = super().get_object()
		return obj.title


class test(ListView):
	"""#bazu podataka koju koristimo
	model = Post
	#uzmi sve postove cije ime categorije je New
	queryset = Post.objects.filter(category__name = "New") """
	#ime template kojeg koristimo
	template_name = "Blog/Post/test.html" 
	#ime var u koju spremamo objekte modela i slajemo u template
	context_object_name = "Posts" 

	def get_queryset(self):

		self.category = get_object_or_404(Category, name = self.kwargs['category'])
		return Post.objects.filter(category = self.category)

	def get_context_data(self, **kwargs):
	    # prvo napravi context(dictonary) sa pozvimo base get_context
	    context = super().get_context_data(**kwargs)
	    # zatim u njega dodaj kljuc(var)
	    context['category'] = self.category
	    return context