from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.encoding import smart_str
from django.views.generic import View, UpdateView

from .models import Student, CV, Avatar, Signature


class StudentSearchForm(forms.Form):
    roll_no = forms.IntegerField(label='Roll No', required=True)


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['dob', 'hostel', 'room_no', 'alternative_email',
                  'mobile_campus', 'mobile_home', 'mobile_campus_alternative',
                  'linkedin_link',
                  'address_line1', 'address_line2', 'address_line3',
                  'pin_code',
                  'percentage_x', 'percentage_xii', 'board_x', 'board_xii',
                  'medium_x', 'medium_xii', 'passing_year_x',
                  'passing_year_xii', 'gap_in_study', 'gap_reason',
                  'jee_air_rank',
                  'spi_1_sem', 'spi_2_sem', 'spi_3_sem',
                  'spi_4_sem', 'spi_5_sem', 'spi_6_sem', 'active_backlogs']


class Home(LoginRequiredMixin, UserPassesTestMixin, View):
    template = 'jobportal/Verifier/home.html'
    raise_exception = False
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'verifier'

    def get(self, request):
        form = StudentSearchForm()
        return render(request, self.template, dict(form=form))

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            student = get_object_or_404(Student,
                                        roll_no=form.cleaned_data['roll_no'])
            return redirect('verifier-student-detail', studid=student.id)
        else:
            return render(request, self.template, dict(form=form))


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    template = 'jobportal/Verifier/student_profile_detail.html'
    form_class = StudentSearchForm
    login_url = reverse_lazy('login')
    raise_exception = False

    def test_func(self):
        return self.request.user.user_type == 'verifier'

    def get(self, request, studid):
        student = get_object_or_404(Student, id=studid)
        try:
            cv = CV.objects.get(stud=student)
        except CV.DoesNotExist:
            cv = None
        try:
            avatar = Avatar.objects.get(stud=student)
        except Avatar.DoesNotExist:
            avatar = None
        try:
            signature = Signature.objects.get(stud=student)
        except Signature.DoesNotExist:
            signature = None
        args = dict(student=student, cv=cv, avatar=avatar,
                    signature=signature)
        return render(request, self.template, args)


class StudentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = StudentProfileForm
    template_name = 'jobportal/Verifier/student_profile_update.html'

    def test_func(self):
        return self.request.user.user_type == 'verifier'

    def get(self, request, *args, **kwargs):
        stud = get_object_or_404(Student, id=self.kwargs['pk'])
        form = StudentProfileForm(instance=stud)
        args = dict(form=form, stud=stud)
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        stud = get_object_or_404(Student, id=self.kwargs['pk'])
        form = StudentProfileForm(instance=stud, data=request.POST)
        if form.is_valid():
            print "form valid"
            form.save()
            return redirect('verifier-student-detail', studid=stud.id)
        else:
            print "form invalid"
            args = dict(form=form, stud=stud)
            return render(request, self.template_name, args)


class StudentCVDownload(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = False

    def test_func(self):
        return self.request.user.user_type == 'verifier'

    @staticmethod
    def get(request, studid, cvno):
        cv = get_object_or_404(CV, stud__id=studid)
        if cvno == '1' and bool(cv.cv1.name):
            response = HttpResponse(cv.cv1,
                                    content_type='application/pdf')
            download_name = 'CV1_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        elif cvno == '2' and bool(cv.cv2.name):
            response = HttpResponse(cv.cv2,
                                    content_type='application/pdf')
            download_name = 'CV2_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        else:
            raise Http404()


class CVUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = CV
    fields = ['cv1', 'cv2']
    template_name = 'jobportal/Verifier/student_cv_update.html'
    success_url = reverse_lazy('stud-cv-detail')

    def test_func(self):
        return self.request.user.user_type == 'verifier'

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(stud__id=self.kwargs['pk'])
        except CV.DoesNotExist:
            stud = get_object_or_404(Student, id=self.kwargs['pk'])
            cv = CV.objects.create(stud=stud)
        return cv

    def get_success_url(self):
        return reverse_lazy('verifier-student-detail',
                            args=(self.kwargs['pk'],))
