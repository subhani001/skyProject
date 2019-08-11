from django.shortcuts import render
from datetime import datetime,timedelta
from skyTestApp.models import Tasks
from skyTestApp.authentications import CustomAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User, Group

# Create your views here.

def taskdata(request):
    """
    This function returns all records from Tasks model/table
    """
    # Tasks in an order from top to down . i.e. in descending order of id.
    for i in range(Tasks.objects.all().count(),0,-1):
        maintask=Tasks.objects.get(id=i)               # Maintask record
        subtasks=Tasks.objects.filter(parent__exact=i) # subtasks for the respective maintask
        subtask_cnt=subtasks.count()                   # Count of sub tasks for a given main task
        print('maintask.id',maintask.id)
        print('subtask_cnt',subtask_cnt)



        maintask.status="Idle"                        # Default Status
        maintask.net_duration=0
        maintask.duration=0

        if subtask_cnt== 0:  # that means if the task has no sub sub tasks
            start_date_object=datetime.strptime(maintask.start_date,"%Y-%m-%dT%H:%M:%SZ")
            end_date_object=datetime.strptime(maintask.end_date,"%Y-%m-%dT%H:%M:%SZ")

            if start_date_object>datetime.now():
                maintask.status="Scheduled"             # Scheduled if the start timestamp is in future.
            elif start_date_object <= datetime.now() and end_date_object >= datetime.now():
                maintask.status="Running"               # Running if the current time is between start time and end time.
            elif end_date_object < datetime.now():
                maintask.status="Complete"              # Complete if the end time has passed.

            # Finding... duration = maintask.end_date-maintask.start_date
            maintask.duration=str(int((datetime.strptime(maintask.end_date,"%Y-%m-%dT%H:%M:%SZ")-datetime.strptime(maintask.start_date,"%Y-%m-%dT%H:%M:%SZ")).total_seconds()/60))

            # Finding...net task duration time=end_date - start_date - idle time)
            if maintask.status=="Idle":
                maintask.net_duration=0
            else:
                maintask.net_duration=maintask.duration

            maintask.save()   # Save the updates

        else:         	# that means the task has some sub tasks

            complete_count=0
            running_count=0
            scheduled_count=0

            running_count=Tasks.objects.filter(parent__exact=i,status__icontains='Running').count()
            complete_count=Tasks.objects.filter(parent__exact=i,status__icontains='Complete').count()
            scheduled_count=Tasks.objects.filter(parent__exact=i,status__icontains='Scheduled').count()

            # Scheduled if none of the sub-tasks have started yet.
            if running_count==0 and complete_count==0:
                maintask.status="Scheduled"

            # Running if one of the child task is running
            if running_count==1:
                maintask.status="Running"

            # Multi-Runs if more than one child is running.
            if running_count >1:
                maintask.status="Multi-Runs"

            print('maintask.end_date',maintask.end_date)
            print('type((maintask.end_date)',type(maintask.end_date))

            print('maintask.end_date',maintask.end_date)
            print('type((maintask.end_date)',type(maintask.end_date))


            # 	Start timestamp: in case of a parent task this should be the least of all the child tasks’ start dates and calculated automatically.
            # 	Endtimestamp: in case of a parent task this should be the highest of the child tasks’ start dates and calculated automatically.
            start_date_list=[]
            end_date_list=[]
            for subtask in list(Tasks.objects.filter(parent__exact=i).values()):
                start_date_list.append(datetime.strptime(subtask["start_date"],"%Y-%m-%dT%H:%M:%SZ"))
                end_date_list.append(datetime.strptime(subtask["end_date"],"%Y-%m-%dT%H:%M:%SZ"))

            maintask.start_date=datetime.strftime(min(start_date_list),"%Y-%m-%dT%H:%M:%SZ")
            maintask.end_date=datetime.strftime(max(end_date_list),"%Y-%m-%dT%H:%M:%SZ")

            # Finding task duration time (end_date - start_date)
            maintask.duration=str(int((datetime.strptime(maintask.end_date,"%Y-%m-%dT%H:%M:%SZ")-datetime.strptime(maintask.start_date,"%Y-%m-%dT%H:%M:%SZ")).total_seconds()/60))

            # Finding  net task duration time (end_date - start_date - idle time)
            if maintask.status=="Idle":
                maintask.net_duration=0
            else:
                maintask.net_duration=maintask.duration
            maintask.save()
    my_dict={'task_list':Tasks.objects.all()}
    return render(request, 'skyTestApp/tasks.html', context=my_dict)

