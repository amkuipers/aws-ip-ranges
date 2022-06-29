[![Pylint](https://github.com/amkuipers/aws-ip-ranges/actions/workflows/pylint.yml/badge.svg)](https://github.com/amkuipers/aws-ip-ranges/actions/workflows/pylint.yml)

# tool: ipranges
Queries the ip-ranges JSON file from AWS, and lists its content in another form. 
The tool includes filters and an IP lookup.
It currently only works with the IPv4 ranges from that file, and ignores the IPv6 ranges.

```
$ python3 ipranges.py -h
usage: Filter AWS IP Ranges [-h] [-r REGION] [-s SERVICE] [-f] [-ip LOOKUP]

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        region filter, like eu-west-2
  -s SERVICE, --service SERVICE
                        service filter, like S3, AMAZON
  -f, --filters         list filters
  -ip LOOKUP, --lookup LOOKUP
                        lookup service and region by ip
```

## IP filter

The `-ip` or `--lookup` filter requires an IPv4 value like `52.219.169.42`.
So when you are wondering if the IP is used on AWS? This will tell you.

Example wide output with ip filter:
```
$ python3 ipranges.py -ip 52.219.169.42
[+] Retrieving ip-ranges.json...
[+] Retrieved ip-ranges.json
[+] File size 1249723
[+] IPv4 CIDR ranges filter for 52.219.169.42
[+] service AMAZON, region eu-central-1, cidr 52.219.169.0/24, from 52.219.169.0, to 52.219.169.255
[+] service S3, region eu-central-1, cidr 52.219.169.0/24, from 52.219.169.0, to 52.219.169.255
```

Example with the services/regions filters output, using the ip filter. 
The IP is in `S3` in `eu-central-1`:
```
$ python3 ipranges.py -ip 52.219.169.42 --filters
[+] Retrieving ip-ranges.json...
[+] Retrieved ip-ranges.json
[+] File size 1249723
[+] IPv4 CIDR ranges filter for 52.219.169.42
[+] service S3
[+] service AMAZON
[+] region eu-central-1
```

It can also be combined with the service and region filters. 
Then the IP might not be found, and that could be useful too.

```
$ python3 ipranges.py --service S3 --region eu-west-2 -ip 52.219.169.42
[+] Retrieving ip-ranges.json...
[+] Retrieved ip-ranges.json
[+] File size 1249723
[+] IPv4 CIDR ranges filter for service S3 in region eu-west-2
[+] IPv4 CIDR ranges filter for 52.219.169.42
[-] Empty result
```


## List filters

The ipranges.py with `-f` or `--filters` option lists the remaining service values and region values.
The service, region and ip filters are applied.
This will not show the wide list.

Example output:
```
$ python3 ipranges.py --filters
[+] Retrieving ip-ranges.json...
[+] Retrieved ip-ranges.json
[+] File size 1249383
[+] service CLOUDFRONT_ORIGIN_FACING
[+] service CLOUD9
[+] service AMAZON_CONNECT
[+] service DYNAMODB
[+] service CHIME_MEETINGS
[+] service ROUTE53_HEALTHCHECKS
[+] service API_GATEWAY
[+] service S3
[+] service EBS
[+] service EC2
[+] service AMAZON_APPFLOW
[+] service WORKSPACES_GATEWAYS
[+] service ROUTE53_HEALTHCHECKS_PUBLISHING
[+] service AMAZON
[+] service CLOUDFRONT
[+] service CHIME_VOICECONNECTOR
[+] service ROUTE53
[+] service GLOBALACCELERATOR
[+] service ROUTE53_RESOLVER
[+] service KINESIS_VIDEO_STREAMS
[+] service EC2_INSTANCE_CONNECT
[+] service CODEBUILD
[+] region ap-southeast-4
[+] region eu-south-2
[+] region eu-central-1
[+] region me-south-1
[+] region us-east-2
[+] region GLOBAL
[+] region us-west-1
[+] region cn-north-1
[+] region eu-west-1
[+] region eu-central-2
[+] region ap-southeast-2
[+] region ap-northeast-2
[+] region ap-south-2
[+] region sa-east-1
[+] region us-gov-east-1
[+] region eu-north-1
[+] region af-south-1
[+] region eu-west-3
[+] region ap-southeast-1
[+] region ap-east-1
[+] region ap-northeast-3
[+] region me-central-1
[+] region us-east-1
[+] region ap-northeast-1
[+] region us-west-2
[+] region us-gov-west-1
[+] region ca-central-1
[+] region eu-west-2
[+] region ap-southeast-3
[+] region cn-northwest-1
[+] region ap-south-1
[+] region eu-south-1
[+] region il-central-1
```

## Wide list 

The ipranges.py prints a wide list of the service, region, cidr and cidr's from-to IPv4 addresses.
The service, region and ip filters are applied.
This will not show the filters list.
This is the default output.

Example output with service and region filters:
```
$ python3 ipranges.py --service S3 --region eu-west-2
[+] Retrieving ip-ranges.json...
[+] Retrieved ip-ranges.json
[+] File size 1249723
[+] IPv4 CIDR ranges filter for service S3 in region eu-west-2
[+] service S3, region eu-west-2, cidr 52.95.150.0/24, from 52.95.150.0, to 52.95.150.255
[+] service S3, region eu-west-2, cidr 16.12.15.0/24, from 16.12.15.0, to 16.12.15.255
[+] service S3, region eu-west-2, cidr 16.12.16.0/23, from 16.12.16.0, to 16.12.17.255
[+] service S3, region eu-west-2, cidr 52.95.148.0/23, from 52.95.148.0, to 52.95.149.255
[+] service S3, region eu-west-2, cidr 52.95.144.0/24, from 52.95.144.0, to 52.95.144.255
[+] service S3, region eu-west-2, cidr 52.95.142.0/23, from 52.95.142.0, to 52.95.143.255
[+] service S3, region eu-west-2, cidr 3.5.244.0/22, from 3.5.244.0, to 3.5.247.255
[+] service S3, region eu-west-2, cidr 18.168.37.160/28, from 18.168.37.160, to 18.168.37.175
[+] service S3, region eu-west-2, cidr 18.168.37.176/28, from 18.168.37.176, to 18.168.37.191
```

## Region filter

The `-r` or `--region` filter requires a value like `eu-west-2`.
Can be used in the list filters and wide list.
Use the list filters option to learn the available region values.

## Service filter

The `-s` or `--service` filter requires a value like `S3` or `EC2`.
Can be used in the list filters and wide list.
Use the list filters option to learn the available service values.

