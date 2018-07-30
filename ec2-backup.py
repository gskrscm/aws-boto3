import boto3

ecl = {}
ecl_test = {'i-0a2abd5d2a9a57b66': [{'Key': 'hello', 'Value': 'hi-boto'}], 'i-09ad7b8dce2e6b1ff': None}

def ec2_list():
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    #print(response)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # This sample print will output entire Dictionary object
            #print(instance)
            # This will print will output the value of the Dictionary key 'InstanceId'
            #print(instance["InstanceId"])
            ecid = instance["InstanceId"]
            tagl = get_instance_tags(ecid)
            ecl.update({ecid:tagl})


def get_instance_tags(ecid):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(ecid)
    tagl = ec2instance.tags
    return tagl

def create_ami_aws(ecl):
    create_fmt = "siva-ami"
    ec2 = boto3.client('ec2')
    for ec in ecl:
        print(ec)
        AMIid = ec2.create_image(InstanceId=ec, 
                            Name="Lambda - " + ec + " from " + create_fmt, 
                            Description="Lambda created AMI of instance " + ec + " from " + create_fmt, 
                            NoReboot=True, DryRun=False)
        print(AMIid)

        ami_image = ec2.Image(AMIid["ImageId"])

        tags = get_instance_tags(ec)
        for key, value in tags: 
            ami_image.create_tags({'Key':key, 'Value':value})




ec2_list()
create_ami_aws(ecl)