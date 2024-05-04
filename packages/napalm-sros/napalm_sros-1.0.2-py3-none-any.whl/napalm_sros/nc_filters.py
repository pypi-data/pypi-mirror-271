# NETCONF filters

# -*- coding: utf-8 -*-
# © 2020-2023 Nokia
# Licensed under the Apache License 2.0 License
# SPDX-License-Identifier: Apache-2.0


GET_FACTS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <chassis>
                <hardware-data>
                    <serial-number/>
                </hardware-data>
            </chassis>
            <system>
                <oper-name />
                <up-time />
                <platform />
                <version>
                    <version-number/>
                </version>
            </system>
            <router>
                <interface>
                    <interface-name />
                </interface>
            </router>
        </state>
    </filter>
    """
}


def GET_INTERFACES(R19):
  return f"""
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <port>
                <port-id></port-id>
                <oper-state />
                <hardware-mac-address />
                <ethernet>
                    <oper-speed />
                </ethernet>
            </port>
            <router>
                <interface>
                    <oper-ip-mtu />
                    { '<if-oper-status/>' if R19 else '<oper-state/>' }
                    <last-oper-change/>
                </interface>
            </router>
            <chassis>
                <hardware-data>
                    <base-mac-address/>
                </hardware-data>
            </chassis>
        </state>
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <port>
                <port-id></port-id>
                <description />
                <ethernet>
                    <mtu />
                </ethernet>
                <admin-state />
            </port>
            <router>
                <interface>
                    <admin-state />
                    <description />
                    <mac />
                    <port/>
                    <loopback/>
                </interface>
            </router>
        </configure>
    </filter>
    """

GET_INTERFACES_COUNTERS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <port>
                <statistics>
                    <out-errors />
                    <in-errors />
                    <out-discards />
                    <in-discards />
                    <out-octets />
                    <in-octets />
                    <out-unicast-packets />
                    <in-unicast-packets />
                    <out-multicast-packets />
                    <in-multicast-packets />
                    <out-broadcast-packets />
                    <in-broadcast-packets />
                </statistics>
            </port>
            <router>
                <interface>
                    <statistics>
                        <ip>
                            <out-discard-packets />
                            <out-octets />
                            <in-octets />
                        </ip>
                    </statistics>
                </interface>
            </router>
        </state>
    </filter>
    """
}

GET_NETWORK_INSTANCES = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <router>
                <router-name>{instance_name}</router-name>
                <interface>
                    <interface-name/>
                </interface>
            </router>
            <service>
                <vprn>
                    <service-name>{instance_name}</service-name>
                    <oper-route-distinguisher/>
                    <interface>
                        <interface-name/>
                    </interface>
                </vprn>
                <vpls>
                    <service-name>{instance_name}</service-name>
                    <interface>
                        <interface-name/>
                    </interface>
                </vpls>
            </service>
        </state>
    </filter>
    """
}

GET_OPTICS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <port>
                <port-id/>
                <transceiver>
                    <digital-diagnostic-monitoring>
                        <lane>
                            <lane-id/>
                            <received-optical-power>
                                <current/>
                            </received-optical-power>
                            <transmit-output-power>
                                <current/>
                            </transmit-output-power>
                            <transmit-bias-current>
                                <current/>
                            </transmit-bias-current>
                        </lane>
                    </digital-diagnostic-monitoring>
                </transceiver>
            </port>
        </state>
    </filter>
    """
}

GET_ARP_TABLE = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <router>
                <router-name>{vrf}</router-name>
                <interface>
                    <ipv4>
                        <neighbor-discovery>
                            <neighbor/>
                        </neighbor-discovery>
                    </ipv4>
                </interface>
            </router>
            <service>
                <vprn>
                    <service-name>{vrf}</service-name>
                    <interface>
                        <ipv4>
                            <neighbor-discovery>
                                <neighbor/>
                            </neighbor-discovery>
                        </ipv4>
                    </interface>
                </vprn>
            </service>
        </state>
    </filter>
    """
}

GET_INTERFACES_IP = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <interface>
                    <interface-name/>
                    <ipv4>
                        <primary>
                            <address/>
                            <prefix-length/>
                        </primary>
                        <secondary>
                            <address/>
                            <prefix-length/>
                        </secondary>
                    </ipv4>
                    <ipv6>
                        <address>
                            <ipv6-address/>
                            <prefix-length/>
                        </address>
                    </ipv6>
                </interface>
            </router>
            <service>
                <vprn>
                    <service-name/>
                    <interface>
                        <interface-name/>
                        <ipv4>
                            <primary>
                                <address/>
                                <prefix-length/>
                            </primary>
                            <secondary>
                                <address/>
                                <prefix-length/>
                            </secondary>
                        </ipv4>
                        <ipv6>
                            <address>
                                <ipv6-address/>
                                <prefix-length/>
                            </address>
                        </ipv6>
                    </interface>
                </vprn>
            </service>
        </configure>
    </filter>
    """
}

