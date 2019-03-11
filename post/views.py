from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# İçinde python fonsiyonları yazacağımız yerdir. Web de herhangi bir sayfayı görüntüleyebilmek için o sayfanın view i olması gerekiyor 
# ( Ders 10 views ) viewwlere karşılık gelen bir url adresi olması gerekio.
# request sistemizi ziyaret eden kullanıcıların yaptığı isteği temsil ediyor. Kullanıcı istekleri ile ilgili bilgiler getiriyor. 
# Http Response metodu bunun için kullanılır

def post_index(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list=post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 5) # Show 25 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
   
    return render(request, 'post/index.html', {'posts':posts} )

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post' : post,
        'form': form,
    }
    return render (request, 'post/detail.html', context)

def post_create(request):

    if not request.user.is_authenticated():
        return Http404

    #if request.method == "POST":   Buradan forma girdiğimiz bilgileri komut ekranında görürüz. 
    #   print(request.POST)         Aşağıda ise bunları DB ye yazmak için komutlar var.

    #title = request.POST.get('title')       Bu genelde kullanılan bir yöntem olmadığı için yorum satırı yaptık.
    #content = request.POST.get('content')
    #Post.objects.create(title=title, content=content)

        # birinci alternatif 
    #if request.method == "POST":
        #Formdan gelen bilgileri kaydet. 
    #    form = PostForm(request.POST)
    #    if form.is_valid():
    #       form.save()
    #else:
        #Formu kullanıcıya göster
    #    form = PostForm()
         
    # ikinci alternatif
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Başarılı Bir şekilde oluşturdunuz')
        return HttpResponseRedirect(post.get_absolute_url())
    context={
        'form':form,
    }
    return render (request, 'post/form.html', context)

def post_update(request, slug):

    if not request.user.is_authenticated:
        return Http404

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,  request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save()
        messages.success(request, 'Başarılı Bir şekilde oluşturudunuz', extra_tags='mesaj başarılı')
        return HttpResponseRedirect(post.get_absolute_url())
    context={
        'form':form,
    }
    return render (request, 'post/form.html', context)

def post_delete(request, slug):

    if not request.user.is_authenticated():
        return Http404

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect ('post:index')

