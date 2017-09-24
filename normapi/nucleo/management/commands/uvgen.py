from django.core.management.base import BaseCommand, CommandError
from django.__main__ import management
from importlib import import_module
import os
import sys

urlpatterns = """from django.conf.urls import url
from django.contrib import admin
from {appname}.views import *

urlpatterns = [
{urls}
]

"""

rawurls = """
    url(r'^{urlname}/$', view{urlname}, name='{urlname}'),

"""

reservednames = [
    '__builtins__',
    '__cached__',
    '__doc__',
    '__file__',
    '__loader__',
    '__name__',
    '__package__',
    '__spec__',
    'unicode_literals',
    'models',
    'AuthGroup',
    'AuthGroupPermissions',
    'AuthPermission',
    'AuthUser',
    'AuthUserGroups',
    'AuthUserUserPermissions',
    'DjangoAdminLog',
    'DjangoContentType',
    'DjangoMigrations',
    'DjangoSession',
]


views = """from {appname}.models import *
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.apps import apps
import datetime
import json


def SerializeModel(model):
    mdict = model_to_dict(model)
    for k, v in mdict.items():
        if type(v) is datetime.date:
            mdict[k] = v.strftime('%d/%m/%Y')
        if type(v) is datetime.datetime:
            mdict[k] = v.isoformat()
    return json.dumps(mdict)


def Factory(modelname, jsonparams):
    params = json.loads(jsonparams)
    orderKey = ''
    try:
        orderKey = str(params.pop('order_by'))
    except:
        pass
    if orderKey == '':
        objeto = apps.get_model('{app}', modelname).objects.filter(**params)
    else:
        objeto = apps.get_model('{app}', modelname).objects.filter(**params).order_by('-' + orderKey)
    return objeto

{indview}


"""

rawview = """

@csrf_exempt
def view{classname}(requests):
    if requests.method == 'POST':    
        modelo = Factory('{classname}', requests.body)
        jsonModel = [SerializeModel(m) for m in modelo]
        return HttpResponse(jsonModel, content_type='application/json')
    if requests.method == 'GET':
        return HttpResponse('erro, verbo indisponivel', 404)
"""

class Command(BaseCommand):
    help = 'Script para migracao dos modelos da base, traçando rotas de acesso a cada uma delas, ignorando as tabelas padrões do django-admin'

    #def add_arguments(self, parser):
    #   parser.add_argument('appname', type=str)

    def handle(self, *args, **options):
        # retrocede diretorios de acordo com o contador
        def cdDir(path, cont):
            diretorio = os.path.dirname(os.path.abspath(path))
            if cont == 0:
                return diretorio
            cont = cont - 1
            return cdDir(diretorio, cont)

        dirApp = cdDir(__file__, 2)

        appname = dirApp.split('\\')[-2:]
        appname = '.'.join(appname)

        with open(dirApp + '\\models.py', 'w') as model:
            sys.stdout = model
            management.call_command('inspectdb', shell=True)

        djangoapp = import_module(appname + '.models')
        urls = ''
        indview = ''

        listclasses = [i for i in dir(djangoapp) if not reservednames.__contains__(i)]

        for classe in listclasses:
            urls = urls + rawurls.format(**{'urlname': classe})
            indview = indview + rawview.format(**{'classname': classe})

        with open(dirApp + '\\urls.py', 'w') as p:
            p.write(urlpatterns.format(**{'urls': urls, 'appname': appname}))

        with open(dirApp + '\\views.py', 'w') as p:
            p.write(views.format(**{'indview': indview, 'appname': appname, 'app': appname.split('.')[-1]}))

