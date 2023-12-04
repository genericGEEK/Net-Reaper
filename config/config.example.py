from datetime import date


# Global Parameters
d1 = date.today()
today = d1.strftime("%m%d%y")


# DNAC Parameters
DNAC_HOST = ''
DNAC_USER = ''
DNAC_PASS = ''

DNAC_WR_GROUP = ''
DNAC_AZ_GROUP = ''
DNAC_TN_GROUP = ''


# AKiPS Parameters
AKIPS_PASS = ''
AKIPS_HOST = ''


# Netbrain Parameters
NETBRAIN_HOST = ''
TENANT_ID = ""
DOMAIN_ID = ""
NETBRAIN_WR_GROUP = ''
NETBRAIN_AZ_GROUP = ''
NETBRAIN_TN_GROUP = ''

SESSION_BODY = {
    "username": "",
    "password": ""
}

DOMAIN_BODY = {
    "tenantId": TENANT_ID,
    "domainId": DOMAIN_ID
}

DOMAIN_STRIP_DICT = {
    '.sub.domain.com': '',
    '.test.domain.com': '',
    '.another.test.domain.com': '',
    '.test.net': ''
}
