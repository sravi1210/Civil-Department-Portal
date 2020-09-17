from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from . import forms
from users.models import CustomUser
from .forms import TASlipForm,UpdateStudDetail ,LeaveForm, UpdateHodDetail,UpdateDppcDetail,UpdateHodDetail,UpdateStaffDetail,UpdateFacultyDetail
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required

# dashboard for the users of the software ie . student , dppc , HOD  , faculty

def dashboard(request):

    # if the user is student
    if request.user.person=='student':
        student = models.Student.objects.filter(user=request.user)

        # if the student has registered for the first time,
        # he will be asked to fill the form
        if not student :
            if request.method=='POST' :

                form = UpdateStudDetail(request.POST , request.FILES )
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = request.user
                    detail.save()
                return redirect('leave_portal:dashboard')
            else :
                form = UpdateStudDetail(request.POST)
                return render(request,'leave_portal/StudDetail.html', {'form':form , 'student':request.user.username} )

        # else he will be directed towards his dashboard
        else:
            student = models.Student.objects.get(user=request.user)
            forms = models.ApplyLeave.objects.filter(student=student).order_by('-DateOfApply')
            return render(request,'leave_portal/dashboard.html',{'user':request.user , 'student':student, 'forms':forms})

    # if the user is a DPPC
    elif request.user.person=='dppc':
        dppc = models.Dppc.objects.filter(user=request.user)

        # as in student, if dppc is logging in for the first time
        if not dppc :
            form =  UpdateDppcDetail()
            if request.method=='POST' :
                form =  UpdateDppcDetail(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = request.user
                    detail.save()
                    #we are getting an error
                return redirect('leave_portal:dashboard')
            else :
                return render(request,'leave_portal/dppc_update_detail.html', {'form':form , 'dppc':request.user.username} )

        # else he will be directed to hos dashbpard
        else:
            authorized = models.Dppc.objects.get(user=request.user)
            forms=models.ApplyLeave.objects.filter(flag=3,ApprovedStatus='pending')
            return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized, 'forms':forms})

    # if the user logging in is the HOD
    elif request.user.person=='hod':
        hod = models.Hod.objects.filter(user=request.user)

        #  if the HOD is logging in for the first time
        if not hod :
            form =  UpdateHodDetail()
            if request.method=='POST' :
                form =  UpdateHodDetail(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = request.user
                    detail.save()
                    #we are getting an error
                return redirect('leave_portal:dashboard')
            else :
                return render(request,'leave_portal/dppc_update_detail.html', {'form':form , 'dppc':request.user.username} )

        # else HOD is taken to his dashboard
        else:
            authorized = models.Hod.objects.get(user=request.user)
            forms=models.ApplyLeave.objects.filter(flag=5,ApprovedStatus__iexact='pending')
            return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized, 'forms':forms})

    #  similar coding has been done for the staff and the faculty users

    elif request.user.person=='staff':
        staff = models.Staff.objects.filter(user=request.user)
        if not staff :
            form =  UpdateStaffDetail()
            if request.method=='POST' :
                form =  UpdateStaffDetail(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = request.user
                    detail.save()
                    #we are getting an error
                return redirect('leave_portal:dashboard')
            else :
                return render(request,'leave_portal/dppc_update_detail.html', {'form':form , 'dppc':request.user.username} )
        else:
            authorized = models.Staff.objects.get(user=request.user)
            forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
            return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

    elif request.user.person=='faculty':
        faculty = models.Faculty.objects.filter(user=request.user)
        if not faculty :
            form =  UpdateFacultyDetail()
            if request.method=='POST' :
                form =  UpdateFacultyDetail(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = request.user
                    detail.save()
                    #we are getting an error
                return redirect('leave_portal:dashboard')
            else :
                return render(request,'leave_portal/dppc_update_detail.html', {'form':form , 'dppc':request.user.username} )
        else:
            authorized = models.Faculty.objects.get(user=request.user)
            forms1=models.ApplyLeave.objects.filter(student__TA_instructor__user=request.user ,flag=1,ApprovedStatus__iexact='pending')
            forms2=models.ApplyLeave.objects.filter(student__Supervisor_1__user=request.user ,flag=2,ApprovedStatus__iexact='pending')
            forms=forms1 | forms2
            return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

#  function was used for testing purposes
def index(request):
    return HttpResponse("HelloWorld!!")

# generic view to display all rhe students we have registered in our database
class StudentListView(generic.ListView):
    model = models.CustomUser
    context_object_name = 'student_list'
    queryset = CustomUser.objects.filter(person__iexact='student') # Get 5 books containing the title war
    template_name = 'leave_portal/student_list.html'

# generic view to display all the information of a student basec on hos id
class StudentDetailView(generic.DetailView):
    model = models.Student

class ApplyLeaveDetailView(generic.DetailView):
    model = models.ApplyLeave

#  function that will be called when student requests for a leave
def ApplyLeave(request,pk):
    student = get_object_or_404(models.Student, pk=pk)
    form =  LeaveForm()

    if request.method == 'POST':
        form =  LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = student

            if '1' in leave.SentTo:
                leave.flag=1

            if '2' in leave.SentTo and leave.flag is 0:
                leave.flag=2

            if '3' in leave.SentTo:
                leave.flag=3

            leave.save()
            return HttpResponseRedirect(student.get_absolute_url())
    return render(request, 'leave_portal/leaveform.html', {'student':student, 'form':form})

#change flag accordingly

# function to make changes to the leave
def ApplyLeaveEdit(request, pk, leave_id):
    student = get_object_or_404(models.Student, pk=pk)
    leave = get_object_or_404(models.ApplyLeave, pk=leave_id, student=student)

    form =  LeaveForm(instance=leave)

    if request.method == 'POST':
        form =  LeaveForm(instance=leave, data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(student.get_absolute_url())

    return render(request, 'leave_portal/leaveform.html', {'form':form, 'student':student})

class DppcListView(generic.ListView):
    model = models.Dppc

class DppcDetailView(generic.DetailView):
    model = models.Dppc

# function that allows the student to uodate his profile
def StudentUpdateDetail(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    form =  UpdateStudDetail( instance = student)

    if request.method == 'POST' :
        form =  UpdateStudDetail( request.POST  , request.FILES , instance = student )
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(student.get_absolute_url())

    return render(request, 'leave_portal/StudDetail.html', {'form':form, 'student':student})

# just like the case for the student we have functions that will update the profiles
# of the HOD , DPPC , staff and the faculty

def DppcUpdateDetail(request, pk):
    dppc = get_object_or_404(models.Dppc, pk=pk)
    form =  UpdateDppcDetail(instance=dppc)

    if request.method == 'POST':
        form =  UpdateDppcDetail( request.POST  , request.FILES , instance = dppc)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(dppc.get_absolute_url())

    return render(request, 'leave_portal/dppc_update_detail.html', {'form':form, 'authorized':dppc})

def HodUpdateDetail(request, pk):
    hod = get_object_or_404(models.Hod, pk=pk)
    form =  UpdateHodDetail(instance=hod)

    if request.method == 'POST':
        form =  UpdateHodDetail( request.POST  , request.FILES , instance = hod )
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(hod.get_absolute_url())

    return render(request, 'leave_portal/dppc_update_detail.html', {'form':form, 'authorized':hod})

def StaffUpdateDetail(request, pk):
    staff = get_object_or_404(models.Staff, pk=pk)
    form =  UpdateStaffDetail(instance=staff)

    if request.method == 'POST':
        form =  UpdateStaffDetail( request.POST  , request.FILES , instance = staff )
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(staff.get_absolute_url())

    return render(request, 'leave_portal/dppc_update_detail.html', {'form':form, 'authorized':staff})

def FacultyUpdateDetail(request, pk):
    faculty = get_object_or_404(models.Faculty, pk=pk)
    form =  UpdateFacultyDetail(instance=faculty)

    if request.method == 'POST':
        form =  UpdateFacultyDetail( request.POST  , request.FILES , instance = faculty)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(faculty.get_absolute_url())

    return render(request, 'leave_portal/dppc_update_detail.html', {'form':form, 'authorized':faculty})

# function to show all the pending requests to the student
def PendingRequest(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    forms = models.ApplyLeave.objects.filter(student=student,ApprovedStatus='pending')
    return render(request, 'leave_portal/pending_request.html', {'forms':forms})

# function that displays all the leaves of the students that are not pending
def History(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    forms = models.ApplyLeave.objects.filter(student=student)
    return render(request, 'leave_portal/history.html', {'forms':forms})

def Update_Odd_Semester(request):
    students = models.Student.objects.all()
    for student in students:
        print(student.Ordinary)
        student.Ordinary = student.Ordinary + 15
        student.Acedemic = student.Acedemic + 30
        student.Medical = student.Medical + 15
        student.save()

    authorized = models.Staff.objects.get(user=request.user)
    forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
    return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

def Update_Even_Semester(request):
    students = models.Student.objects.all()
    for student in students:
        student.Ordinary = 15
        student.Acedemic = 30
        student.Medical = 15
        student.save()

    authorized = models.Staff.objects.get(user=request.user)
    forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
    return render(request,'leave_portal/authorized_dashboard.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

def Verify_Update_Odd_Semester(request):
    authorized = models.Staff.objects.get(user=request.user)
    forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
    return render(request,'leave_portal/confirm_odd_sem.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

def Verify_Update_Even_Semester(request):
    authorized = models.Staff.objects.get(user=request.user)
    forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
    return render(request,'leave_portal/confirm_even_sem.html',{'user':request.user , 'authorized':authorized , 'forms':forms})





#
# the following notation has been used :
# flag value of x denotes the leave iw with y
#
# x=1 means y= TA INSTRUCTOR
# x=2 means y = Supervisor
# x=3 means y= DPPC
# x=4 means y= staff
# x=5 means y= HOD


# funtion that displays all the leaves to the users
def authorized_pending(request):
    if request.user.person == 'dppc':
        forms=models.ApplyLeave.objects.filter(flag=3,ApprovedStatus='pending')

    elif request.user.person == 'faculty' :

        forms1=models.ApplyLeave.objects.filter(student__TA_instructor__user=request.user ,flag=1,ApprovedStatus__iexact='pending')
        forms2=models.ApplyLeave.objects.filter(student__Supervisor_1__user=request.user ,flag=2,ApprovedStatus__iexact='pending')
        forms=forms1 | forms2

    elif request.user.person == 'hod':
        forms=models.ApplyLeave.objects.filter(flag=5,ApprovedStatus__iexact='pending')

    elif request.user.person == 'staff':
        forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')

    return render(request, 'leave_portal/authorized_pending_request.html',{'forms':forms})

#  following all the instructions as per rule, leave will be sent to appropriate location if approved by a user

def approveleave(request, pk):
    form = get_object_or_404(models.ApplyLeave , pk=pk)

    # if hod approves, leave is approved
    if form.flag is 5:
        d = form.LeaveTo - form.LeaveFrom

        student = models.Student.objects.get(user=form.student.user)
        type = form.TypeOfLeave
        day = d.days

        if type == "Ordinary":
            student.Ordinary = student.Ordinary - day
        elif type == "Medical":
            student.Medical = student.Medical-day
        elif type == "Paternity":
            student.Paternity = student.Paternity - day
        elif type == "Maternity":
            student.Maternity = student.Maternity - day
        elif type == "Acedemic":
            student.Acedemic = student.Acedemic - day
        student.save()
        
        form.ApprovedStatus='approved'

    #  if leave request has not reached the staff
    if form.flag < 4 :

        # if the student has sent the leave to both TA INSTRUCTOR and SUPERVISOR
        if '1' in form.SentTo and '2' in form.SentTo:

            #  if the leave is sent to TA_INSTRUCTOR and he approves it, leave is snet to the Supervisor
            if form.flag is 1:
                form.flag=2

            # if its the Supervisor who accepts the request, it is sent to the staff
            else:
                form.flag=4

        # if the student has sent the leave to either the TA INSTRUCTOR or the SUPERVISOR
        elif '1' in form.SentTo or '2' in form.SentTo:
            # request sent to staff straightaway
            form.flag=4

        # if DPPC approves the request it is sent to the staff
        elif '3' in form.SentTo:
            form.flag=4

    # if staff approves the leave, it will be sent to the HOD
    else:
        form.flag+=1

    form.save()
    return redirect('leave_portal:dashboard')

#  if anyone in the process declines the request at any point , status of leave is set to declined
def declineleave(request, pk):
    form = get_object_or_404(models.ApplyLeave , pk=pk)
    form.ApprovedStatus='declined'
    form.save()
    return redirect('leave_portal:dashboard')

def LeaveInfo(request, pk):

    student = models.Student.objects.get(user=request.user)
    forms = models.ApplyLeave.objects.filter(student=student).order_by('-DateOfApply')

    return render(request,'leave_portal/studentLeaveInfo.html',{'user':request.user , 'student':student, 'forms':forms})

def AuthorizedLeaveInfo(request):

    if request.user.person=='dppc':
        authorized = models.Dppc.objects.get(user=request.user)
        forms=models.ApplyLeave.objects.filter(flag=3,ApprovedStatus='pending')
        return render(request,'leave_portal/authorizedLeaveInfo.html',{'user':request.user , 'authorized':authorized, 'forms':forms})

    # if the user logging in is the HOD
    elif request.user.person=='hod':
        authorized = models.Hod.objects.get(user=request.user)
        forms=models.ApplyLeave.objects.filter(flag=5,ApprovedStatus__iexact='pending')
        return render(request,'leave_portal/authorizedLeaveInfo.html',{'user':request.user , 'authorized':authorized, 'forms':forms})

    elif request.user.person=='staff':
        authorized = models.Staff.objects.get(user=request.user)
        forms=models.ApplyLeave.objects.filter(flag=4,ApprovedStatus__iexact='pending')
        return render(request,'leave_portal/authorizedLeaveInfo.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

    elif request.user.person=='faculty':
        authorized = models.Faculty.objects.get(user=request.user)
        forms1=models.ApplyLeave.objects.filter(student__TA_instructor__user=request.user ,flag=1,ApprovedStatus__iexact='pending')
        forms2=models.ApplyLeave.objects.filter(student__Supervisor_1__user=request.user ,flag=2,ApprovedStatus__iexact='pending')
        forms=forms1 | forms2
        return render(request,'leave_portal/authorizedLeaveInfo.html',{'user':request.user , 'authorized':authorized , 'forms':forms})

def ApplyTaSlip(request , pk):

    student = get_object_or_404(models.Student, pk=pk)
    form =  TASlipForm()
    if request.method == 'POST':
        form =  TASlipForm(request.POST)
        if form.is_valid():
            taSlip = form.save(commit=False)
            taSlip.student = student
            taSlip.save()
            return HttpResponseRedirect(student.get_absolute_url())
    return render(request, 'leave_portal/leaveform.html', {'student':student, 'form':form})

def SlipsPortal(request , pk ):

    student = models.Student.objects.get(user=request.user)
    forms = models.TASlip.objects.filter(student=student).order_by('-DateOfApply')

    return render(request,'leave_portal/studentTASlipsInfo.html',{'user':request.user , 'student':student, 'forms':forms})














#  end of views
