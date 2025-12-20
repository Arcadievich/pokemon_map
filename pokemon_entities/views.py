import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from .models import Pokemon
from .models import PokemonEntity
from pogomap.settings import MEDIA_URL


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    """Добавить покемона на карту."""
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    """Показать всех покемонов на карте."""
    local_time = localtime()
    pokemons = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.filter(
        disappeared_at__gt=local_time,
        appeared_at__lt=local_time,
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'{MEDIA_URL}{pokemon_entity.pokemon.image}')
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'{MEDIA_URL}{pokemon.image}'),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    """Показать покемонов в шапке страницы."""
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_entities = pokemon.pokemons.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'{MEDIA_URL}{pokemon_entity.pokemon.image}'),
        )

    pokemon = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': request.build_absolute_uri(f'{MEDIA_URL}{pokemon.image}'),
        'description': pokemon.description,
        'previous_evolution': pokemon.previous_evolution,
        'next_evolution': pokemon.next_evolutions.first(),
    }

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon,
            'MEDIA_URL': MEDIA_URL,
        }
    )