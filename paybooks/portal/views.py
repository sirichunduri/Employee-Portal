from django.shortcuts import render
import time
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.views import APIView
from .forms import *
from .models import *
from .signals import *
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .serializers import EmployeeSerializer,TimesheetSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return render(request, 'portal/home.html')


def report_data(request):
    user = request.user
    if request.method == 'POST':
        form = reportData(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                week_begining = datetime.date(
                    *time.strptime(str(data['year']) + '-0-' + str(data['week']), '%Y-%w-%U')[:3])
                week_ending = week_begining + datetime.timedelta(days=7)
            except ValueError:
                raise Http404
            queryset = Timesheet.objects.filter(employee=user, date__gte=week_begining, date__lt=week_ending).order_by(
                'date',
                'time')
            timesheet = []
            week_hours = 0
            date = week_begining
            while date <= week_ending:
                date_queryset = queryset.filter(date=date)
                for i in date_queryset:
                    timesheet += [{
                        'date': date,
                        'jobs': i.job,
                        'hours': i.hours,
                    }, ]
                    week_hours += i.hours
                date = date + datetime.timedelta(days=1)
            context = {
                'week_begining': week_begining,
                'week_ending': week_ending,
                'week_hours': week_hours
            }
            return JsonResponse({'error': False, 'context': context, 'timesheet': timesheet})

    else:
        form = reportData()
    return render(request, 'portal/report_data.html', {'form': form})


def get_data(request):
    if request.method == 'POST':
        form = add_data(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            get_user = User.objects.get(username=request.user)
            try:
                user_data = Timesheet.objects.get(employee_id=get_user, date=data['date'])
                if user_data.job == "Leave":
                    return JsonResponse({'data': 'Cancel Leave to insert data!!'}, )
                else:
                    user_data.job = data['job']
                    user_data.hours = data['hours']
                    user_data.save()
            except:
                a = Timesheet(**data)
                a.employee = request.user
                a.save()
            return JsonResponse({'error': False, 'data': 'Data Inserted!!'}, )
    else:
        form = add_data()
    return render(request, 'portal/add_data.html', {'form': form})


def post_name(request):
    user_obj = User.objects.get(id=request.user.id)
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    if first_name and last_name:
        name = first_name + ' ' + last_name
    else:
        name = request.user

    if request.method == 'POST':
        form = addName(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name_obj = User.objects.get(id=request.user.id)
            name_obj.first_name = data['First_name']
            name_obj.last_name = data['Last_name']
            name_obj.save()
            name = data['First_name'] + ' ' + data['Last_name']
            return JsonResponse({'error': False, 'name': name}, )
    else:
        form = addName()
        return render(request, 'portal/full_name.html', {'form': form, 'name': name})


def jobtitle(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = jobTitle(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                obj = JobTitle(**data)
                obj.save()
                return JsonResponse({'error': False, 'data': "Title inserted"}, )
        else:
            form = jobTitle()
            return render(request, 'portal/jobtitle.html', {'form': form})
    else:
        return HttpResponse('401 Unauthorized', status=401)


def applyLeave(request, action=None):
    get_user = User.objects.get(username=request.user)
    if request.method == 'POST' and action == "apply":
        form = apply_leave(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['From_Date'] <= data['To_Date']:
                start = data['From_Date']
                while start <= data['To_Date']:
                    try:
                        user_data = Timesheet.objects.get(employee_id=get_user, date=start)
                        user_data.job = "Leave"
                        user_data.hours = 9
                        user_data.save()
                    except:
                        obj = Timesheet(employee=request.user, date=start, job="Leave", hours=9)
                        obj.save()
                    start = start + datetime.timedelta(days=1)
            leave_signal.send(sender=request.user, apply='applied', from_date=str(data['From_Date']),
                              to_date=str(data['To_Date']))
            return JsonResponse({'data': 'Request Registered!!'})
        else:
            return JsonResponse({'data': 'Please enter valid input!!'})
    elif request.method == 'POST' and action == "cancel":
        form = apply_leave(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['From_Date'] <= data['To_Date']:
                start = data['From_Date']
                while start <= data['To_Date']:
                    try:
                        user_data = Timesheet.objects.get(employee_id=get_user, date=start, job='Leave')
                    except:
                        return JsonResponse({'data': 'No leave records available for one or more days in provided input'})
                    start = start + datetime.timedelta(days=1)
                start = data['From_Date']
                while start <= data['To_Date']:
                    user_data = Timesheet.objects.get(employee_id=get_user, date=start, job='Leave')
                    user_data.job = "Cancelled Leave"
                    user_data.hours = 0
                    user_data.save()
                    start = start + datetime.timedelta(days=1)
            leave_signal.send(sender=request.user, apply='cancelled', from_date=str(data['From_Date']),
                              to_date=str(data['To_Date']))
            return JsonResponse({'data': 'Request Registered!!'})
        else:
            return JsonResponse({'data': 'Please enter valid input!!'})
    else:
        form = apply_leave()
        return render(request, 'portal/apply_leave.html', {'form': form})


def approveleave(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            approve = request.POST.getlist('approve')
            for i in approve:
                data = Timesheet.objects.get(id=i)
                data.is_approved = True
                data.save()
            return JsonResponse({'data': "Approved Leave"}, )
        else:
            object_list = Timesheet.objects.filter(job='Leave',is_approved=False).values_list('id','date',
                                                                                              'employee_id__username')
            context = {
                'object_list': object_list,
            }
            return render(request, 'portal/approve_leave.html', context,)
    else:
        return HttpResponse('401 Unauthorized', status=401)


class EmployeeListView(generics.GenericAPIView,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    serializer_class = TimesheetSerializer
    queryset = Timesheet.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id)
        return self.list(request)

    def post(self,request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    def put(self, request, id=None):
        return self.create(request,id)

    def perform_update(self,serializer):
        serializer.save(created_by=self.request.user)

    def delete(self,request,id=None):
        return self.destroy(request,id)



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeAPIView(APIView):
    def get(self,request):
        q = Timesheet.objects.all()
        serialized = TimesheetSerializer(q, many=True)
        return Response(serialized.data, status=200)
    def post(self,request):
        data = request.data
        serializer = TimesheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EmployeeDetailView(APIView):
    def get_object(self,id):
        try:
            return Timesheet.objects.get(id=id)
        except Timesheet.DoesNotExist as e:
            return Response({"error": "Given timesheet object not found"}, status=404)
    def get(self,request,id=None):
        instance = self.get_object(id)
        serialized = TimesheetSerializer(instance)
        return Response(serialized.data)
    def put(self,request,id=None):
        instance = self.get_object(id)
        serialized = TimesheetSerializer(instance)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=200)
        return Response(serialized.errors, status=400)
    def delete(self,request,id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)

@csrf_exempt
def timesheet_api(request):
    if request.method == "GET":
        q=Timesheet.objects.all()
        serialized = TimesheetSerializer(q,many=True)
        return JsonResponse(serialized.data,safe=False)
    elif request.method == "POST":
        obj_parser=JSONParser()
        data = obj_parser.parse(request)
        serializer =TimesheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def timesheet_details(request,id):
    try:
        instance = Timesheet.objects.get(id=id)
    except Timesheet.DoesNotExist as e:
        return JsonResponse({"error":"Given timesheet object not found"},status=404)

    if request.method == "GET":
        serialized = TimesheetSerializer(instance)
        return JsonResponse(serialized.data)
    elif request.method == "POST":
        obj_parser=JSONParser()
        data = obj_parser.parse(request)
        serializer =TimesheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    elif request.method == "PUT":
        obj_parser = JSONParser()
        data = obj_parser.parse(request)
        serializer = TimesheetSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse(status=204)

class LoginView(views.APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response(status=204)
