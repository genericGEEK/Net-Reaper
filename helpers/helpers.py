import csv
import pandas as pd
from threading import Lock
from config.config import DOMAIN_STRIP_DICT


def base_url(host):
    """
    Helper function to create an endpoint URL
    """
    return 'https://{}/'.format(host)


def strip_hostname(hostname):
    new_hostname = hostname
    for sub, rep in DOMAIN_STRIP_DICT.items():  # Dictionary of fqdn domains to strip from hostname
        if sub in hostname:
            new_hostname = hostname.replace(sub, rep)
        else:
            continue
    return new_hostname


def strip_value(value):
    if value is not None and "," in value:
        new_value = value.split(', ', 1)[0]
    else:
        new_value = value
    return new_value


def strip_port(value):
    new_value = value
    if value is not None:
        new_value = value.replace('Port:', '').replace(')', '')
    return new_value


def serial_parse(records, nms=None, family=None, location=None):
    skip = 'no'
    if nms == 'dnac':
        if 'hostname' in records:
            hostname = strip_hostname(records['hostname']).lower()
            if 'vrt' in hostname or '-vg' in hostname:
                skip = 'yes'
        else:
            hostname = 'Missing'
        if 'serialNumber' in records:
            serial = strip_value(records['serialNumber'])
        else:
            serial = 'Missing'
        if 'platformId' in records:
            model = strip_value(records['platformId'])
        else:
            model = 'Missing'
        if 'family' in records:
            family = records['family']
        else:
            family = 'Missing'
    elif nms == 'netbrain':
        if 'name' in records['attributes']:
            hostname = strip_hostname(records['attributes']['name']).lower()
        else:
            hostname = 'Missing'
        if 'sn' in records['attributes']:
            serial = strip_value(records['attributes']['sn'])
        else:
            serial = 'Missing'
        if 'model' in records['attributes']:
            model = strip_value(records['attributes']['model'])
        else:
            model = 'Missing'
        family = family
        location = location
    elif nms == 'akips':
        if 'name' in records:
            hostname = strip_hostname(records['name'])
        else:
            hostname = 'Missing'
        if 'serial' in records:
            serial = strip_value(records['serial'])
        else:
            serial = 'Missing'
        if 'model' in records:
            model = strip_value(records['model'])
        else:
            model = 'Missing'
        family = family
        location = location
    else:
        hostname = 'Missing'
        serial = 'Missing'
        model = 'Missing'
        family = 'Missing'
        location = 'Missing'
    if skip == 'no':
        results_dict = {'hostname': hostname, 'serial': serial, 'model': model, 'family': family, 'location': location}
        return results_dict


def create_csv_header(to_csv, header):
    with open(to_csv, 'a', newline='') as output_csv:
        csv_writer = csv.DictWriter(output_csv, fieldnames=header)
        csv_writer.writeheader()


def write_csv_threads(to_csv, res, header):
    with open(to_csv, 'a', newline='') as output_csv:
        csv_writer = csv.DictWriter(output_csv, fieldnames=header)
        for entry in res:
            csv_writer.writerow(entry)


def write_to_csv(to_csv, res, header, total_cnt, is_header='no'):
    with open(to_csv, 'a', newline='') as output_csv:
        csv_writer = csv.DictWriter(output_csv, fieldnames=header)
        if is_header == 'yes':
            csv_writer.writeheader()
        for entry in res:
            csv_writer.writerow(entry)
    print('--------------------------------------------------------------')
    print('Successfully wrote {} devices to CSV file'.format(total_cnt))


def dup_serials(to_csv):
    data = pd.read_csv(to_csv)
    dup_num = data.duplicated(subset='serial').sum()
    result = data.drop_duplicates(subset='serial', keep='first')
    result.to_csv(to_csv, index=False, header=False)
    print('Successfully removed {} duplicate serial numbers from CSV file'.format(dup_num))


def print_region_success(key):
    print('--------------------------------------------------------------')
    print('')
    print('================== ' + key + ' Complete ===================')
    print('')
    print('')


def print_region_start(key):
    print('')
    print('================== ' + key + ' Starting ===================')
    print('')


def print_call(nms):
    print('--------------------------------------------------------------')
    print('Requested API Call for ' + nms + ' Devices')

def print_records(count):
    print('Processed {} entity records'.format(count))
