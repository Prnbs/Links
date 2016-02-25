from django.shortcuts import render
from tagged_links.models import User, URL, Tags
from django.contrib.auth.decorators import login_required


@login_required
def get_my_saved_links(request):
    errors = []
    print("*"*10)
    print(request.user.email)
    print("*"*10)
    if request.user.is_authenticated():
        users = User.objects.get(email=request.user.email)
        print(users)
        urls = users.url.all()
        print(urls)
        urls_and_tags = []
        for url in urls:
            my_urls_tagged = {}
            my_urls_tagged['url'] = url.url
            tags = url.tags.all()
            this_urls_tags = []
            for tag in tags:
                this_urls_tags.append(tag)
            my_urls_tagged['tags'] = this_urls_tags
            urls_and_tags.append(my_urls_tagged)
        return render(request, 'search_form.html', {'tags_and_urls': urls_and_tags})


@login_required
def get_all_tags_for_url(request):
    errors = []
    if 'link' in request.GET:
        url = request.GET['link']
        if not url:
            errors.append('Enter an url')
            return render(request, 'search_links.html', {'errors':errors})
        else:
            urls = URL.objects.filter(url=url)
            unique_tags = set()
            for url in urls:
                tags = url.tags.all()
                for tag in tags:
                    unique_tags.add(tag)
            return render(request, 'search_links.html', {'unique_tags':unique_tags})
    else:
        return render(request, 'search_links.html')


@login_required
def get_urls_for_tag(request):
    errors = []
    if 'email' in request.GET:
        if 'tag' in request.GET:
            mail_id = request.GET['email']
            input_tag = request.GET['tag']
            if not mail_id or not input_tag:
                errors.append("Both fields are required")
                return render(request, 'search_tag.html', {'errors':errors})
            else:
                user = User.objects.get(email=mail_id)
                urls = user.url.all()
                tagged_urls = set()
                for url in urls:
                    tags = url.tags.all()
                    for tag in tags:
                        if str(tag) == input_tag:
                            tagged_urls.add(url)
                return render(request, 'search_tag.html', {'tagged_url':tagged_urls})
        else:
            errors.append("Both fields are required")
            return render(request, 'search_tag.html', {'errors':errors})
    else:
        return render(request, 'search_tag.html')



