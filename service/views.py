from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from service.tasks import get_service_bot_message
from service.models import ServiceCategory
from django.views.generic import ListView
from service.forms import OrderServiceForm



class ServiceList(ListView):
    template_name = 'service/service_list.html'
    context_object_name = 'services'
    model = ServiceCategory

    def get_queryset(self):
        return ServiceCategory.objects.annotate(total_services=
                                                Count('services',
                                                      filter=
                                                      Q(services__published=
                                                        True))).\
                                                filter(total_services__gt=0)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canonical_url'] = reverse('service:service_list')
        return context


def service_category_detail(request, service_category_slug):
    service_category = get_object_or_404(ServiceCategory,
                                         slug=service_category_slug)
    services = service_category.services.filter(published=True)
    order_form = OrderServiceForm(
        initial={'service_name': service_category.name})
    return render(request, 'service/service_detail.html', {
        'service_category': service_category,
        'services': services,
        'order_form': order_form,
        'canonical_url': request.build_absolute_uri(service_category.get_absolute_url())
    })


class OrderServiceView(View):
    def post(self, request):
        form = OrderServiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            get_service_bot_message.delay(application=cd)
            return JsonResponse(
                data=
                {'success': 'Спасибо! Мы свяжемся с Вами в ближайшее время.'},
                status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse(data={'error': errors}, status=400)








