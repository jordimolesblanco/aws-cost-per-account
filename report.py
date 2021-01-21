import boto3
import sys
from calendar import monthrange


# collecting some command line arguments
month = int(sys.argv[1])
year = int(sys.argv[2])

# defining some variables that we will need later
aws_costs_per_account = {
    'ACCOUNTNUMBER': {'Name': 'ACCOUNT 1', 'Services': {}},
    "ACCOUNTNUMBER": {'Name': 'ACCOUNT 2', 'Services': {}},
}

daysmonth = monthrange(year, month)[1]
daysmonth = str(daysmonth).zfill(2)
month = str(month).zfill(2)
startdate = '%s-%s-01' % (year, month)
enddate = '%s-%s-%s' % (year, month, daysmonth)

# connecting to the Cost Explorer API
cd = boto3.client('ce')

# getting the total amount for each account
totalperaccount = cd.get_cost_and_usage(TimePeriod={'Start': startdate, 'End':  enddate},
                                        Granularity='MONTHLY',
                                        Metrics=['NetAmortizedCost'],
                                        GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}])
totalperaccount = totalperaccount['ResultsByTime'][0]['Groups']

# from the list of accounts and totals, we iterate and extract each value
for account in totalperaccount:
    # we add the total amount and name to the dictionary
    accountid = account['Keys'][0]

    try:
        totalaccount = int(float(account['Metrics']['NetAmortizedCost']['Amount']))
        aws_costs_per_account[accountid]['Total'] = totalaccount

    except:
        aws_costs_per_account[accountid]['Total'] = "Error"

    try:
        # while iterating we also request the cost details per service from this account
        totalperaccount = cd.get_cost_and_usage(TimePeriod={'Start': startdate, 'End': enddate},
                                                Granularity='MONTHLY',
                                                Filter={"Dimensions": {"Key": "LINKED_ACCOUNT", "Values": [accountid]}},
                                                Metrics=['NetAmortizedCost'],
                                                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}])

        totalperaccount = totalperaccount['ResultsByTime'][0]['Groups']

    except:
        aws_costs_per_account[accountid]['Services'] = "Error"

    # now we iterate and only record the biggest billing items
    for costitem in totalperaccount:

        if costitem['Keys'] == ['AWS Lambda']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Lambda'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Lambda'] = "Error"

        if costitem['Keys'] == ['Tax']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Taxes'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Taxes'] = "Error"

        if costitem['Keys'] == ['Amazon Elasticsearch Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['ElasticSearch'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['ElasticSearch'] = "Error"

        if costitem['Keys'] == ['AWS Key Management Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['KMS'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['KMS'] = "Error"

        if costitem['Keys'] == ['AWS Secrets Manager']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['SecretsManager'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['SecretsManager'] = "Error"

        if costitem['Keys'] == ['AWS WAF']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['WAF'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['WAF'] = "Error"

        if costitem['Keys'] == ['Amazon API Gateway']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['APIGateway'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['APIGateway'] = "Error"

        if costitem['Keys'] == ['Amazon CloudFront']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['CloudFront'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['CloudFront'] = "Error"

        if costitem['Keys'] == ['Amazon DocumentDB (with MongoDB compatibility)']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['DocumentDB'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['DocumentDB'] = "Error"

        if costitem['Keys'] == ['Amazon DynamoDB']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['DynamoDB'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['DynamoDB'] = "Error"

        if costitem['Keys'] == ['Amazon EC2 Container Registry (ECR)']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['ECR'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['ECR'] = "Error"

        if costitem['Keys'] == ['Amazon EC2 Container Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['ECS'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['ECS'] = "Error"

        if costitem['Keys'] == ['Amazon ElastiCache']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['ElasticCache'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['ElasticCache'] = "Error"

        if costitem['Keys'] == ['Amazon Elastic Compute Cloud - Compute']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['EC2-Compute'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['EC2-Compute'] = "Error"

        if costitem['Keys'] == ['Amazon Elastic Load Balancing']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['LoadBalancers'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['LoadBalancers'] = "Error"

        if costitem['Keys'] == ['AWS Support (Business)']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Support'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Support'] = "Error"

        if costitem['Keys'] == ['AWS Support (Developer)']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Support'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Support'] = "Error"

        if costitem['Keys'] == ['Amazon Relational Database Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['RDS'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['RDS'] = "Error"

        if costitem['Keys'] == ['Amazon Route 53']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Route53'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Route53'] = "Error"

        if costitem['Keys'] == ['Amazon Simple Notification Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['SNS'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['SNS'] = "Error"

        if costitem['Keys'] == ['Amazon Simple Queue Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['SQS'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['SQS'] = "Error"

        if costitem['Keys'] == ['Amazon Simple Storage Service']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['S3'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['S3'] = "Error"

        if costitem['Keys'] == ['Amazon Transcribe']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['Transcribe'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['Transcribe'] = "Error"

        if costitem['Keys'] == ['Amazon Virtual Private Cloud']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['VPC'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['VPC'] = "Error"

        if costitem['Keys'] == ['AmazonCloudWatch']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['CloudWatch-Logs'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['CloudWatch-Logs'] = "Error"

        if costitem['Keys'] == ['CloudWatch Events']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['CloudWatch-Events'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['CloudWatch-Events'] = "Error"

        if costitem['Keys'] == ['EC2 - Other']:

            try:
                costitemvalue = costitem['Metrics']['NetAmortizedCost']['Amount']
                aws_costs_per_account[accountid]['Services']['EC2-Other'] = int(float(costitemvalue))

            except:
                aws_costs_per_account[accountid]['Services']['EC2-Other'] = "Error"

# finally we generate a list of comma separated values to import into a spreadsheet
print("Summary for %s/%s" % (month, year))
for accountid in aws_costs_per_account:
    accountname = aws_costs_per_account[accountid]['Name']

    try:
        accounttotal = aws_costs_per_account[accountid]['Total']
    except:
        accounttotal = 0

    ec2compute = 0
    ec2others = 0
    loadbalancers = 0
    cloudwatch = 0
    vpc = 0
    transcribe = 0
    s3 = 0
    rds = 0
    dynamodb = 0
    documentdb = 0
    support = 0
    elasticcache = 0
    elasticsearch = 0
    ecs = 0
    waf = 0
    secrets = 0
    taxes = 0
    cloudfront = 0
    llambda = 0

    for service in aws_costs_per_account[accountid]['Services']:
        amount = aws_costs_per_account[accountid]['Services'][service]

        if service in ['EC2-Other']:
            ec2others += amount

        if service in ['CloudWatch-Events', 'CloudWatch-Logs']:
            cloudwatch += amount

        if service in ['VPC']:
           vpc += amount

        if service in ['Transcribe']:
           transcribe += amount

        if service in ['S3']:
           s3 += amount

        if service in ['RDS']:
           rds += amount

        if service in ['DynamoDB']:
           dynamodb += amount

        if service in ['DocumentDB']:
           documentdb += amount

        if service in ['Support']:
           support += amount

        if service in ['LoadBalancers']:
           loadbalancers += amount

        if service in ['EC2-Compute']:
           ec2compute += amount

        if service in ['ElasticCache']:
           elasticcache += amount

        if service in ['ECS', 'ECR']:
           ecs += amount

        if service in ['CloudFront']:
           cloudfront += amount

        if service in ['WAF']:
           waf += amount

        if service in ['SecretsManager', 'KMS']:
           secrets += amount

        if service in ['ElasticSearch']:
           elasticsearch += amount

        if service in ['Taxes']:
           taxes += amount

        if service in ['Lambda']:
           llambda += amount

    print("--- %s ---->" % accountname)
    print("%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s" %
          (ec2compute, loadbalancers, ec2others, cloudwatch, vpc, transcribe, s3, rds, documentdb, dynamodb, elasticsearch,
           cloudfront, support, elasticcache, llambda, ecs, waf, secrets, taxes, accounttotal))
