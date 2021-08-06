from zabbix_api import ZabbixAPI,Already_Exists
import csv
import sys
import time

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

def procurando_templates(nome_template):
    id = zapi.template.get({
        "output": ['name', 'templateid'],
        "search": {"name": '*' + nome_template + '*'},
        "searchWildcardsEnabled": True
    })
    if id:
        print("***Templates encontrados***")
        print()
        for x in id:
            print (x['templateid'], "-", x['name'])
    else:
        print("***Template não encontrado***")
nome_template = input("Pesquise nome de um template não precisa ser completo: ")
print()
procurando_templates(nome_template)
print()
TEMPLATE = input("Insira o templateid...: ")
print ()
def procurando_groupid(nome_group):
    hostgroups = zapi.hostgroup.get({
            "output": ['name','groupid'], 
            "sortfield": "name",
            "search": {"name": '*' + nome_group + '*'},
            "searchWildcardsEnabled": True
    })
    if hostgroups:
        print("***Groups encontrados***")
        print()
        for x in hostgroups:
            print (x['groupid'], "-", x['name'])
    else:
        print("***Group não encontrado***")
nome_group = input("Pesquise nome de um group não precisa ser completo: ")
print()
procurando_groupid(nome_group)
print()
GROUP = input("Insira o groupid...: ")
print()
print('***Listando proxys***')
print()
idproxy = zapi.proxy.get({
    "output": "extend", 
    "sortfield": "host"
    })
for x in idproxy:
    print (x['proxyid'], "-", x['host'])
print()
PROXY = input("Digite o proxyid caso não utilize insira 0: ")
print()
print("***Tipos de interfaces possíveis: 1 - agent; 2 - SNMP***")
print()
TYPEID = input("Insira o typeid...: ")
print()
print('Aguarde...')
time.sleep(2)
print()

info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "4": {"type": "SNMP", "id": "2", "port": "161"},
}

groupids = [GROUP]
groups = [{"groupid": groupid} for groupid in groupids]
            
def create_host(host, ip):
    try:
        create_host = zapi.host.create({
            "groups": groups,
            "host": host,
            "templates": [{"templateid":TEMPLATE}],
            "proxy_hostid": PROXY,
            "interfaces": {
                "type": info_interfaces[TYPEID]['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces[TYPEID]['port']
}
        })
        print(f'Host cadastrado {host}')
    except Already_Exists:
        print(f'Host(s) já cadastrado {host}')
    except Exception as err:
        print(f'Falha ao cadastrar {err}')
   
with open('hosts.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [nome,ipaddress] in file_csv:
        create_host(host=nome,ip=ipaddress)

zapi.logout()
