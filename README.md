# normapi
normapi é uma orm-api, uma proposta de integração e exposição a bancos de dados pre-existentes de maneira rápida, facil e de manutenção automática.

## Features
* Capaz de atualizar seu próprio código fonte, mantem seu app fiel a base com apenas um comando no shell.
* Desacoplado, pode ser "plugado" em apps de projetos antigos e ser executado comumente.
* Querys JSON em bancos de dados relacionais
* E claro. Fonte aberto

## Usage
1 º Modo:


* Baixe o repo

* Configure a conexao default com seu o Banco de Dados no *settings.py* do projeto

* Digite no terminal **>manage.py uvgen** 


2 º Modo(para projetos pre-existentes):


* Navegue até a *normapi/nucleo* e copie a pasta *management*

* Cole-a dentro de seu App escolhido

* Digite no terminal **>manage.py uvgen** 


E por ultimo, configure uma rota para as urls de seu app.


Dizer que o normapi é uma orm é errado, ela funciona como uma porque roda a django-orm em seu background.

Por essa razão, você pode ter acesso ao QuerySet API do **manager** da django-orm nativamente providos pela interpretação da **normapi**. (Apenas disponivel o metodo order_by por enquanto)


Todos os modelos terão por padrão suas rotas de mesmo nome.
Caso queira acessar um model. Faça um POST para a rota do seu App, passando no body um JSON com os parametros da consulta.
Elas serão interpretadas como o **where**

Para consultar um usuario de uma tabela Usuarios cujo o campo de **id** seja id_usuario:
fapa um POST para:

http://rota_para_seu_app/Usuarios/

com um body:
{
  "id_usuario": "100"
}

Se tudo correr bem, a resposta deve ser um JSON com o seu registro usuario serializado.


*versão beta.
