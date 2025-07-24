#!/usr/bin/python3
# This script written to backup and restore F5XC configuration objects 
# It simplify administator to perform periodic backup of configuration for future ref or restore 
# Refer to README for details on what objects it support
# 
# Author: Foo-Bang, Jerald
# Date: 15 Nov 2023
# Note:
#   Example: ./f5xc-backup-restore.py
# - For details on specific resources (use -h for helps)
#   Example: 
#   ./f5xc-backup-restore.py -a backup -n mcn # Backup configuration object in mcn namespace
#   ./f5xc-backup-restore.py -a backup -n arcadia, arcadia-demo # Backup configuration object in arcadia and arcadia-demo namespace
#   ./f5xc-backup-restore.py -a backup -n mcn,shared,system # Backup configuration object in mcn, shared and system namespace
#   ./f5xc-backup-restore.py -a restore -n mcn # Restore configuration object back to mcn namespace
#
#  v1.1 - Release (15 Nov 2023)
# 
import argparse
import requests
# import json
# import base64
import warnings
import sys
import os
import time
import re
import configparser

from datetime import datetime
from zoneinfo import ZoneInfo

warnings.filterwarnings("ignore")

##############################################################################################################################
def get_and_save_conf_object(log_path, backup_path, ns, base_api, items_conf_object, file_format, object_type, sleep_time):
    final_backup_path = backup_path + "/" + ns
    if not os.path.isdir(final_backup_path):
          os.makedirs(final_backup_path)
    if not os.path.isdir(log_path):
          log_path = "./"
    log_file = log_path + '/f5xc-backup-restore.log'
    # Date, job name, namespace, object, start date/time, end data/time, bytes backed up, status, error description
    for item_conf_object in items_conf_object:
       item = item_conf_object['name']
       item_ns = item_conf_object['namespace']
       api_req = base_api +'/' + item
       if item_ns == ns and not (item.startswith('nfv-mgt-ves-io-') or item.startswith('apm-nfv-mgt-op-ves-io-') or item.startswith('ves-io-')):
           payload = ""
           backup_start_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
           response = requests.request("GET", api_req, headers=headers, verify=False)
           backup_end_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
           if response.status_code == 200:
                # item_file = './' + ns + '/' + ns + '_' + file_format + '-' + item + '.json'
                # item_file = final_backup_path + ns + '/' + ns + '_' + file_format + '-' + item + '.json'
                item_file = final_backup_path + '/' + ns + '_' + file_format + '-' + item + '.json'
                with open(item_file,'w', encoding='utf-8') as f:
                    f.write(str(response.text))
  
                in_place_remove_string(item_file)
                log_message = backup_start_utc_now.strftime('%Y-%m-%d UTC') + ',BACKUP,' + ns + ',' + object_type + ',' + backup_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + backup_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + "{:.2f}".format((os.stat(item_file).st_size) / 1024) + ' KB,SUCCESS\n'
                with open(log_file,'a',encoding='utf-8') as lf:
                      lf.write(log_message)
                print(f'\033[0;32m [{ns}] Backing up {object_type} object [{item}] ..... DONE' )
           else:
                log_message = backup_start_utc_now.strftime('%Y-%m-%d UTC') + ',BACKUP,' + ns + ',' + object_type + ',' + backup_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + backup_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',0 KB,FAILED,' + str(response.status_code) +'\n'
                with open(log_file,'a',encoding='utf-8') as lf:
                      lf.write(log_message)
                print(f'\033[0;31m [{ns}] Backing up {object_type} object [{item}] ..... FAILED - status code {response.status_code}') 
       time.sleep(sleep_time)
##############################################################################################################################

def in_place_remove_string(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Search for pattern of "tenant" : "<tenant-id>-xxxx", to remove tenantid dependency for backup configuration object
    prefix = '\"tenant\": \"' + tenant_name
    suffix_char = '\",'
    pattern = re.compile(f'^\s*{re.escape(prefix)}.*{re.escape(suffix_char)}$')
    filtered_lines = [line for line in lines if not pattern.match(line)]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)

##############################################################################################################################


################################################
########## BACKUP FUNCTION #####################
################################################

