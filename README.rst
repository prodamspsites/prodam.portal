*******************************************************************
prodam.portal
*******************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

TODO

Requisitos
----------

Para uso deste pacote, seu site deve ter sido construído com:

    * Plone 4.3.3 ou superior (http://plone.org/products/plone)


Estado deste pacote
-------------------

Este produto possui testes automatizados e, a cada alteração de código
esses testes são executados pelo serviço Travis.

O estado atual dos testes pode ser visto pela imagem abaixo:

.. image:: https://travis-ci.org/prodamspsites/prodam.portal.svg
    :target: https://travis-ci.org/prodamspsites/prodam.portal

O estado atual da cobertyra de testes pode ser acompanhado pela imagem abaixo:

.. image:: https://coveralls.io/repos/prodamspsites/prodam.portal/badge.svg
    :target: https://coveralls.io/r/prodamspsites/prodam.portal 


Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``prodam.portal`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            prodam.portal

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Adicione um novo site Plone.
