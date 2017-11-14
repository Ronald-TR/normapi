def isModelField(field):
    bResult = False
    if not (field.many_to_many or field.many_to_one or field.one_to_many or field.one_to_one) or (field.__class__.__name__ == 'ForeignKey'):
        bResult = True

    return bResult
    
def DictAttrToNeo4jAttr(attributes):
    strattr = ''
    for key, value in attributes.items():
        strattr = strattr + str(key) + ':' + '\'' + str(value) + '\'' + ','

    return '{' + strattr[0:strattr.__len__()-1] + '}'

nodes = []
relationshipsHierarchy = {} # guardo o nome do pai e filhos
# utilizo cont como limitador de recursividade, sera um atributo customizado na criação da querie
def djangomodel_to_neo4j(model, cont = 0):
    classname = model.__class__.__name__
    attributes = {}
    relationships = []
    pk_name = ''
    neo4jlabel = ''
    modelfields = [field for field in model._meta.get_fields() if isModelField(field)]

    for field in modelfields:
        value = model.__getattribute__(field.name)
        # se for chave estrangeira, assigno o valor dela ao pai, e crio um objeto completo do filho e guardo seu nome para o relacionamento
        if field.__class__.__name__ == 'ForeignKey' and not (cont > 0):
            value = model.__getattribute__(field.name).__getattribute__(field.name)
            relationships = relationships + [djangomodel_to_neo4j(model.__getattribute__(field.name), cont + 1)]
            #query_neo4j = query_neo4j + djangomodel_to_neo4j(model.__getattribute__(field.name), cont + 1)

        attributes.__setitem__(field.name, value)
                        
        if field.primary_key: pk_name = field.name

    try:
        neo4jlabel = model.__getattribute__('neo4j_label')()
    except:
        neo4jlabel = pk_name + '_' + str(model.__getattribute__(pk_name))        

    if cont == 0:
        relationshipsHierarchy.__setitem__(neo4jlabel, 'father')
    else:
        relationshipsHierarchy.__setitem__(neo4jlabel, 'child');
    
    # se o model tiver um nome neo4j personalizado para o objeto, assigno, senao
    # utilizo uma convenção de id_ + valor do id para descrever o nome do objeto(o que e muito pouco intuitivo)
    
    query_neo4j = 'CREATE ({neo4jlabel}:{classname}{attributes})'.format(neo4jlabel=neo4jlabel, classname=classname, attributes=DictAttrToNeo4jAttr(attributes))
    print(relationships)

    return query_neo4j

def MakeRelationships(relationshipsHierarchy):
    strRelationship = 'CREATE '
    for key, value in relationshipsHierarchy.items():
        strRelationship = strRelationship + '(' + key + ')-[:pertence_a]->(' + value + '),'
    return strRelationship[0:strRelationship.__len__()-1]
    



    
neo4jQueries = [djangomodel_to_neo4j(cli) for cli in Clientes.objects.all()]

[print(qry) for qry in neo4jQueries] # prints te CREATE Nodes command

print(MakeRelationships(relationshipsHierarchy)) # prints the CREATE Relationships command
