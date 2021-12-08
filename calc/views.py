import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from calc.digitizationAPIs import HSV_detection, image_detect

from django.conf import settings

from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': 'Ravi'})


# def add(request):
#    value1 = int(request.POST['num1'])
#    value2 = int(request.POST['num2'])
#    res = value1 + value2
#    return render(request, 'result.html', {'result': res})


def capture(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        result = image_detect('media')
        print(result)

        if result == 1:
            concentration = 10
        elif result == 2:
            concentration = 30
        elif result == 3:
            concentration = 50
        else:
            concentration = 60
        return render(request, 'home.html', {
            'uploaded_file_url': uploaded_file_url,
            'result': concentration
        })

    return render(request, 'home.html')


def remove(request):
    print("In remove!")
    directory = "media/"
    flag = 0
    if request.method == 'GET':
        print(os.listdir(directory))
        for file in os.listdir(directory):
            f = os.path.join(directory, file)
            if os.path.isfile(f):
                os.remove(f)
        flag = 1
        if flag == 1:
            return render(request, 'home.html', {
                'status': 'ok'
            })
        else:
            return render(request, 'home.html', {
                'status': 'not ok'
            })