# To add test records
def addrecords(request):
    Tasks.objects.bulk_create([
    Tasks(id=1,name='Task A', status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T09:55:17Z',parent=0,duration=0,net_duration=0),
    Tasks(id=2,name='Task A.1',  status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-09-02T10:55:17Z',parent=1,duration=0,net_duration=0),
    Tasks(id=3,name='Task A.2',  status='Idle',start_date='2019-09-02T09:55:17Z',end_date='2019-09-03T10:55:17Z',parent=1,duration=0,net_duration=0),
    Tasks(id=4,name='Task B',    status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T09:55:17Z',parent=0,duration=0,net_duration=0),
    Tasks(id=5,name='Task B.1',  status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T09:55:17Z',parent=4,duration=0,net_duration=0),
    Tasks(id=6,name='Task B.1.1',status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T10:55:17Z',parent=5,duration=0,net_duration=0),
    Tasks(id=7,name='Task B.1.2',status='Idle',start_date='2019-09-02T09:55:17Z',end_date='2019-10-02T10:55:17Z',parent=5,duration=0,net_duration=0),
    Tasks(id=8,name='Task B.2',  status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T10:55:17Z',parent=4,duration=0,net_duration=0),
    Tasks(id=9,name='Task C',    status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T10:55:17Z',parent=0,duration=0,net_duration=0),
    Tasks(id=10,name='Task D',   status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-02T09:55:17Z',parent=0,duration=0,net_duration=0),
    Tasks(id=11,name='Task D.1', status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-09-02T10:55:17Z',parent=10,duration=0,net_duration=0),
    Tasks(id=12,name='Task D.2', status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-09-04T10:55:17Z',parent=10,duration=0,net_duration=0),
    Tasks(id=13,name='Task D.3', status='Idle',start_date='2019-09-02T09:55:17Z',end_date='2019-11-02T10:55:17Z',parent=10,duration=0,net_duration=0),
    Tasks(id=14,name='Task D.3', status='Idle',start_date='2019-07-02T09:55:17Z',end_date='2019-07-10T10:55:17Z',parent=10,duration=0,net_duration=0),
    ])
    return render(request, 'skyTestApp/tasks0.html')

# To delete all records
def deleterecs(request):
    Tasks.objects.all().delete()
    return render(request, 'skyTestApp/tasks1.html')


# Serializer class relating to Tasks Model
class TasksSerializer(serializers.Serializer):
     id=serializers.IntegerField()
     name=serializers.CharField(max_length=30)
     status=serializers.CharField(max_length=30)
     start_date=serializers.CharField(max_length=30)
     end_date=serializers.CharField(max_length=30)
     parent=serializers.IntegerField()
     duration=serializers.CharField(max_length=30)
     net_duration=serializers.CharField(max_length=30)

# Default UserSerializer class relating to User Model
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

# Default GroupSerializer class relating to Group Model
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# Api Serializer class relating to Tasks Model
class ApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'name','status','start_date','end_date','parent','duration','net_duration']

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ApiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

#
# class TasksCRUDCBV(ModelViewSet):
#     queryset=Tasks.objects.all()
#     serializer_class=TasksSerializer
#     authentication_classes=[CustomAuthentication,]
#     permission_classes=[IsAuthenticated,]
