from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.model import filter_list_term_type, find_term_match
from hestia_earth.utils.tools import flatten, list_sum, non_empty_list
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from hestia_earth.validation.utils import _filter_list_errors, get_term_lookup_value
from hestia_earth.validation.terms import TERMS_QUERY, get_terms
from .shared import valid_list_sum


def validate_defaultValue(data: dict, list_key: str = 'practices'):
    def validate(values: tuple):
        index, practice = values
        term = practice.get('term', {})
        has_value = len(practice.get('value', [])) > 0
        default_value = get_term_lookup_value(term, 'defaultValue')
        return has_value or default_value is None or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}]",
            'message': 'should specify a value when Hestia has a default one',
            'params': {
                'term': term,
                'expected': default_value
            }
        }

    return _filter_list_errors(flatten(map(validate, enumerate(data.get(list_key, [])))))


def validate_longFallowPeriod(practices: list):
    max_nb_years = 5
    longFallowPeriod = find_term_match(practices, 'longFallowPeriod', None)
    longFallowPeriod_index = practices.index(longFallowPeriod) if longFallowPeriod else 0
    value = list_sum(longFallowPeriod.get('value', [0])) if longFallowPeriod else 0
    rotationDuration = list_sum(find_term_match(practices, 'rotationDuration').get('value', 0))
    return value == 0 or ((rotationDuration - value) / value) < max_nb_years * 365 or {
        'level': 'error',
        'dataPath': f".practices[{longFallowPeriod_index}].value",
        'message': f"longFallowPeriod must be lower than {max_nb_years} years"
    }


def validate_waterRegime_rice_products(cycle: dict, list_key: str = 'practices'):
    all_rice_product_ids = get_terms(TERMS_QUERY.RICE)
    products = cycle.get('products', [])
    rice_products = non_empty_list([
        find_term_match(products, term_id, None) for term_id in all_rice_product_ids
    ])
    lookup = download_lookup('waterRegime.csv')

    def validate(values: tuple):
        index, practice = values
        term = practice.get('term', {})
        term_id = term.get('@id')
        allowed_product_ids = get_table_value(lookup, 'termid', term_id, column_name('allowedRiceTermIds')).split(';')
        not_allowed = list(filter(lambda p: p.get('term').get('@id') not in allowed_product_ids, rice_products))
        return len(not_allowed) == 0 or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].term",
            'message': 'rice products not allowed for this water regime practice',
            'params': {
                'term': term,
                'products': non_empty_list(map(lambda p: p.get('term'), not_allowed))
            }
        }

    return _filter_list_errors(flatten(map(validate, enumerate(cycle.get(list_key, [])))))


def validate_excretaManagement(node: dict, practices: list):
    has_input = len(filter_list_term_type(node.get('inputs', []), TermTermType.EXCRETA)) > 0
    has_practice = len(filter_list_term_type(practices, TermTermType.EXCRETAMANAGEMENT)) > 0
    return not has_practice or has_input or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'an excreta input is required when using an excretaManagement practice'
    }


NO_TILLAGE_ID = 'noTillage'
FULL_TILLAGE_ID = 'fullTillage'
TILLAGE_DEPTH_ID = 'tillageDepth'
NB_TILLAGES_ID = 'numberOfTillages'


def _practice_is_tillage(practice: dict):
    term_id = practice.get('term', {}).get('@id')
    term_type = practice.get('term', {}).get('termType')
    return True if term_type == TermTermType.OPERATION.value and get_table_value(
        download_lookup('operation.csv'), 'termid', term_id, column_name('isTillage')) else False


def validate_no_tillage(practices: list):
    no_tillage = find_term_match(practices, NO_TILLAGE_ID, None)
    no_value = list_sum(no_tillage.get('value', [100]), 100) if no_tillage else 0
    return _filter_list_errors([{
        'level': 'error',
        'dataPath': f".practices[{index}]",
        'message': f"is not allowed in combination with {NO_TILLAGE_ID}"
    } for index, p in enumerate(practices) if _practice_is_tillage(p)] if no_value == 100 else [])


_TILLAGE_SITE_TYPES = [
    SiteSiteType.CROPLAND.value
]


def validate_tillage_site_type(practices: list, site: dict):
    has_tillage = len(filter_list_term_type(practices, TermTermType.TILLAGE)) > 0
    site_type = site.get('siteType')
    return site_type not in _TILLAGE_SITE_TYPES or has_tillage or {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should contain a tillage practice'
    }


