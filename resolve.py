# 解析A、NS、CNAME、MX记录
# @input    ip：选定的DNS服务器的ip
# @input    domain：需要查询的域名
# @input    dns_type：DNS记录类型
# @output   res：解析结果数组
# @output   res_pre：解析结果（优先级）
# @output   res_exc：解析结果（邮件服务器）
import dns.resolver


def resolve(ip, domain, dns_type):
    local_server = dns.resolver.Resolver()
    local_server.nameservers = [ip]                     # 指定本机的DNS服务器
    record = local_server.resolve(domain, dns_type)     # 只有CNAME的域名前要加www，其他不用

    if dns_type == 'A':
        res = []
        for i in record.response.answer:
            for j in i.items:
                res.append(j.address)
        return res

    elif dns_type == 'NS' or dns_type == 'CNAME':
        res = []
        for i in record.response.answer:
            for j in i.items:
                res.append(j.to_text())
        return res

    elif dns_type == 'MX':
        res_pre = []
        res_exc = []
        for i in record:
            res_pre.append(i.preference)    # 优先级
            res_exc.append(i.exchange)      # 邮件服务器
        return res_pre, res_exc
