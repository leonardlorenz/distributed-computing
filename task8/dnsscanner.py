import dns.resolver
import sys

domain = sys.argv[1]

print("Mail-Server:")
try:
    answers = dns.resolver.query(domain,'MX')
    for server in answers:
        print (server.exchange)
except Exception:
    pass
finally:
    print("")
    try:
        print("DNS-Server:")
        answers = dns.resolver.query(domain,'NS')
        for server in answers:
            print (server)
    except Exception:
        pass
    finally:
        print("")
        print("Web-Server:")
        domainWeb = "www." + domain
        try:
            answersWeb = dns.resolver.query(domainWeb,'A')
            for server in answersWeb:
                print (server)
        except Exception:
            pass
        finally:
            print("")