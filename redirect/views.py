# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation
from user_agents import parse
from redirect.models import *
# from redirect.models import Page, PageAlias, Redirection


def redirector(request, uri=None):
    def get_uri():
        # Cogemos el id del tweet de la uri
        a = uri.split('/')
        tweet_id = int(a[len(a)-1])

        muTweet = ProjectMutweet.objects.get(pk=tweet_id)
        promo = ProjectPromo.objects.get(pk=muTweet.promo_msg._get_pk_val)
        link_all = promo.link_all
        link_android = promo.link_android
        link_ios = promo.link_ios
        link_others = promo.link_others

        # si existe link_all devuelve el link, sino el correspondiente al user_agent
        if link_all:
            return link_all
        userAgent = request.META['HTTP_USER_AGENT']
        user_agent = parse(userAgent)
        if user_agent.os.family == 'Android':
            return link_android
        elif user_agent.os.family == 'iOS':
            return link_ios
        else:
            return link_others

    redirection_url = get_uri()
    lang = translation.get_language_from_request(request)
    lang = lang[:2] if lang else None


    # try:
    #     redirection = page.redirections.get(platform=platform, language=lang)
    # except Redirection.DoesNotExist:
    #     try:
    #         redirection = page.redirections.get(platform=platform, language='')
    #     except Redirection.DoesNotExist:
    #         # si no existe la plataforma con el lenguaje por defecto miramos la redirección para todas las plataformas
    #         try:
    #             redirection = page.redirections.get(platform=platform, language=lang)
    #         except Redirection.DoesNotExist:
    #             # si no existe el lenguaje para todas las plataformas devolvemos de todas plataformas para todos los lenguajes
    #             redirection = page.redirections.get(platform=None, language='')
    #
    # # pillamos la url hacia la imágen de la card
    # if page.card_img_file:
    #     page.card_img_full_url = request.build_absolute_uri(page.card_img_file.url)
    # elif page.card_img_url:
    #     page.card_img_full_url = page.card_img_url
    # else:
    #     page.card_img_full_url = None
    #
    # page.full_url = request.build_absolute_uri()

    return render_to_response(
        'redirection.html',
        {'redirection_url': redirection_url},
        context_instance=RequestContext(request)
    )


def test(request):
    return render_to_response('test.html')

