import src.arguments
import src.commands
import sys
from src.netpan_config import NetplanConf

def apply_changes():
    return input("Are you sure you want to apply changes [S/N]?: ").upper() == 'S'

def main():
    NETPLAN_FILE = '/etc/netplan/00-installer-config.yaml'
    
    if not src.commands.is_root():
        print("error: cannot access file: permission denied")
        sys.exit(1)
    
    if not src.commands.exists_netplan_config(NETPLAN_FILE):
        print(f"error: '{NETPLAN_FILE}' does not exists")
        sys.exit(2)
        
    parse = src.arguments.create_parse()
    args = parse.parse_args()
    netplan = NetplanConf(args,NETPLAN_FILE)
    static_args = any([
        args.address is not None,
        args.dns_addresses is not None,
        args.search is not None, 
        args.gateway is not None,
        args.to != 'default',
        args.via is not None       
    ])
    
    if args.type == 'dhcp' and static_args:
        print("error: 'dhcp' cannot be used with any static parameter")
        sys.exit(3)

    if args.type == 'static' and not static_args:
        print("error: 'static' requires at least another static parameter")
        sys.exit(3)

    
    if args.type == 'dhcp' and  args.force:
        netplan.dhcp_conf()
        netplan.netplan_apply()

    elif args.type == 'dhcp' and apply_changes():
        netplan.dhcp_conf()
        netplan.netplan_apply()

    if args.type == 'static' and args.force:
        netplan.static_conf()
        netplan.netplan_apply()

    elif args.type == 'static' and static_args and apply_changes():
        netplan.static_conf()
        netplan.netplan_apply()


if __name__ == '__main__':
    main()