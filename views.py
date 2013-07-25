###########
# Blog v2
# copyright 2010, Modular Programming Systems Inc
# released as GPL3
#
###########

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from intf.blog.models import Post, Comment, Tag, Category
import re
from time import strftime, strptime

@login_required
def index(request):
    data=Post.objects.filter(viewable='True').order_by('-date').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
    tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
    archive=Post.objects.dates('date','month', order='DESC')
    categories=Category.objects.all().order_by('category')
    index="x"
    nextpage=""
    if len(data)>10:
        nextpage=10
        data=data[:nextpage]
    postcategory=request.POST.get('category','')
    posttitle=request.POST.get('title','')
    postcontent=request.POST.get('postcontent','')
    posttag=request.POST.get('posttag','')
    if posttitle and postcontent:
        postcategorynumber=str(Category.objects.filter(category=postcategory).values("id"))
        Post.objects.create(category=postcategorynumber, title=posttitle, content=postcontent).save()
        return HttpResponseRedirect('/')
    searchterm=request.POST.get('search','')
    tagterm=request.POST.get('tagterm','')
    archiveterm=request.POST.get('archiveterm','')

    if tagterm:
        return HttpResponseRedirect('/tag/'+tagterm)
    if archiveterm:
        return HttpResponseRedirect('/archive/'+archiveterm)
    if searchterm:
        searchtitle,searchtext=searchquery(searchterm)
        return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
    else:
        return render_to_response('blogdetail.html', {'index': index, 'categories': categories, 'data': data, 'nextpage': nextpage, 'tags': tags, 'archive': archive})


@login_required
def archive(request,month):
    month=strftime("%Y-%m", strptime(month,"%B-%Y"))
    monthsplit=month.split("-")
    month+="-01 00:00"
    if monthsplit[1]=="12":
        nextmonth=str(int(monthsplit[0])+1)+"-01-01 00:00"
    if monthsplit[1]=="09" or monthsplit[1]=="10" or monthsplit[1]=="11":
        nextmonth=monthsplit[0]+"-"+str(int(monthsplit[1])+1)+"-01 00:00"
    if int(monthsplit[1])<9:
        nextmonth=monthsplit[0]+"-0"+str(int(monthsplit[1])+1)+"-01 00:00"
        data=Post.objects.filter(date__gte=month, date__lt=nextmonth).order_by('-date').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
        tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
        archive=Post.objects.dates('date','month', order='DESC')
        categories=Category.objects.all().order_by('category')
        searchterm=request.POST.get('search','')
        tagterm=request.POST.get('tagterm','')
        archiveterm=request.POST.get('archiveterm','')

        if tagterm:
            return HttpResponseRedirect('/tag/'+tagterm)
        if archiveterm:
            return HttpResponseRedirect('/archive/'+archiveterm)
        if searchterm:
            searchtitle,searchtext=searchquery(searchterm)
            return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
        else:
            return render_to_response('blogdetail.html', {'data': data, 'categories': categories, 'tags': tags, 'archive': archive})


@login_required
def category(request,category):
    category=re.sub("-"," ",category)
    data=Post.objects.filter(viewable='True', category__category=category).order_by('-date').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
    tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
    archive=Post.objects.dates('date','month', order='DESC')
    categories=Category.objects.all().order_by('category')
    searchterm=request.POST.get('search','')
    tagterm=request.POST.get('tagterm','')
    archiveterm=request.POST.get('archiveterm','')

    if tagterm:
        return HttpResponseRedirect('/tag/'+tagterm)
    if archiveterm:
        return HttpResponseRedirect('/archive/'+archiveterm)
    if searchterm:
        searchtitle,searchtext=searchquery(searchterm)
        return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
    else:   
        return render_to_response('blogdetail.html', {'data': data, 'categories': categories, 'tags': tags, 'archive': archive})

    
