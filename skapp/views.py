from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
from .models import Sk
from .summakey import sk_wrapper, convert_markdown_to_html, extract_text_from_pdf
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

def index(request):
    sks = Sk.objects.order_by('-datetime')
    return render(request, 'blog/index.html', {'items':sks})

def write(request):
    if request.method == 'POST':
        fl = request.FILES['inputFile']
        print(fl)
        if fl:
            fp = os.path.join(settings.MEDIA_ROOT, 'input_files', fl.name)
            
            with open(fp, 'wb+') as fd:
                for chunk in fl.chunks():
                    fd.write(chunk)
            

            if os.path.splitext(fl.name)[1] =='.txt':
                fc = ''
                with open(fp, 'r', encoding='utf-8') as f:
                    fc = f.read()

            elif os.path.splitext(fl.name)[1] =='.pdf':
                fc = extract_text_from_pdf(fp)
            
            dif_outs = [0, 1]

            # sk = sk_wrapper(dif_outs, fc)

            with ProcessPoolExecutor() as executor:
                sk = list(executor.map(sk_wrapper, dif_outs, repeat(fc)))
            
            sk = {"summary": sk[0], "keytakeaways": sk[1]}
            
            print(sk)



            Sk.objects.create(
                summary = sk["summary"],
                keytakeaways = sk["keytakeaways"],
                filename = fp.replace("\\", "/").split("/")[-1],
                # varticle = varticle['varticle'],
                inputfile = fl
            )
            

            return JsonResponse({"summary": convert_markdown_to_html(sk["summary"]),
                                 "keytakeaways": convert_markdown_to_html(sk["keytakeaways"])}, safe=False)
        
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
    print(sk.summary)
    return render(request, 'blog/read.html', {'summary': convert_markdown_to_html(sk.summary), 
                                              'keytakeaways': convert_markdown_to_html(sk.keytakeaways),
                                              'title': sk.filename, 
                                              'datetime': sk.datetime})