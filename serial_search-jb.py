import harvesters.dnac
import harvesters.netbrain
import harvesters.akips
from helpers.helpers import *
from config.config import *
import argparse
import json

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('serial_numbers', help='Valid Serial Numbers separated by commas (no spaces)')
ARGS = parser.parse_args()

serials = ARGS.serial_numbers

def main():
    for s in serials.split(","):
        # DNAC API call
        with harvesters.dnac.DnacAPI() as dnac:
            dnac.login(username=DNAC_USER, passwd=DNAC_PASS)
            response = dnac.get('api/v1/network-device?serialNumber=' + s.strip())
            data = json.loads(str(response))
            resp = data.get('response', [])
            if len(resp) == 0:
                type_value = "Not found"
                hostname_value = "Not found"
            else:
                type_value = resp[0].get('type', 'Not found')
                hostname_value = resp[0].get('hostname', 'Not found')
                
            print (s +"," + type_value + "," + hostname_value)


if __name__ == '__main__':
    main()
