
from django.contrib import messages
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.utils.html import format_html
from django.conf import settings
from django.db.models import Q, Case, When, Value, IntegerField

import os
import io
import locale
from datetime import datetime
from docxtpl import DocxTemplate

from .functions import number_to_text_uzbek
from .forms import ApplicationForm
from .models import Hall, District, Application

locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')

class HallList(ListView):
    model = Hall
    context_object_name = 'halls'
    ordering = ['-created_at']
    template_name = 'index.html'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('name')
        object_list = self.model.objects
        if query:
            return object_list.annotate(
                relevance=Case(
                    When(name__icontains=query, then=Value(2)),
                    When(description__icontains=query, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).order_by('-relevance', '-created_at')
        return object_list.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if query := self.request.GET.get('name'):
            context["name"] = query
        return context
    
class HallDetail(DetailView):
    model = Hall
    context_object_name = 'hall'
    template_name = 'detail.html'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        hall = self.get_object()
        hall.view_count += 1
        hall.save()
        
        return response
    
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        UUID = ''
        if form.is_valid(): 
            application = form.save(commit=False)
            date_range = form.cleaned_data.get('date_range')
            
            if date_range:
                application.date_from, application.date_to = date_range.split(' - ')
            
            application.save()
            UUID = application.application_id
        else:
            messages.error(request, 'Ma\'lumotlar notug\'ri kiritilgan:')
            print(form.errors, flush=True)
            for error in form.errors:
                messages.error(request, error)
            return redirect('detail', pk=kwargs.get('pk'))
        
        scheme = request.scheme
        host = request.get_host()
        full_url = f"{scheme}://{host}/application/{UUID}"
        
        message_text = f'Ariza muvaffaqiyatli yuborildi, iltimos Ariza ID ({UUID}) ni saqlab quying, ariza holatini <a href="{full_url}" class="text-decoration-underline">{full_url}</a> orqali tekshirishingiz mumkin'
        
        messages.success(request, format_html(message_text))
        return redirect('application-detail', application_id=UUID)

class ApplicationDetail(DetailView):
    model = Application
    template_name = 'application_detail.html' 
    context_object_name = 'application'

    def get_object(self, queryset=None):
        application_id = self.kwargs.get('application_id')
        obj = get_object_or_404(Application, application_id=application_id)
        return obj

class ApplicationSearch(TemplateView):
    template_name = 'application_search.html'
    
    def post(self, request, *args, **kwargs):
        application_id = request.POST.get('application_id', '')
        application = Application.objects.filter(application_id=application_id.replace(" ", "")).first()
        if application:
            return redirect('application-detail', application_id=application.application_id)
        else:
            messages.error(request, 'Ariza topilmadi')
            return render(request, self.template_name)

class ApplicationFile(View):
    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        application = get_object_or_404(Application, application_id=str(application_id))

        rent_days = application.date_to - application.date_from
        rent_days = int(rent_days.days)
        
        hall = application.hall
        total_sum = int(hall.price) * rent_days
        total_sum_format = f"{total_sum:,}".replace(',', ' ')
        hall_location = hall.location()
        context = {
            'contract_number':application.id,
            'hall_name': hall.name,
            'hall_director': hall.director,
            'hall_price': f"{hall.price:,}".replace(',', ' '),
            'hall_phone_number':hall.phone_number,
            'hall_location_asd': hall_location,
            'hall_inn': hall.inn,
            'application_name': application.name,
            'application_director': application.director,
            'application_address': application.address,
            'application_phone_number': application.phone_number,
            'application_inn': application.inn,
            'application_acc_number': application.account_number,
            'date': datetime.now().strftime("%Y-yil “%d” %B"),
            'hall_days': rent_days,
            'total_text': f'{total_sum_format} ({number_to_text_uzbek(total_sum)})',
            'total_sum': total_sum_format
        }
        
        template = DocxTemplate(os.path.join(settings.BASE_DIR, 'static', 'assets', 'doc', 'template.docx'))
        template.render(context)

        doc_io = io.BytesIO()
        template.save(doc_io)
        doc_io.seek(0)

        response = HttpResponse(doc_io.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Shartnoma.docx"'
        return response

def load_districts(request):
    region_id = request.GET.get('region')
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)