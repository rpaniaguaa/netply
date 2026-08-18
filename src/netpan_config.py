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

    def dhcp_conf(self):

        if os.path.getsize(self.NETPLAN_FILE) == 0:
            self.data = self.__create_structure()
        
        self.data['network']['ethernets'][self.args.interface] = {'dhcp4':True}

        with open(self.NETPLAN_FILE,'w',encoding="utf-8") as file:
            yaml.safe_dump(
                self.data,
                file,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

