import dns.resolver


class DNSDetect(object):
    def __init__(self, domain):
        self.domain = domain

    def a(self):
        A = dns.resolver.resolve(self.domain, 'A')             # 指定查询类型为A记录
        for i in A.response.answer:
            for j in i.items:
                print(j.address)

    def mx(self):
        try:
            MX = dns.resolver.resolve(self.domain, 'MX')
        except dns.resolver.NoAnswer:
            print(f'{self.domain}没有MX记录')
            return False
        for i in MX:
            print(i)
        return True

    def ns(self):
        """只限一级域名"""
        ns = dns.resolver.resolve(self.domain, 'NS')
        for i in ns.response.answer:
            for j in i.items:
                print(j.to_text())

    def cname(self):
        cname = dns.resolver.resolve(self.domain, 'CNAME')
        for i in cname.response.answer:
            for j in i.items:
                print(j.to_text())



if __name__ == '__main__':
    domain = input('Please input an domain: ')
    obj = DNSDetect(domain)
    obj.cname()
