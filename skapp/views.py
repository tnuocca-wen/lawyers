from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Sk
from .summakey import process, create_timeline, convert_markdown_to_html
from concurrent.futures import ProcessPoolExecutor
# from itertools import repeat
import os
from django.conf import settings

def history(request):
    sks = Sk.objects.order_by('-datetime')
    return render(request, 'blog/index.html', {'items':sks})

def write(request):
    if request.method == 'POST':

        print(request.FILES.getlist("inputFile"))
        allfiles = request.FILES.getlist("inputFile")
        # fl = request.FILES['inputFile']
        flist = []
        
        for fl in allfiles:
            fp = os.path.join(settings.MEDIA_ROOT, 'input_files', fl.name)
            flist.append(fp)    
            with open(fp, 'wb+') as fd:
                for chunk in fl.chunks():
                    fd.write(chunk)
        

        with ProcessPoolExecutor() as executor:
            tuplist = list(executor.map(process, flist))

        for item, inpfile in zip(tuplist, allfiles):
            Sk.objects.create(
                notes = item[1]["notes"],
                timeline = item[1]["timeline"],
                description = item[0],
                filename = item[2].split("/")[-1],
                inputfile = inpfile)
        
        # with ProcessPoolExecutor() as executor:
        #     sklist = list(executor.map(process, flist))

        sklist = [{item[2].split("/")[-1] : item[1]} for item in tuplist]
        
        notess = []
        timelines = []
        for sk_dict in sklist:
            # print(sk_dict)
            for key, sk in sk_dict.items():
                notess.append({key: [convert_markdown_to_html(sk["notes"]), sk["notes"]]})
                timelines.append(sk["timeline"])

        timeline = create_timeline(timelines)

        # print(notess)

        return JsonResponse({"notes": notess,
                            "timeline": [convert_markdown_to_html(timeline), timeline]}, safe=False)
        
        return render(request, 'blog/write.html', {'messages': 'File not acceptable.'})
    
    # if request.method == 'GET':
    #     publish = request.GET.get('publish', '')
    #     if publish:
    #         try:
    #             article = Sk.objects.get(slug=publish)
    #         except:
    #             article = None
            
    #         if article:
    #             article.publish = True
    #             article.save()
    #         return redirect('blog:index')

    return render(request, 'blog/write.html', {})

def read(request, slug):
    sk = get_object_or_404(Sk, sk_id=int(slug))
    print(sk)
    return render(request, 'blog/read.html', {'notes': convert_markdown_to_html(sk.notes),
                                              'timeline': convert_markdown_to_html(sk.timeline),
                                              'title': sk.filename, 
                                              'datetime': sk.datetime})