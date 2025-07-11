import logging
import typing
from time import time
from typing import overload

import xmltodict
from lxml import etree


logger = logging.getLogger(__name__)
VIRTA_NAMESPACE = "{urn:mace:funet.fi:virta/2015/09/01}"


def _load_virta_xml_todict(
    xml_data: typing.IO | bytes,
    force_list: list[str] | None = None
) -> dict:
    if force_list is None:
        force_list = []

    if isinstance(xml_data, bytes):
        return xmltodict.parse(
            xml_data,
            process_namespaces=False,
            namespaces={
                'urn:mace:funet.fi:virta/2015/09/01': None,
                'http://www.w3.org/2001/XMLSchema': None,
                'http://www.w3.org/2001/XMLSchema-instance': None
            },
            force_list=force_list
        )

    return xmltodict.parse(
        xml_data.read(),
        process_namespaces=False,
        namespaces={
            'urn:mace:funet.fi:virta/2015/09/01': None,
            'http://www.w3.org/2001/XMLSchema': None,
            'http://www.w3.org/2001/XMLSchema-instance': None
        }
    )


@overload
def parse_virtafile_to_dict(
    input_file: typing.IO | str,
    tag: str,
    keytag_or_key_gen_func: typing.Callable,
    force_list: list[str] | None = None
) -> tuple[dict, dict]:
    ...


@overload
def parse_virtafile_to_dict(
    input_file: typing.IO | str,
    tag: str,
    keytag_or_key_gen_func: str,
    func: typing.Callable | None = None,
    force_list: list[str] | None = None
) -> tuple[dict, dict]:
    ...


tag_to_force_list_defaults = {
    'Opintosuoritus': [
        'Organisaatio',
        'Koulutusala',
        'Sisaltyvyys',
        'Patevyys',
        'Luokittelu',
    ]
}


def parse_virtafile_to_dict(
    input_file: typing.IO | str,
    tag: str,
    keytag_or_key_gen_func: str | typing.Callable,
    func: typing.Callable | None = None,
    force_list: list[str] | None = None,
) -> tuple[dict, dict]:
    if force_list is None and tag in tag_to_force_list_defaults:
        force_list = tag_to_force_list_defaults[tag]

    if force_list is None:
        force_list = []

    start = time()
    logger.info(f"Starting load and processing of {input_file}")

    tree = etree.parse(input_file)

    result = {}
    metadata = {
        'total_count': 0
    }
    for elem in tree.getiterator(VIRTA_NAMESPACE + tag):
        metadata['total_count'] += 1
        xml_to_dict = _load_virta_xml_todict(etree.tostring(elem), force_list=force_list)
        node = xml_to_dict[tag]
        changes = {}
        poppable_keys = ['@xmlns', '@xmlns:xsd', '@xmlns:xsi']
        for key, values in node.items():
            if len(values) == 2 and "#text" in values:
                values_no_text = [x for x in values.keys() if x != '#text']
                compiled_key = f'{key}.{".".join([values[x] for x in values_no_text])}'
                changes[f'X-{compiled_key}'] = values['#text']
            elif isinstance(values, dict):
                diu = {
                    f'X-{key}.{subkey}': values[subkey]
                    for subkey in values.keys()
                }
                changes = changes | diu
                poppable_keys.append(key)
        node = node | changes
        for pop_key in poppable_keys:
            node.pop(pop_key, None)

        try:
            if isinstance(keytag_or_key_gen_func, typing.Callable):
                _key = keytag_or_key_gen_func(node)
                result[_key] = node
                continue

            if keytag_or_key_gen_func in node:
                if not func:
                    _key = node[keytag_or_key_gen_func]
                    result[_key] = node
                    continue

                if func(node[keytag_or_key_gen_func]):
                    _key = func(node[keytag_or_key_gen_func])
                    result[_key] = node
                else:
                    continue
            else:
                raise Exception("Wtf yhyy", node)
            continue
        except Exception as e:
            print(f"Exception {e} at", node)
    end = time()
    logger.info(f"Finished load and processing of {input_file} in {end - start} seconds")

    return result, metadata
