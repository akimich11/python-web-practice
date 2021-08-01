import json
import os
import tempfile

from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Setting
from .form import ControllerForm


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        try:
            with open(os.path.join(tempfile.gettempdir(), 'controller.json')) as f:
                context['data'] = json.load(f)  # Current values
        except FileNotFoundError:
            context['data'] = {}
        return context

    def get_initial(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), 'controller.json')) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'bedroom_light': False, 'bathroom_light': False}
        return {
            'bedroom_light': data['bedroom_light'],
            'bathroom_light': data['bathroom_light'],
            'hot_water_target_temperature': Setting.objects.get(controller_name='hot_water_target_temperature').value,
            'bedroom_target_temperature': Setting.objects.get(controller_name='bedroom_target_temperature').value
        }

    def form_valid(self, form):
        with open(os.path.join(tempfile.gettempdir(), 'form.json'), 'w') as f:
            json.dump({'bedroom_light': form.cleaned_data['bedroom_light'],
                       'bathroom_light': form.cleaned_data['bathroom_light']}, f)
        Setting.objects.filter(controller_name='hot_water_target_temperature').update(
            value=form.cleaned_data['hot_water_target_temperature'])
        Setting.objects.filter(controller_name='bedroom_target_temperature').update(
            value=form.cleaned_data['bedroom_target_temperature'])
        return super(ControllerView, self).form_valid(form)
