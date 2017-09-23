import datetime
import json
from django.db.models.utils import make_model_tuple
from django.forms import model_to_dict


class Pessoa():
    def __init__(self):
        self.nome = 'ronald'
        self.idade = 22
        self.data_nascimento = datetime.date(1995, 11, 30)

ronald = Pessoa()

r = ronald.__dict__


def SerializeModel(model):
    mdict = model_to_dict(model)
    for k, v in mdict.items():
        if type(v) is datetime.date:
            mdict[k] = v.strftime('%d/%m/%Y')
        if type(v) is datetime.datetime:
            mdict[k] = v.isoformat()
    return json.dumps(mdict)

