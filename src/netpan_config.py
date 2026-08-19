import yaml
import os

class NetplanConf:
    def __init__(self,args,NETPLAN_FILE):
        self.args = args
        self.NETPLAN_FILE = NETPLAN_FILE
        try:
            with open(NETPLAN_FILE, "r", encoding="utf-8") as archivo:
                self.data = yaml.safe_load(archivo) or {}
        except yaml.YAMLError as err:
            raise ValueError(f"Sintax error in YAML file: {err}")

        
    def __create_structure(self):
        init_conf = {
            'network': {
                'version': 2, 
                'ethernets': {

                }    
            }
        }
        return init_conf

    def __is_empty_file(self):
        with open(self.NETPLAN_FILE,'r',encoding="utf-8") as file:
            return not file.read(1).strip()

    def __edit_yaml_file(self):
        with open(self.NETPLAN_FILE,'w',encoding="utf-8") as file:
            yaml.safe_dump(
                self.data,
                file,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    def dhcp_conf(self):
        if self.__is_empty_file():
            self.data = self.__create_structure()
        
        self.data['network']['ethernets'][self.args.interface] = {'dhcp4':True}
        self.__edit_yaml_file()


    def static_conf(self):

        if self.args.gateway and (self.args.to != 'default' or self.args.via):
            print("error: argument --gateway cannot be used with --to or --via")
            exit(3)

        if self.__is_empty_file():
            self.data = self.__create_structure()

        if self.args.interface not in self.data['network']['ethernets']:
            self.data['network']['ethernets'].update({self.args.interface:{}})

        if self.args.address:
            static_address = {'dhcp4':False,'addresses': [self.args.address]}
            self.data['network']['ethernets'][self.args.interface].update(static_address)

        if self.args.dns_addresses:
            dns = {'addresses':self.args.dns_addresses if isinstance(self.args.dns_addresses, list) else [self.args.dns_addresses]}

            if 'nameserver' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['nameserver'] = dns

            else:
                self.data['network']['ethernets'][self.args.interface]['nameserver'].update(dns)

        if self.args.search:
            dns_search = {'search':self.args.search if isinstance(self.args.search, list) else [self.args.search]}
            
            if 'nameserver' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['nameserver'] = dns_search

            else:
                self.data['network']['ethernets'][self.args.interface]['nameserver'].update(dns_search)

        if self.args.gateway:
            gateway = {'gateway4': self.args.gateway}
            self.data['network']['ethernets'][self.args.interface].update(gateway)

        if self.args.to and self.args.via:
            route = [{'to': self.args.to,'via':self.args.via}]

            if 'routes' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['routes'] = route
            
            else:
                self.data['network']['ethernets'][self.args.interface]['routes'].update(route)
        else:
                print("error: missing required argument pairing")
                print("  Both '--to' (destination) and '--via' (gateway) must be specified together.")

            
        self.__edit_yaml_file()
        

