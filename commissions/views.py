from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission, Job, JobApplication
from user_management import models as profileModel


class CommissionListView(ListView):
	model = Commission
	template_name = "commission-list.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			user = profileModel.Profile.objects.get(user=self.request.user)
			commission_by_user = Commission.objects.filter(author=user)
			applied_by_user = JobApplication.objects.filter(applicant=user)
			ctx['commission_by_user'] = commission_by_user
			ctx['applied_by_user'] = applied_by_user
		return ctx

class CommissionDetailView(DetailView):
	model = Commission
	template_name = "commission-detail.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		commission = self.object()
		
		for job in commission.job.all:
			total += job.manpower_required
		
		for person in commission.job.applicant.all:
			if person.status == 'accepted':
				taken += 1 

		open_manpower = total - taken
		ctx['total_manpower_requried'] = total
		ctx['open_manpower'] = open_manpower
		return ctx