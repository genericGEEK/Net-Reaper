import harvesters.dnac
import harvesters.netbrain
import harvesters.akips
from helpers.helpers import *
from config.config import *


def main():
    dnac_count = 0
    results_filtered_list_of_dict = []
    to_csv = 'export/name_of_report_' + today + '.csv'

    # DNAC API call and parsing
    print_call('DNAC')
    with harvesters.dnac.DnacAPI() as dnac:
        dnac.login(username=DNAC_USER, passwd=DNAC_PASS)
        response = dnac.get('/dna/intent/api/v1/device-detail')
        for this_entity in response['response']:
            output = serial_parse(this_entity, nms='dnac')
            if output is not None:
                dnac_count += 1
                results_filtered_list_of_dict.append(output)
    print_records(dnac_count)

    # List comprehension to remove any duplicates
    res = []
    [res.append(x) for x in results_filtered_list_of_dict if x not in res]
    # Write to CSV
    total_count = dnac_count
    header = ['hostname', 'serial', 'model', 'family']
    write_to_csv(to_csv, res, header, total_count, is_header='yes')

    # List Comprehension only works if the whole line is a duplicate, so I used pandas and wrote
    # another function to look for duplicate serial numbers that could have a different hostname
    # i.e. some of our Nexus devices have virtual switches so different hostnames will have the same
    # serial number
    dup_serials(to_csv)


if __name__ == '__main__':
    main()