GET_NTP_PEERS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <system>
                <time>
                    <ntp>
                        <peer>
                            <ip-address/>
                        </peer>
                    </ntp>
                </time>
            </system>
        </state>
    </filter>
    """
}

GET_NTP_SERVERS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <system>
                <time>
                    <ntp>
                        <server>
                            <ip-address/>
                        </server>
                    </ntp>
                </time>
            </system>
        </state>
    </filter>
    """
}

GET_SNMP_INFORMATION = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <system>
                <name/>
                <location/>
                <contact/>
                <security>
                    <snmp>
                        <community>
                            <community-string/>
                            <source-access-list/>
                            <access-permissions/>
                        </community>
                    </snmp>
                </security>
            </system>
        </configure>
    </filter>
    """
}

GET_USERS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <system>
                <security>
                    <aaa>
                        <local-profiles>
                            <profile>
                                <user-profile-name/>
                            </profile>
                        </local-profiles>
                    </aaa>
                    <user-params>
                        <local-user>
                            <user>
                                <user-name/>
                                <password/>
                                <console>
                                    <member/>
                                </console>
                                <public-keys>
                                    <rsa>
                                        <rsa-key>
                                            <key-value/>
                                        </rsa-key>
                                    </rsa>
                                </public-keys>
                            </user>
                        </local-user>
                    </user-params>
                </security>
            </system>
        </configure>
    </filter>
    """
}

GET_ROUTE_TO = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <router>
                <router-name/>
                <bgp>
                    <neighbor/>
                </bgp>
            </router>
            <service>
                <vprn>
                    <oper-service-id/>
                    <bgp>
                        <neighbor/>
                    </bgp>
                </vprn>
            </service>
        </state>
    </filter>
    """
}

GET_PROBES_CONFIG = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <saa>
                <owner>
                    <owner-name/>
                    <test/>
                    <type>
                        <icmp-ping>
                            <destination-address/>
                            <count/>
                            <source-address/>
                            <interval/>
                        </icmp-ping>
                    </type>
                </owner>
            </saa>
        </configure>
    </filter>
    """
}