def validate_tillage_values(practices: list):
    tillage_100_index = next((index for index in range(0, len(practices)) if all([
        practices[index].get('term', {}).get('termType') == TermTermType.TILLAGE.value,
        list_sum(practices[index].get('value', [0])) == 100
    ])), -1)
    tillage_100_practice = practices[tillage_100_index] if tillage_100_index >= 0 else None
    tillage_100_term = (tillage_100_practice or {}).get('term', {})

    tillage_depth_practice = find_term_match(practices, TILLAGE_DEPTH_ID)
    nb_tillages_practice = find_term_match(practices, NB_TILLAGES_ID)
    error_message = (
        'cannot use no tillage if depth or number of tillages is not 0' if all([
            tillage_100_term.get('@id') == NO_TILLAGE_ID,
            any([
                tillage_depth_practice and list_sum(tillage_depth_practice.get('value', [0])) > 0,
                nb_tillages_practice and list_sum(nb_tillages_practice.get('value', [0])) > 0
            ])

        ])
        else 'cannot use full tillage if depth or number of tillages is 0' if all([
            tillage_100_term.get('@id') == FULL_TILLAGE_ID,
            any([
                tillage_depth_practice and list_sum(tillage_depth_practice.get('value', [1])) == 0,
                nb_tillages_practice and list_sum(nb_tillages_practice.get('value', [1])) == 0
            ])
        ])
        else 'must use no tillage when number of tillages is 0' if all([
            tillage_100_term.get('@id') != NO_TILLAGE_ID,
            nb_tillages_practice and list_sum(nb_tillages_practice.get('value', [1])) == 0
        ])
        else None
    ) if tillage_100_practice else None
    return {
        'level': 'error',
        'dataPath': f".practices[{tillage_100_index}]",
        'message': error_message
    } if error_message else True


def validate_liveAnimal_system(data: dict):
    has_liveAnimal = len(filter_list_term_type(data.get('products', []), TermTermType.LIVEANIMAL)) > 0
    has_system = len(filter_list_term_type(data.get('practices', []), TermTermType.SYSTEM)) > 0
    return not has_liveAnimal or has_system or {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should add an animal production system'
    }


PASTURE_GRASS_TERM_ID = 'pastureGrass'


def validate_pastureGrass_key_termType(data: dict, list_key: str = 'practices'):
    validate_key_termType = TermTermType.LANDCOVER.value

    def validate(values: tuple):
        index, practice = values
        term_id = practice.get('term', {}).get('@id')
        key_termType = practice.get('key', {}).get('termType')
        return term_id != PASTURE_GRASS_TERM_ID or not key_termType or key_termType == validate_key_termType or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].key",
            'message': f"{PASTURE_GRASS_TERM_ID} key termType must be '{validate_key_termType}'",
            'params': {
                'value': key_termType,
                'expected': validate_key_termType,
                'term': practice.get('key', {})
            }
        }

    return _filter_list_errors(flatten(map(validate, enumerate(data.get(list_key, [])))))


def validate_pastureGrass_key_value(data: dict, list_key: str = 'practices'):
    practices = [p for p in data.get(list_key, []) if p.get('term', {}).get('@id') == PASTURE_GRASS_TERM_ID]
    total_value, valid_sum = valid_list_sum(practices)
    return {
        'level': 'error',
        'dataPath': f".{list_key}",
        'message': 'all values must be numbers'
    } if not valid_sum else len(practices) == 0 or total_value == 100 or {
        'level': 'error',
        'dataPath': f".{list_key}",
        'message': f"the sum of all {PASTURE_GRASS_TERM_ID} values must be 100",
        'params': {
            'expected': 100,
            'current': total_value
        }
    }


def validate_has_pastureGrass(data: dict, site: dict, list_key: str = 'practices'):
    site_type = site.get('siteType')
    has_practice = find_term_match(data.get(list_key, []), PASTURE_GRASS_TERM_ID, None) is not None
    return site_type not in [
        SiteSiteType.PERMANENT_PASTURE.value
    ] or has_practice or {
        'level': 'warning',
        'dataPath': f".{list_key}",
        'message': f"should add the term {PASTURE_GRASS_TERM_ID}"
    }
