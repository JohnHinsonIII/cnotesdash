# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import GeneratePdf

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('all_contracts/', views.all_contracts, name='all_contracts'),
    path('add_contract/', views.add_contract, name='add_contract'),
    path('update_contract/<edit_id>/', views.update_contract, name='update_contract'),
    path('delete_contract/<delete_id>/', views.delete_contract, name="delete_contract"),
    path('detail_contracts/<detail_id>/', views.detail_contracts, name='detail_contracts'),
    path('add_document/<int:contract_id>/', views.add_document, name='add_document'),
    path('update_document/<int:document_id>/', views.update_document, name='update_document'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),

    path('add_review/<int:contract_id>/', views.add_review, name='add_review'),
    path('update_review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('pdf/<detail_id>/', GeneratePdf.as_view(), name='pdf'),



    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