@login_required
def page(request,pagecount):
    data=Post.objects.filter(viewable='True').order_by('-date').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
    tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
    archive=Post.objects.dates('date','month', order='DESC')
    categories=Category.objects.all().order_by('category')
    pagecount=int(pagecount)
    nextpage=pagecount+10
    if len(data) < nextpage+1:
        nextpage=""
    data=data[pagecount:pagecount+10]
    searchterm=request.POST.get('search','')
    tagterm=request.POST.get('tagterm','')
    archiveterm=request.POST.get('archiveterm','')

    if tagterm:
        return HttpResponseRedirect('/tag/'+tagterm)
    if archiveterm:
        return HttpResponseRedirect('/archive/'+archiveterm)
    if searchterm:
        searchtitle,searchtext=searchquery(searchterm)
        return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
    else:   
        return render_to_response('blogdetail.html', {'data': data, 'categories': categories, 'nextpage': nextpage, 'tags': tags, 'archive': archive})

@login_required
def posting(request,title):
    post="x"
    comments=[]
    data=Post.objects.filter(slug=title)
    if not data:
        return render_to_response('404.html',)
    data2=Post.objects.filter(slug=title).values()
    for item in data2:
        comments=Comment.objects.filter(title__title=item["title"]).order_by('date')
        commenttitleid=item["id"]
        tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
        archive=Post.objects.dates('date','month', order='DESC')
        categories=Category.objects.all().order_by('category')
        content=request.POST.get('postcontent','')
        content=re.sub("<a href=.*?</a>","",content)
        content=re.sub("<\?","",content)

        if content:
            Comment.objects.create(title_id=commenttitleid, content=content).save()

        searchterm=request.POST.get('search','')
        tagterm=request.POST.get('tagterm','')
        archiveterm=request.POST.get('archiveterm','')

        if tagterm:
            return HttpResponseRedirect('/tag/'+tagterm)
        if archiveterm:
            return HttpResponseRedirect('/archive/'+archiveterm)
        if searchterm:   
            searchtitle,searchtext=searchquery(searchterm)
            return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
        else:
            return render_to_response('blogdetail.html', {'data': data, 'categories': categories, 'post': post, 'comments': comments, 'tags': tags, 'archive': archive})


@login_required
def random(request):
        data=Post.objects.filter(viewable='True').order_by('?').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
        tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
        archive=Post.objects.dates('date','month', order='DESC')
        categories=Category.objects.all().order_by('category')
        data=data[:10]
        searchterm=request.POST.get('search','')
        if searchterm:
            searchtitle,searchtext=searchquery(searchterm)
            return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
        else:
            return render_to_response('blogdetail.html', {'categories': categories, 'data': data, 'tags': tags, 'archive': archive})

def searchquery(searchterm):
    searchterm=re.sub("[^A-Za-z 0-9]","",searchterm)
    searchtitle=Post.objects.filter(viewable='True', title__icontains=searchterm).order_by('-date')
    searchtext=Post.objects.filter(viewable='True', content__icontains=searchterm).order_by('-date')
    return searchtitle,searchtext

@login_required
def tag(request,tag):
    tag=re.sub("-"," ",tag)
    data=Post.objects.filter(viewable='True', tags__tag=tag).order_by('-date').extra(select={'commentcount':'select count(blog_comment.id) from blog_comment where blog_comment.title_id=blog_post.id'},)
    tags=Tag.objects.all().order_by('tag').extra(select={'tagcount':'select count(blog_post_tags.post_id) from blog_post_tags where blog_tag.id=blog_post_tags.tag_id group by blog_post_tags.tag_id'},)
    archive=Post.objects.dates('date','month', order='DESC')
    categories=Category.objects.all().order_by('category')
    searchterm=request.POST.get('search','')
    tagterm=request.POST.get('tagterm','')
    archiveterm=request.POST.get('archiveterm','')

    if tagterm:
        return HttpResponseRedirect('/tag/'+tagterm)
    if archiveterm:
        return HttpResponseRedirect('/archive/'+archiveterm)
    if searchterm:
        searchtitle,searchtext=searchquery(searchterm)
        return render_to_response('blogdetail.html', {'searchtitle': searchtitle, 'searchtext': searchtext, 'categories': categories, 'tags': tags, 'archive': archive})
    else:
        return render_to_response('blogdetail.html', {'data': data, 'categories': categories, 'tags': tags, 'archive': archive})
