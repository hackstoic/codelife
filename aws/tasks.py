#!/usr/bin/env python
# -*- coding: utf-8 -*-


import boto3
import argparse
import sys


def start_ec2():
    print "start all ec2 instances"
    msg = ""
    action = str(sys._getframe().f_code.co_name)
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for ins in instances:
        print "instance id : %s" % ins.id
        msg += "%s;" % ins.id
        ins.start()
    return {"action": action, "status": True, "msg": msg, "error": ""}


def stop_ec2():
    print "stop all ec2 instances"
    msg = ""
    action = str(sys._getframe().f_code.co_name)
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for ins in instances:
        print "instance id : %s" % ins.id
        msg += "%s;" % ins.id
        ins.stop()
    return {"action": action, "status": True, "msg": msg, "error": ""}


def check_ec2():
    print "check all ec2 status"
    msg = ""
    action = str(sys._getframe().f_code.co_name)
    ec2 = boto3.resource('ec2')
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        msg += str(status) + ";"    
    return {"action": action, "status": True, "msg": msg, "error": ""}


def main():
    parser = argparse.ArgumentParser(description="my aws tasks client")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--check_ec2", action="store_true", help="check status of  all ec2 instance")
    group.add_argument("-s", "--start_ec2", action="store_true", help="start all ec2 instance")
    group.add_argument("-k", "--stop_ec2", action="store_true", help="stop all ec2 instance")
    args = parser.parse_args()
    if args.start_ec2:
        start_ec2()
    if args.stop_ec2:
        stop_ec2()
    if args.check_ec2:
        check_ec2()

if __name__ == "__main__":
    sys.exit(main())