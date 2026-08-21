import yaml
import subprocess
class NetplanConf:
    def __init__(self,args,NETPLAN_FILE):
        self.args = args
        self.NETPLAN_FILE = NETPLAN_FILE
        try:
            with open(NETPLAN_FILE, "r", encoding="utf-8") as archivo:
                self.data = yaml.safe_load(archivo) or {}
        except yaml.YAMLError :
            raise ValueError(f"Sintax error in YAML file: '{self.NETPLAN_FILE}', please fix it manually")

        
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

    def __correct_sintax_yaml(self):
        
        with open(self.NETPLAN_FILE,'r',encoding="utf-8") as file:
            self.data = yaml.safe_load(file)
            
        if self.data['network'] is None:
            self.data['network']= {'version':2,'ethernets':{}}

        if self.data['network'].get('version') is None:
            self.data['network']['version'] = 2

        if self.data['network'].get('ethernets') is None:
            self.data['network']['ethernets'] = {}

           
    def dhcp_conf(self):
        if self.__is_empty_file():
            self.data = self.__create_structure()
        else:
            self.__correct_sintax_yaml()      

        self.data['network']['ethernets'][self.args.interface] = {'dhcp4':True}
        self.__edit_yaml_file()


    def static_conf(self):

        if self.args.gateway and (self.args.to != 'default' or self.args.via):
            print("error: argument --gateway cannot be used with --to or --via")
            exit(3)

        if self.__is_empty_file():
            self.data = self.__create_structure()
        else:
            self.__correct_sintax_yaml()


        if self.args.interface not in self.data['network']['ethernets']:
            self.data['network']['ethernets'].update({self.args.interface:{}})

        if self.args.address:
            static_address = {'dhcp4':False,'addresses': [self.args.address]}
            self.data['network']['ethernets'][self.args.interface].update(static_address)

        if self.args.dns_addresses:
            dns = {'addresses':self.args.dns_addresses if isinstance(self.args.dns_addresses, list) else [self.args.dns_addresses]}

            if 'nameservers' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['nameservers'] = dns

            else:
                self.data['network']['ethernets'][self.args.interface]['nameservers'].update(dns)

        if self.args.search:
            dns_search = {'search':self.args.search if isinstance(self.args.search, list) else [self.args.search]}
            
            if 'nameservers' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['nameservers'] = dns_search

            else:
                self.data['network']['ethernets'][self.args.interface]['nameservers'].update(dns_search)

        if self.args.gateway:
            gateway = {'gateway4': self.args.gateway}
            self.data['network']['ethernets'][self.args.interface].update(gateway)


        if self.args.via:
            dest = [{'to': self.args.to,'via': self.args.via}]

            if dest[0].get('to') is None:
                print("error: missing required argument pairing")
                print("  Both '--to' (destination) and '--via' (gateway) must be specified together.")    
                print("  Alternatively, you can specify only a default gateway using '--via' alone.")    
                exit(3)
            
            if 'routes' not in self.data['network']['ethernets'][self.args.interface]:
                self.data['network']['ethernets'][self.args.interface]['routes'] = dest
            
            if dest[0] not in self.data['network']['ethernets'][self.args.interface]['routes']:
                self.data['network']['ethernets'][self.args.interface]['routes'].append(dest[0])

            
        self.__edit_yaml_file()

    def netplan_apply(self):
        args=['sudo','netplan','apply']
        subprocess.run(args,text=True)
        

