from subprocess import check_output as cmd
from multiprocessing import Pool as Threads
from global_imports import *
import re
   
def process(proxy_addrs, check_connectivity_func) -> list:
    thread=Threads(processes=25, maxtasksperchild=4)
    prx=''.join(thread.map(check_connectivity_func, (proxy_addrs))).split()
    thread.close()
    return prx

def check_device_connectivity(addr) -> str:
    x='n' if(SYSTEM=='Windows')else 'c'
    try:
        packet=cmd(f'ping -{x} 1 {addr}', timeout=INTERVAL_TIMING).decode('utf-8', 'ignore')
        if((not re.search('host unreachable', packet))and((re.search('Received = ([1-9])', packet)))):
            return f'{addr} '
    except:
        return ''
    return ''
 
#STILL NEEDS SUPPORT fOR LINUX
def local_ip_to_hostname(addr) -> str:
    args=f'ping -a -n 1 {addr}' if(SYSTEM == 'Windows') else f'nmblookup -A {addr}'
    try:
        packet=cmd(args, timeout=INTERVAL_TIMING).decode('utf-8', 'ignore')
        if(not re.search('host unreachable', packet)and(re.search('Received = ([1-9])', packet))):
            device_name=re.search('\s*(Pinging\s[a-zA-z1-9\S.\s]*?)\s', packet).group().replace('Pinging', '').strip()
            return f'{addr}:{device_name} '
    except:
        return ''
    return ''

def local_ip_list() -> tuple:
    ip_list=list()
    try:
        if(SYSTEM == 'Windows'):
            ip_info=cmd('ipconfig').decode('utf-8')
            try: #IS WI_FI
                packet=re.search('Wireless\s[A-Z]*\s[a-z]*\s[A-Z][a-z]\S[A-Z][a-z][\S\s1-9a-zA-Z]*', ip_info).group()
                ipv4=re.search('\S*?IPv4\s[A-za-z]*[\S\s]*?\s(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[0-9]*)', packet).group().split(':')[1].strip().split()[0]
                subnet=re.search('\S*?Subnet\s[A-Za-z]*[\S\s]*?\s(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[0-9]*)', packet).group().split(':')[1].strip()
                gateway=re.search('\S*?Default\s[A-Za-z]*\s[\S\s]*?\S(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[1-9]*)', packet).group().split()[-1].strip()
            except: #IS ETHERNET
                packet=re.search("\S*?Ethernet\s[a-z]*\s[E-Z][a-z]*\:\s[a-zA-Z1-9\s\S]*",ip_info).group()    
                ipv4=re.search('\S*?IPv4\s[A-za-z]*[\S\s]*?\s(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[0-9]*)', packet).group().split(':')[1].strip().split()[0]
                subnet=re.search('\S*?Subnet\s[A-Za-z]*[\S\s]*?\s(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[0-9]*)', packet).group().split(':')[1].strip()
                gateway=re.search('\S*?Default\s[A-Za-z]*\s[\S\s]*?\S(0?[1-9]*\.0?[0-9]*\.0?[0-9]*\.0?[1-9]*)', packet).group().split()[-1].strip()      
        else: #LINUX  (kali wifi tested)       
            ip_info=cmd('ifconfig').decode('utf-8')
            try:
                ipv4=re.search('\S*?inet\s[1-9\S]*)', ip_info).group().split()[1].strip()
                subnet=re.search('\S*?netmask\s[1-9\S]*)', ip_info).group().split()[1].strip()
                gateway=re.search('\S*?broadcast\s[1-9\S]*)', ip_info).group().split()[1].strip()
            except:
                raise Exception            
    except Exception as e:
        raise e
    else:
        ###identify network class and appropriate the ip scan list. 
        ###overload scan function or accept additional parameter to specify the iterations of an exterior loop.
        sub=subnet.split('.')
        type = 'Class D'
        if(sub[3] < 255):
            type = 'Class C'
            oct_iters = 1
        if(sub[2] < 255):
            type = 'Class B'
            oct_iters = 2
        if(sub[1] < 255):
            type = 'Class A'
            oct_iters = 3
       
        octs=ipv4.split('.')
        [ip_list.append(str(f'{octs[0]}.{octs[1]}.{octs[2]}.{x}')) for x in range(0,256)]
        return (ip_list, subnet, gateway, ipv4)
    
def get_local_live_ips() -> list:
    class_A = '255.0.0.0'
    class_B = '255.255.0.0'
    class_C = '255.255.255.0'
    class_D = '255.255.255.255'
    try:
        (proxy_list, subnet, gateway, ipv4)=local_ip_list()
    except Exception as e:
        raise e
    else:
        if(not((subnet == class_A) or (subnet == class_B) or (subnet == class_C) or (subnet == class_D ))):
            print(f'{YELLOW}Segmented submask found.{YELLOW}')
        print(f'{YELLOW}{str.ljust("IPv4 Address: ",20,".")}{CYAN}{str.rjust(ipv4,15)}')
        print(f'{YELLOW}{str.ljust("Default Gateway: ",20,".")}{CYAN}{str.rjust(gateway,15)}')
        print(f'{YELLOW}{str.ljust("Subnet Mask: ",20,".")}{CYAN}{str.rjust(subnet,15)}')
        return proxy_list

def print_prx(prx):
    print(f'{chr(0x0a)}{YELLOW}RETURNED:  {CYAN}{len(prx)}{chr(0x0a)}{[x for x in prx]}{YELLOW}')

def import_file() -> list:
    filename = str(input(f'Enter the filename and the extension of the import file: {MAGENTA}')) 
    try:         
        with open(filename, mode='r') as fhandle:
            proxy_list = fhandle.read().split()
        fhandle.close()
        return proxy_list
    except Exception as e:
        print(f'{RED}file {filename} does not exist in the directory.{YELLOW}')
        raise e

def write_prx(prx):
    outfile = input(f'{YELLOW}Save as: {MAGENTA}')
    outfile = re.sub(r'\.txt$', '', outfile)
    if(not outfile.endswith('.txt')):
        outfile += '.txt'
    with open(outfile, mode='a+') as fhandle:
        for i, x in enumerate(prx, start=0):
            fhandle.seek(0, 0)
            if(not re.search(x, fhandle.read())):
                fhandle.write(f'{x}\n')
    print(f'{GREEN}{outfile} saved.{YELLOW}')
