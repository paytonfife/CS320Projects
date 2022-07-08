from bisect import bisect
import netaddr
import re
import pandas as pd

ips = pd.read_csv("ip2location.csv")

def lookup_region(ip):
    global ips
    ip_replaced = re.sub(r'[a-z]', '0', ip)
    int_ip = int(netaddr.IPAddress(ip_replaced))
    return ips.iloc[(bisect(ips['low'], int_ip)) - 1][3]

class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"20\d{2}-\d{2}-\d{2}|19\d{2}-\d{2}-\d{2}", html)
        sic = re.findall(r"SIC=\D*(\d*)", html)
        if sic == []:
            self.sic = None
        else:
            self.sic = int(sic[0])
        self.addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):  
                line2 = line.strip()
                if line2 != '':
                    lines.append(line2)
            address = "\n".join(lines)
            self.addresses.append(address)
            if self.addresses[-1] == '':
                self.addresses.pop(-1)
        
    def state(self):
        for line in self.addresses:
            state = re.findall(r"([A-Z]{2}) \d{5}", line)
            if state == []:
                continue
            else:
                break
        if state == []:
            return None
        else:
            return state[0]