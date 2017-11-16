import json
from visualiser.models import Country, StatisticItem, Statistics
from django.http import JsonResponse
from django.db.models import Avg, Max, Count
from django.db.models.sql.datastructures import Join
from django.db.models.fields.related import ForeignObject


def get_value(statistics):
    if statistics.name.type == 'integer':
        return statistics.int_value
    elif statistics.name.type == 'numeric':
        return statistics.numeric_value
    elif statistics.name.type == 'string':
        return statistics.string_value
    elif statistics.name.type == 'binary':
        return statistics.binary_value
    elif statistics.name.type == 'json':
        return statistics.json_value
    elif statistics.name.type == 'datetime':
        return statistics.datetime_value
    else:
        return None


def default(request):
    '''
    default data presentation
    '''

    countries = Country.objects.all()
    query = Statistics.objects.raw(
        r'select * from {statistics} join ('
        r'select max("{statistics}"."updated_at") as "latest_updated_at",'
        r'"{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}" '
        r'from "{statistics}" '
        r'group by "{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}"'
        r') as t '
        r'on "{statistics}"."serial" = t."serial" and '
        r'"{statistics}"."{country}" = t."{country}" and '
        r'"{statistics}"."{name}" = t."{name}" and '
        r'"{statistics}"."updated_at" = t."latest_updated_at"'
        .format(
            statistics=Statistics._meta.db_table,
            country=Statistics._meta.get_field('country').get_attname(),
            name=Statistics._meta.get_field('name').get_attname()
        ))
    result = {
        'countries':
            [{
                'id': o.pk,
                'name': o.name,
                'description': o.description
            } for o in countries],
        'statistic_items':
            [{
                'id': o.pk,
                'name': o.name,
                'description': o.description,
                'type': o.type
            } for o in StatisticItem.objects.all()],
        'statistics':
            [{
                'id': o.pk,
                'country': o.country.pk,
                'name': o.name.pk,
                'value': get_value(o),
                'serial': o.serial,
                'updated_at': o.updated_at
            } for o in query]
    }
    return JsonResponse(result)


def by_country(request, country):
    '''
    retrieve country history
    '''
    query = Statistics.objects.raw(
        r'select * from {statistics} join ('
        r'select max("{statistics}"."updated_at") as "latest_updated_at",'
        r'"{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}" '
        r'from "{statistics}" '
        r'group by "{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}"'
        r') as t '
        r'on "{statistics}"."serial" = t."serial" and '
        r'"{statistics}"."{country}" = t."{country}" and '
        r'"{statistics}"."{name}" = t."{name}" and '
        r'"{statistics}"."updated_at" = t."latest_updated_at"'
        .format(
            statistics=Statistics._meta.db_table,
            country=Statistics._meta.get_field('country').get_attname(),
            name=Statistics._meta.get_field('name').get_attname()
        ))
    country = Country.objects.get(pk=country)
    result = {
        'countries': [{
            'id': country.pk,
            'name': country.name,
            'description': country.description
        }],
        'statistics_items':
            [{
                'id': o.pk,
                'name': o.name,
                'description': o.description,
                'type': o.type
            } for o in StatisticItem.objects.all()],
        'statistics':
            [{
                'id': o.pk,
                'country': o.country.pk,
                'name': o.name.pk,
                'value': get_value(o),
                'serial': o.serial,
                'updated_at': o.updated_at
            } for o in query]
    }
    return JsonResponse(result)


def filter_by(request):
    filters = json.load(request.body)
    params = []
    if 'serial' in filters and len(filters['serials']) > 0:
        serial_filter = r'"%s"."serial" in (' % Statistics._meta.db_table \
                      + ','.join(map(lambda: '%s', filters['serials'])) \
                      + ')'
        params += filters['serials']
    else:
        serial_filter = 'true'

    if 'countries' in filters and len(filters['countries']) > 0:
        country_filter = r'"%s"."%s" in (' % (
                            Statistics._meta.db_table,
                            Statistics._meta.get_field('country').get_attname()
                         ) \
                       + ','.join(map(lambda: '%s', filters['countries'])) \
                       + ')'
        params += filters['countries']
    else:
        country_filter = 'true'

    if 'names' in filters and len(filters['names']) > 0:
        name_filter = r'"%s"."%s" in (' % (
                          Statistics._meta.db_table,
                          Statistics._meta.get_field('name').get_attname()
                      ) \
                    + ','.join(map(lambda: '%s', filters['names'])) \
                    + ')'
        params += filters['names']
    else:
        name_filter = 'true'

    query = Statistics.objects.raw(
        r'select * from "{statistics}" join ('
        r'select max("{statistics}"."updated_at") as "latest_updated_at",'
        r'"{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}" '
        r'from "{statistics}" '
        r'group by "{statistics}"."serial", "{statistics}"."{country}", "{statistics}"."{name}"'
        r') as t '
        r'on "{statistics}"."serial" = t."serial" and '
        r'"{statistics}"."{country}" = t."{country}" and '
        r'"{statistics}"."{name}" = t."{name}" and '
        r'"{statistics}"."updated_at" = t."latest_updated_at"'
        r'where {serial_filter} and {country_filter} and {name_filter}'
        .format(
            statistics=Statistics._meta.db_table,
            country=Statistics._meta.get_field('country').get_attname(),
            name=Statistics._meta.get_field('name').get_attname(),
            serial_filter=serial_filter,
            country_filter=country_filter,
            name_filter=name_filter
        ),
        params=params
    )
    countries = []
    statistics = []
    for o in query:
        statistics.append({
            'id': o.pk,
            'country': o.country.pk,
            'name': o.name.pk,
            'value': get_value(o),
            'serial': o.serial,
            'updated_at': o.updated_at
        })
        countries.append({
            'id': o.country.pk,
            'name': o.country.name,
            'description': o.country.description
        })
    result = {
        'countries': countries,
        'statistics_item':
            [{
                'id': o.pk,
                'name': o.name,
                'description': o.description,
                'type': o.type
            } for o in StatisticItem.objects.all()],
        'statistics': statistics
    }
    return JsonResponse(result)