GET_BGP_CONFIG = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <autonomous-system/>
                <bgp>
                    <description/>
                    <apply-groups/>
                    <multihop/>
                    <local-as>
                        <as-number/>
                    </local-as>
                    <remove-private/>
                    <cluster>
                        <cluster-id/>
                    </cluster>
                    <multipath>
                     <ebgp/>
                     <ibgp/>
                    </multipath>
                    <client-reflect/>
                    <group>
                        <group-name>{group_name}</group-name>
                        <description/>
                        <type/>
                        <apply-groups/>
                        <multihop/>
                        <peer-as/>
                        <local-address/>
                        <next-hop-self/>
                        <client-reflect/>
                        <local-as>
                            <as-number/>
                        </local-as>
                        <import>
                            <policy/>
                        </import>
                        <export>
                            <policy/>
                        </export>
                        <remove-private>
                            <limited/>
                        </remove-private>
                        <prefix-limit>
                            <family/>
                            <maximum/>
                            <threshold/>
                            <idle-timeout/>
                        </prefix-limit>
                    </group>

                    <neighbor>
                        <ip-address>{neighbor}</ip-address>
                        <group/>
                        <type/>
                        <authentication-keychain/>
                        <description/>
                        <peer-as/>
                        <next-hop-self/>
                        <client-reflect/>
                        <local-as>
                            <as-number/>
                        </local-as>
                        <local-address/>
                        <import>
                            <policy/>
                        </import>
                        <export>
                            <policy/>
                        </export>
                        <prefix-limit>
                            <family/>
                            <maximum/>
                            <threshold/>
                            <idle-timeout/>
                        </prefix-limit>
                        <cluster>
                            <cluster-id/>
                        </cluster>
                    </neighbor>
                </bgp>
            </router>
            <service>
                <vprn>
                  <autonomous-system/>
                  <bgp>
                    <description/>
                    <apply-groups/>
                    <multihop/>
                    <local-as>
                        <as-number/>
                    </local-as>
                    <remove-private/>
                    <cluster>
                        <cluster-id/>
                    </cluster>
                    <multipath>
                     <ebgp/>
                     <ibgp/>
                    </multipath>
                    <client-reflect/>
                    <group>
                        <group-name>{group_name}</group-name>
                        <description/>
                        <type/>
                        <apply-groups/>
                        <multihop/>
                        <peer-as/>
                        <local-address/>
                        <next-hop-self/>
                        <local-as>
                            <as-number/>
                        </local-as>
                        <import>
                            <policy/>
                        </import>
                        <export>
                            <policy/>
                        </export>
                        <remove-private/>
                        <prefix-limit>
                            <family/>
                            <maximum/>
                            <log-only/>
                            <threshold/>
                            <idle-timeout/>
                            <post-import/>
                            <apply-groups/>
                        </prefix-limit>
                        <cluster>
                            <cluster-id/>
                        </cluster>
                        <client-reflect/>
                    </group>
                    <neighbor>
                        <ip-address>{neighbor}</ip-address>
                        <group/>
                        <type/>
                        <authentication-keychain/>
                        <description/>
                        <peer-as/>
                        <next-hop-self/>
                        <client-reflect/>
                        <local-as>
                            <as-number/>
                        </local-as>
                        <local-address/>
                        <import>
                            <policy/>
                        </import>
                        <export>
                            <policy/>
                        </export>
                        <prefix-limit>
                            <family/>
                            <maximum/>
                            <log-only/>
                            <threshold/>
                            <idle-timeout/>
                            <post-import/>
                            <apply-groups/>
                        </prefix-limit>
                        <cluster>
                            <cluster-id/>
                        </cluster>
                    </neighbor>
                  </bgp>
                </vprn>
            </service>
        </configure>
    </filter>
    """
}

GET_LLDP_NEIGHBORS = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <port>
                <oper-state/>
                <ethernet>
                    <lldp>
                        <dest-mac>
                            <remote-system>
                                <chassis-id/>
                                <remote-port-id/>
                                <port-description/>
                                <system-name/>
                            </remote-system>
                        </dest-mac>
                    </lldp>
                </ethernet>
            </port>
        </state>
    </filter>
    """
}

GET_LLDP_NEIGHBORS_DETAIL = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <port>
                <port-id>{port_id}</port-id>
                <oper-state/>
                <ethernet>
                    <lldp>
                        <dest-mac>
                            <remote-system>
                                <chassis-id/>
                                <remote-port-id/>
                                <system-name/>
                                <port-description/>
                                <system-description/>
                                <system-supported-capabilities/>
                                <system-enabled-capabilities/>
                            </remote-system>
                        </dest-mac>
                    </lldp>
                </ethernet>
            </port>
        </state>
    </filter>
    """
}
GET_IPV6_NEIGHBORS_TABLE = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <router>
                <router-name/>
            </router>
            <service>
                <vprn>
                    <oper-service-id/>
                </vprn>
            </service>
        </state>
    </filter>
    """
}


GET_ENVIRONMENT = {
    "_": """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <chassis>
                <fan>
                    <fan-slot/>
                    <hardware-data>
                        <oper-state/>
                    </hardware-data>
                </fan>
                <power-shelf>
                    <power-module>
                        <power-module-id/>
                        <available-wattage/>
                        <hardware-data>
                            <oper-state/>
                        </hardware-data>
                    </power-module>
                </power-shelf>
            </chassis>
            <cpm>
                <hardware-data>
                    <temperature/>
                    <temperature-threshold/>
                </hardware-data>
            </cpm>
            <card>
                <hardware-data>
                    <temperature/>
                    <temperature-threshold/>
                </hardware-data>
                <mda>
                    <hardware-data>
                        <temperature/>
                        <temperature-threshold/>
                    </hardware-data>
                </mda>
            </card>
            <system>
                <memory-pools>
                    <summary>
                        <available-memory/>
                        <total-in-use/>
                    </summary>
                </memory-pools>
                <cpu>
                    <summary>
                        <usage>
                            <cpu-usage/>
                        </usage>
                    </summary>
                </cpu>
            </system>
        </state>
    </filter>
    """
}
