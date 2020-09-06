from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.views.generic.edit import FormView
from blancas.forms import SearchForm
from django.views.generic import TemplateView
import requests
import json
import logging
from blancas.tools import extract_paginas_blancas, encode_html
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)


class MainView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/login/'
    permissions = []
    template_name = 'blancas/index.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        response = super(MainView, self).get(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            names = list(map(lambda x: x.surname, form.get_names()))
            # Do assign call...
            return TemplateResponse(
                request,
                self.template_name,
                {
                    'actual_index': 0,
                    'total_index': len(names),
                    'names': names,
                    'province': form.data.get('province'),
                    'city': form.data.get('province')
                }
            )


class SearchView(FormView):
    template_name = 'blancas/search.html'
    form_class = SearchForm
    success_url = '/grupo-andujar/'

    def post(self, request, *args, **kwargs):
        """ Returns a json containing 1. The html to load.
        2. The actual index 3. the total index """
        names = request.POST.get("names", '')
        province = request.POST.get("province", '')
        city = request.POST.get("city", '')
        actual = int(request.POST.get("actual_index", '0'))
        total = int(request.POST.get("total_index", '0'))
        numbers = request.POST.get("numbers", '[]')
        if actual < total:
            # Do request
            names_list = names[1:-1].split(', ')
            number_list = json.loads(numbers)
            for name in names_list[actual: actual+10]:
                _url = "http://blancas.paginasamarillas.es/jsp/resultados.jsp?ap1={surname}&sec=23&lo={city}&pgpv=1&tbus=0&nomprov={province}&idioma=spa".format(
                    surname=encode_html(name),
                    city=encode_html(city),
                    province=encode_html(province),
                )
                headers = {
                    "Host": "blancas.paginasamarillas.es",
                    "Connection": "keep-alive",
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,it;q=0.7"
                }
                response = requests.get(_url, headers=headers)
                if response.status_code == 200:
                    number_list.extend(
                        extract_paginas_blancas(response.content.decode())
                    )
                else:
                    if response.content:
                        logger.error("Error calling {}. Details: {}".format(
                            _url,
                            response.content.decode()
                        ))
                    else:
                        logger.error("Error calling {}. Code: {}".format(
                            _url,
                            response.status_code
                        ))
                actual += 1

            template = TemplateResponse(
                request,
                'blancas/table_list.html',
                {
                    'number_list': number_list
                }
            )
            return JsonResponse({
                'content': template.rendered_content,
                'total': total,
                'actual': actual,
                'names': names,
                'numbers': number_list
            })
        else:
            if len(json.loads(numbers)) == 0:
                # There are no numbers so we clean main view data
                # return TemplateResponse(
                #     request,
                #     'blancas/index.html',
                #     {
                #         'actual_index': actual,
                #         'total_index': total,
                #         'names': names,
                #         'province': '',
                #         'city': ''
                #     }
                # )   
                template = TemplateResponse(
                    request,
                    'blancas/table_list.html',
                    {
                        'number_list': json.loads(numbers)
                    }
                )
                return JsonResponse({
                    'content': template.rendered_content,
                    'total': total,
                    'actual': actual,
                    'names': names,
                    'numbers': json.loads(numbers)
                })         

            