##########################################
# Function to backup HTTP LB by namespace
##########################################
def backup_http_lb (log_path,backup_path,ns,wait_time):
        api_http_lb = tenant_url + '/api/config/namespaces/' + ns + '/http_loadbalancers'
        req_http_lb = requests.get(api_http_lb, headers=headers, verify=False)
        data_http_lb = req_http_lb.json()
        items_http_lb = data_http_lb['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_http_lb, items_http_lb, 'http_lb', 'HTTP Loadbalancer', wait_time)
################################################

################################################
# Function to backup Origin Pool by namespace
################################################
def backup_origin_pool (log_path,backup_path,ns,wait_time):
        api_origin_pool = tenant_url + '/api/config/namespaces/' + ns + '/origin_pools'
        req_origin_pool = requests.get(api_origin_pool, headers=headers, verify=False)
        data_origin_pool = req_origin_pool.json()
        items_origin_pool = data_origin_pool['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_origin_pool, items_origin_pool, 'origin_pool', 'Origin Pool', wait_time)
################################################

###############################################
# Function to backup Health Check by namespace
###############################################
def backup_healthchecks (log_path,backup_path,ns,wait_time):
        api_healthchecks = tenant_url + '/api/config/namespaces/' + ns + '/healthchecks'
        req_healthchecks = requests.get(api_healthchecks, headers=headers, verify=False)
        data_healthchecks = req_healthchecks.json()
        items_healthchecks = data_healthchecks['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_healthchecks, items_healthchecks, 'healthcheck', 'Health Check', wait_time)
################################################

################################################
# Function to backup App firewalls by namespace
################################################
def backup_app_fw (log_path,backup_path,ns,wait_time):
        api_app_fw = tenant_url + '/api/config/namespaces/' + ns + '/app_firewalls'
        req_app_fw = requests.get(api_app_fw, headers=headers, verify=False)
        data_app_fw = req_app_fw.json()
        items_app_fw = data_app_fw['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_app_fw, items_app_fw, 'app_fw', 'App Firewall', wait_time)      
################################################

################################################
# Function to backup Service Policy by namespace
################################################
def backup_service_policy (log_path,backup_path,ns,wait_time):
        api_service_policy = tenant_url + '/api/config/namespaces/' + ns + '/service_policys'
        req_service_policy = requests.get(api_service_policy, headers=headers, verify=False)
        data_service_policy = req_service_policy.json()
        items_service_policy = data_service_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_service_policy, items_service_policy, 'service_policy', 'Service Policy', wait_time)      
################################################

#####################################################
# Function to backup TCP Load Balancer by namespace
#####################################################
def backup_tcp_lb (log_path,backup_path,ns,wait_time):
        api_tcp_lb = tenant_url + '/api/config/namespaces/' + ns + '/tcp_loadbalancers'
        req_tcp_lb = requests.get(api_tcp_lb, headers=headers, verify=False)
        data_tcp_lb = req_tcp_lb.json()
        items_tcp_lb = data_tcp_lb['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_tcp_lb, items_tcp_lb, 'tcp_lb', 'TCP Load Balancer', wait_time)      
################################################

######################################################
# Function to backup Forward Proxy Policy by namespace
######################################################
def backup_fwdproxy_policy (log_path,backup_path,ns,wait_time):
        api_fwdproxy_policy = tenant_url + '/api/config/namespaces/' + ns + '/forward_proxy_policys'
        req_fwdproxy_policy = requests.get(api_fwdproxy_policy, headers=headers, verify=False)
        data_fwdproxy_policy = req_fwdproxy_policy.json()
        items_fwdproxy_policy = data_fwdproxy_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_fwdproxy_policy, items_fwdproxy_policy, 'fwdproxy_policy', 'Forward Proxy', wait_time)      
################################################

######################################################
# Function to backup Rate Limit Policy by namespace
######################################################
def backup_ratelimiter_policy (log_path,backup_path,ns,wait_time):
        api_ratelimiter_policy = tenant_url + '/api/config/namespaces/' + ns + '/rate_limiter_policys'
        req_ratelimiter_policy = requests.get(api_ratelimiter_policy, headers=headers, verify=False)
        data_ratelimiter_policy = req_ratelimiter_policy.json()
        items_ratelimiter_policy = data_ratelimiter_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_ratelimiter_policy, items_ratelimiter_policy, 'ratelimiter_policy', 'Rate Limit', wait_time)      
################################################

###########################################################
# Function to backup Malicious User Mitigation by namespace
###########################################################
def backup_malicioususer_policy (log_path,backup_path,ns,wait_time):
        api_malicioususer_policy = tenant_url + '/api/config/namespaces/' + ns + '/malicious_user_mitigations'
        req_malicioususer_policy = requests.get(api_malicioususer_policy, headers=headers, verify=False)
        data_malicioususer_policy = req_malicioususer_policy.json()
        items_malicioususer_policy = data_malicioususer_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_malicioususer_policy, items_malicioususer_policy, 'malicioususer_policy', 'Malicious User Mitigation', wait_time)      
################################################

############################################################
# Function to backup User Identification Policy by namespace
############################################################
def backup_useridentification_policy (log_path,backup_path,ns,wait_time):
        api_useridentification_policy = tenant_url + '/api/config/namespaces/' + ns + '/user_identifications'
        req_useridentification_policy = requests.get(api_useridentification_policy, headers=headers, verify=False)
        data_useridentification_policy = req_useridentification_policy.json()
        items_useridentification_policy = data_useridentification_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_useridentification_policy, items_useridentification_policy, 'useridentification_policy', 'User Identification', wait_time)      
################################################

