from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory

from .models import Commission, Job, JobApplication
from .forms import JobApplicationForm, CommissionForm, JobForm
from user_management import models as profileModel

from operator import attrgetter


class CommissionListView(ListView):
	model = Commission
	template_name = "commission-list.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			user = profileModel.Profile.objects.get(user=self.request.user)
			commission_by_user = Commission.objects.filter(author=user)

			job_applications = JobApplication.objects.filter(applicant=user)
			applied_by_user = []
			for application in job_applications:
				job = application.job
				commission = job.commission
				if commission not in applied_by_user:
					applied_by_user.append(commission)
			applied_by_user.sort(key=attrgetter('created_on'))

			ctx['commission_by_user'] = commission_by_user
			ctx['applied_by_user'] = applied_by_user
		return ctx


class CommissionDetailView(DetailView):
	model = Commission
	template_name = "commission-detail.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)	
		job_application_form = JobApplicationForm()
		commission = self.get_object()
		total_ongoing_power = total_manpower_required = 0

		for job in commission.jobs.all():
			job.update_ongoing_manpower()
			total_ongoing_power += job.ongoing_manpower
			total_manpower_required += job.manpower_required

		jobs_in_commission = Job.objects.filter(commission=commission)

		ctx['jobs_in_commission'] = jobs_in_commission
		ctx['total_manpower_required'] = total_manpower_required
		ctx['open_manpower'] = total_manpower_required - total_ongoing_power
		ctx['job_application_form'] = job_application_form

		if self.request.user.is_authenticated:
			user_profile = profileModel.Profile.objects.get(user=self.request.user)
			ctx['display_name_of_user'] = user_profile.display_name

		job_applications = JobApplication.objects.filter(job__in=jobs_in_commission)
		ctx['job_applications'] = job_applications

		return ctx

	def post(self, request, *args, **kwargs):
		commission = self.get_object()
		job_application_form = JobApplicationForm()
		job_pk = request.POST.get('job_pk')
		job = Job.objects.get(pk=job_pk, commission=commission)
		applicant = profileModel.Profile.objects.get(user=self.request.user)

		existing_application = JobApplication.objects.filter(job=job, applicant=applicant).exists()
		if not existing_application:
			job_app = JobApplication.objects.create(applicant=applicant, job=job)
			
		return HttpResponseRedirect(reverse('commissions:commission-detail', kwargs={'pk': commission.pk}))

		ctx = self.get_context_data(**kwargs)
		return self.render_to_response(ctx)


class CommissionCreateView(LoginRequiredMixin, CreateView):
	model = Commission
	form_class = CommissionForm
	template_name = "commission-create.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		author = profileModel.Profile.objects.get(
			user=self.request.user
		)
		ctx['commission_form'] = CommissionForm(initial={'author':author})
		ctx['job_form'] = JobForm(initial={'ongoing_manpower':0})
		return ctx

	def post(self, request, *args, **kwargs):

		post = request.POST
		title = post['title']
		author = profileModel.Profile.objects.get(
			user=self.request.user
		)
		description = post['description']
		status = post['status']

		commission_form = CommissionForm()
		new_commission = commission_form.save(commit=False)
		new_commission.title = title
		new_commission.author = author
		new_commission.description = description
		new_commission.status = status
		new_commission.save()

		temp_post = dict(post)
		roles = temp_post['role']
		manpowers = temp_post['manpower_required']

		for index in range(len(roles)):
			jobform = JobForm()
			new_job = jobform.save(commit=False)
			new_job.role = roles[index]
			new_job.manpower_required = manpowers[index]
			new_job.commission = new_commission
			new_job.save()

		return redirect('commissions:commission-detail', pk=new_commission.id)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
	model = Commission
	form_class = CommissionForm
	template_name = "commission-update.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		commission = self.get_object()
		jobs_in_commission = Job.objects.filter(commission=commission)
		job_applications = JobApplication.objects.filter(job__in=jobs_in_commission)
		job_app_forms = []
		for job_app in job_applications:
			job_app_form = JobApplicationForm(instance=job_app) 
			job_app_forms.append(job_app_form)

		ctx['jobs'] = jobs_in_commission
		ctx['job_applications'] = job_applications
		ctx['job_app_forms'] = job_app_forms
		return ctx

	def post(self, request, *args, **kwargs):
		post = request.POST
		temp_post = dict(post)
		commission = self.get_object()
		statuses = temp_post['status']
		total_manpower_required = total_ongoing_power = 0

		jobs_in_commission = Job.objects.filter(commission=commission)
		for job in jobs_in_commission:
			job.role = temp_post['job_role_'+str(job.pk)][0]
			job.manpower_required = temp_post['job_manpower_required_'+str(job.pk)][0]
			job.save()

		job_applications = JobApplication.objects.filter(job__in=jobs_in_commission)
		counter = 1
		for job_app in job_applications:
			job_app_form = JobApplicationForm(instance=job_app) 
			update_job_app_form = job_app_form.save(commit=False)
			update_job_app_form.status = statuses[counter]
			update_job_app_form.save()
			counter += 1
		
		commission_form = CommissionForm(instance=commission)
		update_comm = commission_form.save(commit=False)
		update_comm.title = temp_post['title'][0]
		update_comm.description = temp_post['description'][0]

		for job in commission.jobs.all():
			job.update_ongoing_manpower()
			total_ongoing_power += job.ongoing_manpower
			total_manpower_required += job.manpower_required

		if statuses[0] == "0" and total_manpower_required == total_ongoing_power:
			update_comm.status = "1"
		else:
			update_comm.status = statuses[0]
		update_comm.save()

		return redirect('commissions:commission-detail', pk=commission.pk)

	def form_invalid(self, form):
		ctx = self.get_context_data(form=form)
		return self.render_to_response(ctx)