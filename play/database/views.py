
from django.http import HttpResponse
from django.shortcuts import render


from .models import One, Three, Two
# Create your views here.

'''
def fn(request):
    # print(request.user)
    data = One.objects.filter(two_id=1)
    # lst_data = list(data)
    # print(type(lst_data))
    # print(len(lst_data))
    # print(lst_data[1])
    # print(lst_data)
    # print(type(lst_data[1]))
    # print(type(data.user_id))
    # print(data)
    if len(data) == 0:
        print("no")
    else:
        for i in data:
            print(i.name)

    return HttpResponse("ok")
'''

'''
def fn(request):
    # print(request.user)
    data = One.objects.get(id=1)
    print(data.two.place)

    return HttpResponse("ok")
'''


'''
def fn(request):
    # print(request.user)
    data = One.objects.filter(two__place="janksd")
    data2 = One.objects.filter(two__id=1)
    # print(data.two.place)
    print(data, data2)

    return HttpResponse("ok")
'''


'''
def fn(request):
    # print(request.user)
    # data = Three.objects.all()
    # data = Three.objects.get(id=1)
    data = Three.objects.filter(two__place="new place")
    print(data)

    return HttpResponse("ok")
'''

'''
def fn(request):
    # print(request.user)
    # two__id=1 and two__id=6
    # data = Three.objects.filter(two__id=1).filter(two__id=6)
    # data = Three.objects.filter(two__id=1).filter(two__id=2)
    data = Three.objects.filter(two__id=1).filter(two__id=3)
    print(data)

    return HttpResponse("ok")
'''

'''
def fn(request):
    # print(request.user)
    # two__id=1 and two__id=6
    # data = Three.objects.filter(two__id=1).filter(two__id=6)
    # data = Three.objects.filter(two__id=1).filter(two__id=2)
    data = Three.objects.filter(two__id=1).filter(two__id=3)
    print(data)

    return HttpResponse("ok")
'''

'''
def fn(request):
    obj = Two()
    obj.place = "check"
    obj.place_id = 20
    obj.save()
    print(obj)

    return HttpResponse("ok")
'''


'''
def fn(request):
    obj = Two.objects.get(id=7)
    obj.place = "newcheck"
    obj.place_id = 100
    obj.save()
    print(obj)

    return HttpResponse("ok")
'''


'''
def fn(request):
    obj = Two.objects.get(id=7)
    obj.place_id = 4
    obj.save()
    print(obj)

    return HttpResponse("ok")
'''


'''
def fn(request):
    obj = Two.objects.get_or_create(place="sss", place_id=4)
    print(obj)

    return HttpResponse("ok")
'''


def fn(request):

    return HttpResponse("ok")
