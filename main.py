import src.arguments

def main():
    parse = src.arguments.create_parse()
    args = parse.parse_args()

    NETPLAN_FILE = '/etc/netplan/00-installer-config.yaml'
    


if __name__ == '__main__':
    main()