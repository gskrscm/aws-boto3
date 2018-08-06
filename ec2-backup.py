import boto3
import datetime

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
retention_days = 7

def ec2_list():
    '''Get List of ec2 instances and their tags'''
    ecl = {}
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            ecid = instance["InstanceId"]
            tagl = get_instance_tags(ecid)
            ecl.update({ecid:tagl})
    return ecl

def get_instance_tags(ecid):
    '''Get ec2 instance tags as list'''
    ec2instance = ec2_resource.Instance(ecid)
    tagl = ec2instance.tags
    return tagl

def get_image_tags(amid): 
    image = ec2_resource.Image(amid)
    return image.tags

# create ami and set all tags. 
def create_ami_aws(ecl):
    ''' Create ami and set all tags'''

    # Time formatting
    create_time = datetime.datetime.now() 
    create_fmt = create_time.strftime('%Y-%m-%d')
    print(create_fmt)

    for ec in ecl:
        # Ami creation
        try: 
            AMIid = ec2_client.create_image(InstanceId=ec, 
                            Name="Lambda - " + ec + " from " + create_fmt, 
                            Description="Lambda created AMI of instance " + ec + " from " + create_fmt, 
                            NoReboot=True, DryRun=False)
            print("Ami id: {} is created for ec2 instance: {} ".format(AMIid["ImageId"], ec))
            tags = get_instance_tags(ec)

            delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
            delete_fmt = delete_date.strftime('%m-%d-%Y')
            delete_on = {'Key' : "DeleteOn", 'Value' : delete_fmt}

            tags.append(delete_on)

            print("Tags: {} , for ec2: {} ".format(tags, ec))

            for tag in tags:
                print("key: {}, Value : {}".format(tag["Key"], tag["Value"]))

                response = ec2_client.create_tags(DryRun=False,
                                        Resources=[AMIid["ImageId"]],
                                        Tags=[
                                            {
                                                'Key': tag["Key"],
                                                'Value': tag["Value"]
                                            }
                                        ]
                                    )
                print("Ami create tags response: ".format(response))
        except Exception as e:
            print("Exception: {}".format(e))

def aws_ami_delte(): 
    '''Get all ami and delete if tag matches today date'''
    iml =[]
    response = ec2_client.describe_images(Filters=[
        {
            'Name': 'tag-key', 
            'Values' : ['DeleteOn']
        }     
    ], 
    DryRun=False
    )

    to_day = datetime.date.today()
    to_day_fmt = to_day.strftime('%m-%d-%Y')
    print(to_day_fmt)


    for img in response['Images']:
        tags = get_image_tags(img['ImageId'])
        for tag in tags:
            print(tag['Key'], tag['Value'])
            if tag['Key'] == 'DeleteOn':
                if tag['Value'] == to_day_fmt:
                    resp = aws_ami_deregister(img['ImageId'])
                    print(resp)


def aws_ami_deregister(amid):
    ''' Deregister an ami and also dlete respective snapshot'''
    response = ec2_client.deregister_image(ImageId=amid, DryRun=False)
    return response 

if __name__ == "__main__": 

    # Get EC2 list: 
    ec2_list = ec2_list()

    # Create ami
    create_ami_aws(ec2_list)

    # Delete ami which are equal to retention days
    res = aws_ami_delte()['ResponseMetadata']
    if res['HTTPStatusCode'] == '200': 
        print('Ami succesfully deleted.')
    else: 
        raise ValueError('Ami deletion Failed.')




