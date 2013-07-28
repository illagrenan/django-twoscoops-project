# -*- encoding: utf-8 -*-

import chromelogger as console
from django.shortcuts import render


def default_page(request):
    console.log(request)

    return render(request, 'web/index.html', {

    })