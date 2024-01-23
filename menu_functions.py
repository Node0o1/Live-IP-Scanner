from global_imports import *
import pyfiglet

def banner():
    ascii_banner = pyfiglet.figlet_format('LIVE - IP SCANNER')
    print(f'{CYAN}{chr(0x0a)}{ascii_banner}')
    print(f'{YELLOW}'+str.center('by Node001 and JennyBlve',45),'\n')

def menu_selection() -> str:
    print(f'\n{CYAN}Please choose a scan option ({YELLOW}1-5{CYAN})')
    print(f'{RED}'+str.ljust('',45,'+'))
    print(f'\n{CYAN}  '+str.ljust('Domain/Port ICMP Connectivity Scan',40,'.'),f'{YELLOW}1')
    print(f'\n{CYAN}  '+str.ljust('Local Network Live ICMP Scan',40,'.'),f'{YELLOW}2')
    print(f'\n{RED}*{CYAN} '+str.ljust('Resolve Found Network Device Names',40,'.'),f'{YELLOW}3')
    print(f'\n{CYAN}  '+str.ljust('Exit Proxy IP Scanner',40,'.'),f'{YELLOW}4')
    print(f'\n{RED}'+str.ljust('',45,'+'))
    selection=str(input(f'{CYAN}Selection: {MAGENTA}'))
    print(f'{YELLOW}')
    return selection
