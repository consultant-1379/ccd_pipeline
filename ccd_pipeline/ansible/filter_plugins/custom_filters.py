import ipaddress

class FilterModule(object):
    ''' IPv6 address expansion filter '''

    def filters(self):
        return {
            'custom_expand_ipv6': self.custom_expand_ipv6
        }

    def custom_expand_ipv6(self, ipv6_address):
        try:
            expanded_address = str(ipaddress.IPv6Address(ipv6_address).exploded)
            return expanded_address
        except ipaddress.AddressValueError as e:
            raise ValueError(f"Failed to expand IPv6 address: {e}")