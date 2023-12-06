import harvesters.dnac
import harvesters.netbrain
import harvesters.akips
from helpers.helpers import *
from config.config import *


def main():
    # DNAC API call
    with harvesters.dnac.DnacAPI() as dnac:
        dnac.login(username=DNAC_USER, passwd=DNAC_PASS)
        response = dnac.get('dna/intent/api/v1/site/count')
        print (response)
    
    # NetBrain API call
    with harvesters.netbrain.NetbrainAPI() as netbrain:
        netbrain.login()
        response = netbrain.get("")
        print (response)


    # AKIPS API call
    with harvesters.akips.AkipsAPI() as akips:
        response = akips.request("GET",";filename=sp2vlan","api-spm")
        print (response.text)

if __name__ == '__main__':
    main()
