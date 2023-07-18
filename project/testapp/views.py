from django.shortcuts import render, reverse
from django import forms
from django.views import View
from .tasks import task1, task2, task3
from celery import current_app
from django.http import JsonResponse





class NumForm(forms.Form):
    first_num = forms.IntegerField(label='Input first number')
    second_num = forms.IntegerField(label='Input second number')


class HomeView(View):

    def get(self, request):
        form = NumForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = NumForm(request.POST)
        context = {}
        if form.is_valid():

            task_a = task1.delay(int(request.POST.get('first_num')), int(request.POST.get('second_num')))
            task_b = task2.delay(int(request.POST.get('first_num')), int(request.POST.get('second_num')))
            task_c = task3.delay(int(request.POST.get('first_num')), int(request.POST.get('second_num')))

            #context['task_id'] = task_a.id
            #context['task_status'] = task_a.status
            context['task_a'] = {'task_id': task_a.id}
            context['task_a']['task_status'] = task_a.status
            context['task_b'] = {'task_id': task_b.id}
            context['task_b']['task_status'] = task_b.status
            context['task_c'] = {'task_id': task_c.id}
            context['task_c']['task_status'] = task_c.status
            return render(request, 'home.html', context)

        context['form'] = form
        return render(request, 'home.html', context)


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)

        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse({'result': response_data})