################################################
# Function to backup IP Prefix set by namespace
################################################
def backup_ip_prefixset (log_path,backup_path,ns,wait_time):
        api_ip_prefixset = tenant_url + '/api/config/namespaces/' + ns + '/ip_prefix_sets'
        req_ip_prefixset = requests.get(api_ip_prefixset, headers=headers, verify=False)
        data_ip_prefixset = req_ip_prefixset.json()
        items_ip_prefixset = data_ip_prefixset['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_ip_prefixset, items_ip_prefixset, 'ip_prefixset', 'IP Prefix', wait_time)
################################################

################################################
# Function to backup Alert Policy by namespace
################################################
def backup_alert_policy (log_path,backup_path,ns,wait_time):
        api_alert_policy = tenant_url + '/api/config/namespaces/' + ns + '/alert_policys'
        req_alert_policy = requests.get(api_alert_policy, headers=headers, verify=False)
        data_alert_policy = req_alert_policy.json()
        items_alert_policy = data_alert_policy['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_alert_policy, items_alert_policy, 'alert_policy', 'Alert Policy', wait_time)
################################################

################################################
# Function to backup Alert Receiver by namespace
################################################
def backup_alert_receiver (log_path,backup_path,ns,wait_time):
        api_alert_receiver = tenant_url + '/api/config/namespaces/' + ns + '/alert_receivers'
        req_alert_receiver = requests.get(api_alert_receiver, headers=headers, verify=False)
        data_alert_receiver = req_alert_receiver.json()
        items_alert_receiver = data_alert_receiver['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_alert_receiver, items_alert_receiver, 'alert_receiver', 'Alert Receiver', wait_time)
################################################

#####################################################
# Function to backup Global Log Receiver by namespace
#####################################################
def backup_global_log_receiver (log_path,backup_path,ns,wait_time):
        api_global_log_receiver = tenant_url + '/api/config/namespaces/' + ns + '/global_log_receivers'
        req_global_log_receiver = requests.get(api_global_log_receiver, headers=headers, verify=False)
        data_global_log_receiver = req_global_log_receiver.json()
        items_global_log_receiver = data_global_log_receiver['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_global_log_receiver, items_global_log_receiver, 'global_log_receiver', 'Global Log Receiver', wait_time)
################################################

#######################################################
# Function to backup Report Configuration by namespace
#######################################################
def backup_report_conf (log_path,backup_path,ns,wait_time):
        api_report_conf = tenant_url + '/api/report/namespaces/' + ns + '/report_configs'
        req_report_conf = requests.get(api_report_conf, headers=headers, verify=False)
        data_report_conf = req_report_conf.json()
        items_report_conf = data_report_conf['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_report_conf, items_report_conf, 'report_conf', 'Report Configuration', wait_time)
################################################

################################################
# Function to backup API Definition by namespace
################################################
def backup_xc_api_definition (log_path,backup_path,ns,wait_time):
        api_xc_api_definition = tenant_url + '/api/config/namespaces/' + ns + '/api_definitions'
        req_xc_api_definition = requests.get(api_xc_api_definition, headers=headers, verify=False)
        data_xc_api_definition = req_xc_api_definition.json()
        items_xc_api_definition = data_xc_api_definition['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_xc_api_definition, items_xc_api_definition, 'xc_api_definition', 'API Definition', wait_time)
################################################

################################################
# Function to backup TLS Certificate by namespace
################################################
def backup_cert_mgmt (log_path,backup_path,ns,wait_time):
        api_cert_mgmt = tenant_url + '/api/config/namespaces/' + ns + '/certificates'
        req_cert_mgmt = requests.get(api_cert_mgmt, headers=headers, verify=False)
        data_cert_mgmt = req_cert_mgmt.json()
        items_cert_mgmt = data_cert_mgmt['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_cert_mgmt, items_cert_mgmt, 'cert_mgmt', 'TLS Certificate', wait_time)
################################################
   
########################################################
# Function to backup TLS Certificate Chain by namespace
########################################################
def backup_cert_mgmt_chain (log_path,backup_path,ns,wait_time):
        api_cert_mgmt_chain = tenant_url + '/api/config/namespaces/' + ns + '/certificate_chains'
        req_cert_mgmt_chain = requests.get(api_cert_mgmt_chain, headers=headers, verify=False)
        data_cert_mgmt_chain = req_cert_mgmt_chain.json()
        items_cert_mgmt_chain = data_cert_mgmt_chain['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_cert_mgmt_chain, items_cert_mgmt_chain, 'cert_mgmt_chain', 'TLS Certificate Chain', wait_time)
################################################
        
#####################################################
# Function to backup Service Discovery by namespace
#####################################################
def backup_svc_discovery (log_path,backup_path,ns,wait_time):
        api_svc_discovery = tenant_url + '/api/config/namespaces/' + ns + '/discoverys'
        req_svc_discovery = requests.get(api_svc_discovery, headers=headers, verify=False)
        data_svc_discovery = req_svc_discovery.json()
        items_svc_discovery = data_svc_discovery['items']
        get_and_save_conf_object(log_path,backup_path, ns, api_svc_discovery, items_svc_discovery, 'svc_discovery', 'Service Discovery', wait_time)
################################################


##############################################################################################################################
def post_and_write_conf_object(log_path, restore_path, ns, api_url, filename_prefix, object_type, sleep_time):
    final_restore_path = restore_path + '/' + ns
    if not os.path.isdir(log_path):
          log_path = "./"
    log_file = log_path + '/f5xc-backup-restore.log'
    # Date, job name, namespace, object, start date/time, end data/time, bytes backed up, status, error description
    for file_name in os.listdir(final_restore_path):
            if os.path.isfile(os.path.join(final_restore_path, file_name)) and file_name.startswith(filename_prefix):
                with open(os.path.join(final_restore_path, file_name), 'r') as file:
                    post_data = file.read()
                    item_file = final_restore_path + '/' + file_name
                    restore_start_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
                    response = requests.request("POST", api_url, headers=headers, data=post_data, verify=False)
                    restore_end_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
                    if response.status_code == 200:
                        log_message = restore_start_utc_now.strftime('%Y-%m-%d UTC') + ',RESTORE,' + ns + ',' + object_type + ',' + restore_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + restore_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + "{:.2f}".format( (os.stat(item_file).st_size) / 1024 ) + ' KB,SUCCESS\n'
                        with open(log_file,'a',encoding='utf-8') as lf:
                               lf.write(log_message)
                        print(f'\033[0;94m [{ns}] Restoring {object_type} object from file [ {file_name} ] ..... DONE' )
                    else:
                        log_message = restore_start_utc_now.strftime('%Y-%m-%d UTC') + ',RESTORE,' + ns + ',' + object_type + ',' + restore_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + restore_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',0 KB,FAILED,' + str(response.status_code) +'\n'
                        with open(log_file,'a',encoding='utf-8') as lf:
                                lf.write(log_message)
                        print(f'\033[0;31m [{ns}] Restoring {object_type} object from file [ {file_name} ] ..... FAILED - status code {response.status_code}')
    time.sleep(sleep_time)
##############################################################################################################################


#################################################
########## RESTORE FUNCTION #####################
#################################################

################################################
# Function to Restore Health Check by namespace
################################################
def restore_healthchecks (log_path,restore_path,ns,wait_time):
        api_healthchecks = tenant_url + '/api/config/namespaces/' + ns + '/healthchecks'
        filename_prefix = ns + '_healthcheck-'
        post_and_write_conf_object(log_path,restore_path, ns, api_healthchecks, filename_prefix, 'Health Check', wait_time)    
################################################

################################################
# Function to Restore HTTP Loadbalancer by namespace
################################################
def restore_http_lb (log_path,restore_path,ns,wait_time):
        api_http_lb = tenant_url + '/api/config/namespaces/' + ns + '/http_loadbalancers'
        filename_prefix = ns + '_http_lb-'
        post_and_write_conf_object(log_path,restore_path, ns, api_http_lb, filename_prefix, 'HTTP LoadBalancer', wait_time)
################################################

################################################
# Function to Restore origin pool by namespace
################################################
def restore_origin_pool (log_path,restore_path,ns,wait_time):
        api_origin_pool = tenant_url + '/api/config/namespaces/' + ns + '/origin_pools'
        filename_prefix = ns + '_origin_pool-'
        post_and_write_conf_object(log_path,restore_path, ns, api_origin_pool, filename_prefix, 'Origin Pool', wait_time)
################################################

################################################
# Function to Restore TCP LB by namespace
################################################
def restore_tcp_lb (log_path,restore_path,ns,wait_time):
        api_tcp_lb = tenant_url + '/api/config/namespaces/' + ns + '/tcp_loadbalancers'
        filename_prefix = ns + '_tcp_lb-'
        post_and_write_conf_object(log_path,restore_path, ns, api_tcp_lb, filename_prefix, 'TCP LoadBalancer', wait_time)
################################################

################################################
# Function to Restore App Firewall by namespace
################################################
def restore_app_fw (log_path,restore_path,ns,wait_time):
        api_app_fw = tenant_url + '/api/config/namespaces/' + ns + '/app_firewalls'
        filename_prefix = ns + '_app_fw-'
        post_and_write_conf_object(log_path,restore_path, ns, api_app_fw, filename_prefix, 'App Firewall', wait_time)
################################################

##################################################
# Function to Restore Service Policy by namespace
##################################################
def restore_service_policy (log_path,restore_path,ns,wait_time):
        api_service_policy = tenant_url + '/api/config/namespaces/' + ns + '/service_policys'
        filename_prefix = ns + '_service_policy-'
        post_and_write_conf_object(log_path,restore_path, ns, api_service_policy, filename_prefix, 'Service Policy', wait_time)
################################################

########################################################
# Function to Restore Forword Proxy Policy by namespace
########################################################
def restore_fwdproxy_policy (log_path,restore_path,ns,wait_time):
        api_fwdproxy_policy = tenant_url + '/api/config/namespaces/' + ns + '/forward_proxy_policys'
        filename_prefix = ns + '_fwdproxy_policy-'
        post_and_write_conf_object(log_path,restore_path, ns, api_fwdproxy_policy, filename_prefix, 'Forward Proxy Policy', wait_time)
################################################

########################################################
# Function to Restore Rate Limiter Policy by namespace
########################################################
def restore_ratelimiter_policy (log_path,restore_path,ns,wait_time):
        api_ratelimiter_policy = tenant_url + '/api/config/namespaces/' + ns + '/rate_limiter_policys'
        filename_prefix = ns + '_ratelimiter_policy-'
        post_and_write_conf_object(log_path,restore_path, ns, api_ratelimiter_policy, filename_prefix, 'Rate Limiter Policy', wait_time)
################################################

########################################################
# Function to Restore Malicious User Policy by namespace
########################################################
def restore_malicioususer_policy (log_path,restore_path,ns,wait_time):
        api_malicioususer_policy = tenant_url + '/api/config/namespaces/' + ns + '/malicious_user_mitigations'
        filename_prefix = ns + '_malicioususer_policy-'
        post_and_write_conf_object(log_path,restore_path, ns, api_malicioususer_policy, filename_prefix, 'Malicious User Policy', wait_time)
################################################

#################################################
# Function to Restore IP Prefix Set by namespace
#################################################
def restore_ip_prefixset (log_path,restore_path,ns,wait_time):
        api_ip_prefixset = tenant_url + '/api/config/namespaces/' + ns + '/ip_prefix_sets'
        filename_prefix = ns + '_ip_prefixset-'
        post_and_write_conf_object(log_path,restore_path, ns, api_ip_prefixset, filename_prefix, 'IP Prefix', wait_time)
################################################

#####################################################
# Function to Restore API Definition Set by namespace
#####################################################
def restore_xc_api_definition (log_path,restore_path,ns,wait_time):
        api_xc_api_definition = tenant_url + '/api/config/namespaces/' + ns + '/api_definitions'
        filename_prefix = ns + '_xc_api_definition-'
        post_and_write_conf_object(log_path,restore_path, ns, api_xc_api_definition, filename_prefix, 'API Definition', wait_time)
################################################

#############################################################
# Function to Restore User Identification Policy by namespace
#############################################################
def restore_useridentification_policy (log_path,restore_path,ns,wait_time):
        api_useridentification_policy = tenant_url + '/api/config/namespaces/' + ns + '/user_identifications'
        filename_prefix = ns + '_useridentification_policy-'
        post_and_write_conf_object(log_path,restore_path, ns, api_useridentification_policy, filename_prefix, 'User Identification Policy', wait_time)
################################################          


##############################################################################################################################
def delete_conf_object(log_path, ns, base_api, items_conf_object, object_type, sleep_time):
    
    if not os.path.isdir(log_path):
          log_path = "./"
    log_file = log_path + '/f5xc-backup-restore.log'
    # Date, job name, namespace, object, start date/time, end data/time, bytes backed up, status, error description
    for item_conf_object in items_conf_object:
       item = item_conf_object['name']
       item_ns = item_conf_object['namespace']
       api_req = base_api +'/' + item
       if item_ns == ns and not (item.startswith('nfv-mgt-ves-io-') or item.startswith('apm-nfv-mgt-op-ves-io-') or item.startswith('ves-io-')):
           payload = ""
           delete_start_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
           response = requests.request("DELETE", api_req, headers=headers, verify=False)
           delete_end_utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
           if response.status_code == 200:
                log_message = delete_start_utc_now.strftime('%Y-%m-%d UTC') + ',DELETE,' + ns + ',' + item + ',' + object_type + ',' + delete_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + delete_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',SUCCESS\n'
                with open(log_file,'a',encoding='utf-8') as lf:
                      lf.write(log_message)
                print(f'\033[0;32m [{ns}] Deleting {object_type} object [{item}] ..... DONE' )
           else:
                log_message = delete_start_utc_now.strftime('%Y-%m-%d UTC') + ',DELETE,' + ns + ',' + item + ',' + object_type + ',' + delete_start_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',' + delete_end_utc_now.strftime('%Y-%m-%d %H:%M:%S UTC') + ',FAILED,' + str(response.status_code) +'\n'
                with open(log_file,'a',encoding='utf-8') as lf:
                      lf.write(log_message)
                print(f'\033[0;31m [{ns}] Deleting {object_type} object [{item}] ..... FAILED - status code {response.status_code}') 
       time.sleep(sleep_time)
##############################################################################################################################


################################################
######## LIST AND DELETE FUNCTION ##############
################################################

##########################################
# Function to delete HTTP LB by namespace
##########################################
def list_and_delete_http_lb (log_path,ns,wait_time):
        api_http_lb = tenant_url + '/api/config/namespaces/' + ns + '/http_loadbalancers'
        req_http_lb = requests.get(api_http_lb, headers=headers, verify=False)
        data_http_lb = req_http_lb.json()
        items_http_lb = data_http_lb['items']
        delete_conf_object(log_path, ns, api_http_lb, items_http_lb, 'HTTP Loadbalancer', wait_time)
################################################

################################################
# Function to delete Origin Pool by namespace
################################################
def list_and_delete_origin_pool (log_path,ns,wait_time):
        api_origin_pool = tenant_url + '/api/config/namespaces/' + ns + '/origin_pools'
        req_origin_pool = requests.get(api_origin_pool, headers=headers, verify=False)
        data_origin_pool = req_origin_pool.json()
        items_origin_pool = data_origin_pool['items']
        delete_conf_object(log_path, ns, api_origin_pool, items_origin_pool, 'Origin Pool', wait_time)
################################################

###############################################
# Function to delete Health Check by namespace
###############################################
def list_and_delete_healthchecks (log_path,ns,wait_time):
        api_healthchecks = tenant_url + '/api/config/namespaces/' + ns + '/healthchecks'
        req_healthchecks = requests.get(api_healthchecks, headers=headers, verify=False)
        data_healthchecks = req_healthchecks.json()
        items_healthchecks = data_healthchecks['items']
        delete_conf_object(log_path, ns, api_healthchecks, items_healthchecks, 'Health Check', wait_time)
################################################

################################################
# Function to delete App firewalls by namespace
################################################
def list_and_delete_app_fw (log_path,ns,wait_time):
        api_app_fw = tenant_url + '/api/config/namespaces/' + ns + '/app_firewalls'
        req_app_fw = requests.get(api_app_fw, headers=headers, verify=False)
        data_app_fw = req_app_fw.json()
        items_app_fw = data_app_fw['items']
        delete_conf_object(log_path, ns, api_app_fw, items_app_fw, 'App Firewall', wait_time)      
################################################

################################################
# Function to delete Service Policy by namespace
################################################
def list_and_delete_service_policy (log_path,ns,wait_time):
        api_service_policy = tenant_url + '/api/config/namespaces/' + ns + '/service_policys'
        req_service_policy = requests.get(api_service_policy, headers=headers, verify=False)
        data_service_policy = req_service_policy.json()
        items_service_policy = data_service_policy['items']
        delete_conf_object(log_path, ns, api_service_policy, items_service_policy, 'Service Policy', wait_time)      
################################################

#####################################################
# Function to delete TCP Load Balancer by namespace
#####################################################
def list_and_delete_tcp_lb (log_path,ns,wait_time):
        api_tcp_lb = tenant_url + '/api/config/namespaces/' + ns + '/tcp_loadbalancers'
        req_tcp_lb = requests.get(api_tcp_lb, headers=headers, verify=False)
        data_tcp_lb = req_tcp_lb.json()
        items_tcp_lb = data_tcp_lb['items']
        delete_conf_object(log_path, ns, api_tcp_lb, items_tcp_lb, 'TCP Load Balancer', wait_time)      
################################################

######################################################
# Function to delete Forward Proxy Policy by namespace
######################################################
def list_and_delete_fwdproxy_policy (log_path,ns,wait_time):
        api_fwdproxy_policy = tenant_url + '/api/config/namespaces/' + ns + '/forward_proxy_policys'
        req_fwdproxy_policy = requests.get(api_fwdproxy_policy, headers=headers, verify=False)
        data_fwdproxy_policy = req_fwdproxy_policy.json()
        items_fwdproxy_policy = data_fwdproxy_policy['items']
        delete_conf_object(log_path, ns, api_fwdproxy_policy, items_fwdproxy_policy, 'Forward Proxy', wait_time)      
################################################

######################################################
# Function to delete Rate Limit Policy by namespace
######################################################
def list_and_delete_ratelimiter_policy (log_path,ns,wait_time):
        api_ratelimiter_policy = tenant_url + '/api/config/namespaces/' + ns + '/rate_limiter_policys'
        req_ratelimiter_policy = requests.get(api_ratelimiter_policy, headers=headers, verify=False)
        data_ratelimiter_policy = req_ratelimiter_policy.json()
        items_ratelimiter_policy = data_ratelimiter_policy['items']
        delete_conf_object(log_path, ns, api_ratelimiter_policy, items_ratelimiter_policy, 'Rate Limit', wait_time)      
################################################

###########################################################
# Function to delete Malicious User Mitigation by namespace
###########################################################
def list_and_delete_malicioususer_policy (log_path,ns,wait_time):
        api_malicioususer_policy = tenant_url + '/api/config/namespaces/' + ns + '/malicious_user_mitigations'
        req_malicioususer_policy = requests.get(api_malicioususer_policy, headers=headers, verify=False)
        data_malicioususer_policy = req_malicioususer_policy.json()
        items_malicioususer_policy = data_malicioususer_policy['items']
        delete_conf_object(log_path, ns, api_malicioususer_policy, items_malicioususer_policy, 'Malicious User Mitigation', wait_time)      
################################################

############################################################
# Function to delete User Identification Policy by namespace
############################################################
def list_and_delete_useridentification_policy (log_path,ns,wait_time):
        api_useridentification_policy = tenant_url + '/api/config/namespaces/' + ns + '/user_identifications'
        req_useridentification_policy = requests.get(api_useridentification_policy, headers=headers, verify=False)
        data_useridentification_policy = req_useridentification_policy.json()
        items_useridentification_policy = data_useridentification_policy['items']
        delete_conf_object(log_path, ns, api_useridentification_policy, items_useridentification_policy, 'User Identification', wait_time)      
################################################

################################################
# Function to delete IP Prefix set by namespace
################################################
def list_and_delete_ip_prefixset (log_path,ns,wait_time):
        api_ip_prefixset = tenant_url + '/api/config/namespaces/' + ns + '/ip_prefix_sets'
        req_ip_prefixset = requests.get(api_ip_prefixset, headers=headers, verify=False)
        data_ip_prefixset = req_ip_prefixset.json()
        items_ip_prefixset = data_ip_prefixset['items']
        delete_conf_object(log_path, ns, api_ip_prefixset, items_ip_prefixset, 'IP Prefix', wait_time)
################################################

################################################
# Function to delete Alert Policy by namespace
################################################
def list_and_delete_alert_policy (log_path,ns,wait_time):
        api_alert_policy = tenant_url + '/api/config/namespaces/' + ns + '/alert_policys'
        req_alert_policy = requests.get(api_alert_policy, headers=headers, verify=False)
        data_alert_policy = req_alert_policy.json()
        items_alert_policy = data_alert_policy['items']
        delete_conf_object(log_path, ns, api_alert_policy, items_alert_policy, 'Alert Policy', wait_time)
################################################

################################################
# Function to delete Alert Receiver by namespace
################################################
def list_and_delete_alert_receiver (log_path,ns,wait_time):
        api_alert_receiver = tenant_url + '/api/config/namespaces/' + ns + '/alert_receivers'
        req_alert_receiver = requests.get(api_alert_receiver, headers=headers, verify=False)
        data_alert_receiver = req_alert_receiver.json()
        items_alert_receiver = data_alert_receiver['items']
        delete_conf_object(log_path, ns, api_alert_receiver, items_alert_receiver, 'Alert Receiver', wait_time)
################################################

#####################################################
# Function to delete Global Log Receiver by namespace
#####################################################
def list_and_delete_global_log_receiver (log_path,ns,wait_time):
        api_global_log_receiver = tenant_url + '/api/config/namespaces/' + ns + '/global_log_receivers'
        req_global_log_receiver = requests.get(api_global_log_receiver, headers=headers, verify=False)
        data_global_log_receiver = req_global_log_receiver.json()
        items_global_log_receiver = data_global_log_receiver['items']
        delete_conf_object(log_path, ns, api_global_log_receiver, items_global_log_receiver, 'Global Log Receiver', wait_time)
################################################

#######################################################
# Function to delete Report Configuration by namespace
#######################################################
def list_and_delete_report_conf (log_path,backup_path,ns,wait_time):
        api_report_conf = tenant_url + '/api/report/namespaces/' + ns + '/report_configs'
        req_report_conf = requests.get(api_report_conf, headers=headers, verify=False)
        data_report_conf = req_report_conf.json()
        items_report_conf = data_report_conf['items']
        delete_conf_object(log_path,backup_path, ns, api_report_conf, items_report_conf, 'report_conf', 'Report Configuration', wait_time)
################################################

################################################
# Function to backup API Definition by namespace
################################################
def list_and_delete_xc_api_definition (log_path,ns,wait_time):
        api_xc_api_definition = tenant_url + '/api/config/namespaces/' + ns + '/api_definitions'
        req_xc_api_definition = requests.get(api_xc_api_definition, headers=headers, verify=False)
        data_xc_api_definition = req_xc_api_definition.json()
        items_xc_api_definition = data_xc_api_definition['items']
        delete_conf_object(log_path, ns, api_xc_api_definition, items_xc_api_definition, 'API Definition', wait_time)
################################################

################################################
# Function to delete TLS Certificate by namespace
################################################
def list_and_delete_cert_mgmt (log_path,ns,wait_time):
        api_cert_mgmt = tenant_url + '/api/config/namespaces/' + ns + '/certificates'
        req_cert_mgmt = requests.get(api_cert_mgmt, headers=headers, verify=False)
        data_cert_mgmt = req_cert_mgmt.json()
        items_cert_mgmt = data_cert_mgmt['items']
        delete_conf_object(log_path, ns, api_cert_mgmt, items_cert_mgmt, 'TLS Certificate', wait_time)
################################################
   
########################################################
# Function to delete TLS Certificate Chain by namespace
########################################################
def list_and_delete_cert_mgmt_chain (log_path,ns,wait_time):
        api_cert_mgmt_chain = tenant_url + '/api/config/namespaces/' + ns + '/certificate_chains'
        req_cert_mgmt_chain = requests.get(api_cert_mgmt_chain, headers=headers, verify=False)
        data_cert_mgmt_chain = req_cert_mgmt_chain.json()
        items_cert_mgmt_chain = data_cert_mgmt_chain['items']
        delete_conf_object(log_path, ns, api_cert_mgmt_chain, items_cert_mgmt_chain, 'TLS Certificate Chain', wait_time)
################################################
        
#####################################################
# Function to delete Service Discovery by namespace
#####################################################
def list_and_delete_svc_discovery (log_path,ns,wait_time):
        api_svc_discovery = tenant_url + '/api/config/namespaces/' + ns + '/discoverys'
        req_svc_discovery = requests.get(api_svc_discovery, headers=headers, verify=False)
        data_svc_discovery = req_svc_discovery.json()
        items_svc_discovery = data_svc_discovery['items']
        delete_conf_object(log_path, ns, api_svc_discovery, items_svc_discovery, 'Service Discovery', wait_time)
################################################


#######################
####### MAIN ##########
#######################

# Global Variable
tenant_name = 'XXXXXXXXXXXXXXXXX' # Update with your tenant name - e.g. f5-apac-sp
tenant_url = 'https://' + tenant_name + '.console.ves.volterra.io'
api_token = 'xxxxxxxxxxxxxxxxx' # Update with your API token. Refer to documentation to generate API Token.
version = '1.6' # Updated to version 1.5, changed from using environment variables to reading from a config file

try:
    # api_token = os.environ.get("XC_API_TOKEN")
    # tenant_name = os.environ.get("XC_TENANT")
    config = configparser.ConfigParser()
    home_dir = os.path.expanduser("~")
    configFile  = home_dir + "/.f5xc/config.ini"
    config.read(configFile)
    tenant_name = config['DEFAULT']['tenant']
    api_token = config['DEFAULT']['token']

    tenant_url = 'https://' + tenant_name + '.console.ves.volterra.io'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'APIToken ' + api_token
    }

    parser = argparse.ArgumentParser(description='F5XC Backup/Restore Utility Usage')
    parser.add_argument('--action','-a', help='Desire Action - backup / restore / forcerestore', required=True)
    parser.add_argument('--path','-p', help='Path to create backups in / restore backups from', required=True)
    parser.add_argument('--log','-l', help="Path to log backup and restore process", required=True)
    parser.add_argument('--namespace','-n', help='Namespace - comma deliminated', required=True)
    parser.add_argument('--version', action='version', version=f'%(prog)s v{version}')
    
    args = vars(parser.parse_args())
    namespace = args['namespace']
    backup_wait_time = 1
    restore_wait_time = 2
    input_path = args['path']
    log_path = args['log']
    
    ###api_ns = tenant_url + '/api/web/namespaces'
    ###req_ns = requests.get(api_ns, headers=headers, verify=False)
    ###data_ns = req_ns.json()
    ###items_ns = data_ns['items']
    #items_ns = ['arcadia-demo']
    #items_ns = ['mcn','shared','system','arcadia-demo']

    if not os.path.isdir(input_path) and os.path.isdir(log_path):
        raise Exception("Path is not a directory")
    else:
        # utc_now = datetime.utcnow()
        utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
        formatted_utc_now = utc_now.strftime('%Y%m%d_%H%M%S')
        backup_path = input_path + '/f5xc-backup-' + formatted_utc_now
        restore_path = input_path

    # print(backup_path)
    # print(restore_path)
    
    if args['action'] == 'backup':
        # utc_now = datetime.utcnow()
        utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
        formatted_utc_now = utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f'\033[0;35m\n ======================================================================================================================' )
        print(f'\033[0;35m [STARTED]     Date: {formatted_utc_now}     Tenant: {tenant_name}     TASK: BACKUP       Namespace: {namespace}')
        print(f'\033[0;35m ======================================================================================================================' )

        items_ns = namespace.split(',')

        for item_ns in items_ns:
            ns = item_ns
            backup_http_lb(log_path,backup_path,ns,backup_wait_time)
            backup_origin_pool(log_path,backup_path,ns,backup_wait_time)
            backup_healthchecks(log_path,backup_path,ns,backup_wait_time)
            backup_tcp_lb(log_path,backup_path,ns,backup_wait_time)
            backup_app_fw(log_path,backup_path,ns,backup_wait_time)
            backup_xc_api_definition(log_path,backup_path,ns,backup_wait_time)
            backup_service_policy(log_path,backup_path,ns,backup_wait_time)
            backup_ratelimiter_policy(log_path,backup_path,ns,backup_wait_time)
            backup_malicioususer_policy(log_path,backup_path,ns,backup_wait_time)
            backup_useridentification_policy(log_path,backup_path,ns,backup_wait_time)
            backup_ip_prefixset(log_path,backup_path,ns,backup_wait_time)
            
            #backup_fwdproxy_policy(log_path,backup_path,ns,backup_wait_time)
            #backup_alert_policy(log_path,backup_path,ns,backup_wait_time)
            #backup_alert_receiver(log_path,backup_path,ns,backup_wait_time)
            #backup_global_log_receiver(log_path,backup_path,ns,backup_wait_time)
            #backup_report_conf(log_path,backup_path,ns,backup_wait_time)
            #backup_cert_mgmt(log_path,backup_path,ns,backup_wait_time)
            #backup_cert_mgmt_chain(log_path,backup_path,ns,backup_wait_time)
            #backup_svc_discovery(log_path,backup_path,ns,backup_wait_time)
        
    elif args['action'] == 'restore':
        # utc_now = datetime.utcnow()
        utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
        formatted_utc_now = utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f'\033[0;35m \n==================================================================================================================================' )
        print(f'\033[0;35m [STARTED]     Date: {formatted_utc_now}      Tenant: {tenant_name}    TASK: RESTORE      Namespace: {namespace}' )
        print(f'\033[0;35m ====================================================================================================================================' )

        items_ns = namespace.split(',')
        
        for item_ns in items_ns:
            ns = item_ns
            restore_healthchecks(log_path,restore_path,ns,restore_wait_time)
            restore_origin_pool(log_path,restore_path,ns,restore_wait_time)
            restore_app_fw(log_path,restore_path,ns,restore_wait_time)
            restore_service_policy(log_path,restore_path,ns,restore_wait_time)
            restore_ratelimiter_policy(log_path,restore_path,ns,restore_wait_time)
            restore_ip_prefixset(log_path,restore_path,ns,restore_wait_time)
            restore_http_lb(log_path,restore_path,ns,restore_wait_time) # Note: New Auto-Cert will generate new cert.
            restore_tcp_lb(log_path,restore_path,ns,restore_wait_time) # Note: Hostname (start with ves-io-xxxx will be generate new)
            restore_malicioususer_policy(log_path,restore_path,ns,restore_wait_time)
            restore_useridentification_policy(log_path,restore_path,ns,restore_wait_time)
            
            #restore_fwdproxy_policy(log_path,restore_path,ns,restore_wait_time)
            #restore_xc_api_definition(log_path,restore_path,ns,restore_wait_time) # Need swagger file uploaded and update swagger link.
            #backup_cert_mgmt(log_path,restore_path,ns,restore_wait_time)
            #backup_cert_mgmt_chain(log_path,restore_path,ns,restore_wait_time)
            #backup_alert_policy(log_path,restore_path,ns,restore_wait_time)
            #backup_alert_receiver(log_path,restore_path,ns,restore_wait_time)
            #backup_global_log_receiver(log_path,restore_path,ns,restore_wait_time)
            #backup_report_conf(log_path,restore_path,ns,restore_wait_time) # Need reciever of report group created prior
            #backup_svc_discovery(log_path,restore_path,ns,restore_wait_time) # site must exist prior

    elif args['action'] == 'forcerestore':
        # utc_now = datetime.utcnow()
        utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
        formatted_utc_now = utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f'\033[0;35m \n==================================================================================================================================' )
        print(f'\033[0;35m [STARTED]     Date: {formatted_utc_now}      Tenant: {tenant_name}    TASK: FORCED RESTORE      Namespace: {namespace}' )
        print(f'\033[0;35m ====================================================================================================================================' )

        items_ns = namespace.split(',')
        
        for item_ns in items_ns:
            ns = item_ns
            list_and_delete_healthchecks(log_path,ns,restore_wait_time)
            restore_healthchecks(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_http_lb(log_path,ns,restore_wait_time)
            list_and_delete_tcp_lb(log_path,ns,restore_wait_time)
            list_and_delete_origin_pool(log_path,ns,restore_wait_time)
            restore_origin_pool(log_path,restore_path,ns,restore_wait_time)
            restore_http_lb(log_path,restore_path,ns,restore_wait_time) # Note: New Auto-Cert will generate new cert.
            restore_tcp_lb(log_path,restore_path,ns,restore_wait_time) # Note: Hostname (start with ves-io-xxxx will be generate new)

            list_and_delete_app_fw(log_path,ns,restore_wait_time)
            restore_app_fw(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_service_policy(log_path,ns,restore_wait_time)
            restore_service_policy(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_ratelimiter_policy(log_path,ns,restore_wait_time)
            restore_ratelimiter_policy(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_ip_prefixset(log_path,ns,restore_wait_time)
            restore_ip_prefixset(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_malicioususer_policy(log_path,ns,restore_wait_time  )
            restore_malicioususer_policy(log_path,restore_path,ns,restore_wait_time)

            list_and_delete_useridentification_policy(log_path,ns,restore_wait_time)
            restore_useridentification_policy(log_path,restore_path,ns,restore_wait_time)
            
            #restore_fwdproxy_policy(log_path,restore_path,ns,restore_wait_time)
            #restore_xc_api_definition(log_path,restore_path,ns,restore_wait_time) # Need swagger file uploaded and update swagger link.
            #backup_cert_mgmt(log_path,restore_path,ns,restore_wait_time)
            #backup_cert_mgmt_chain(log_path,restore_path,ns,restore_wait_time)
            #backup_alert_policy(log_path,restore_path,ns,restore_wait_time)
            #backup_alert_receiver(log_path,restore_path,ns,restore_wait_time)
            #backup_global_log_receiver(log_path,restore_path,ns,restore_wait_time)
            #backup_report_conf(log_path,restore_path,ns,restore_wait_time) # Need reciever of report group created prior
            #backup_svc_discovery(log_path,restore_path,ns,restore_wait_time) # site must exist prior
    # utc_now = datetime.utcnow()
    utc_now = datetime.now(tz=ZoneInfo("Etc/UTC"))
    formatted_utc_now = utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f'\033[0;35m ================================================================================================================' )
    print(f'\033[0;35m [COMPLETED]   Date: {formatted_utc_now}     Tenant: {tenant_name}')
    print(f'\033[0;35m ================================================================================================================\n' )

except KeyError:
    print( "Error reading from config.ini, please sure that config.ini exists in $HOME/.f5xc" )
    sys.exit(1)