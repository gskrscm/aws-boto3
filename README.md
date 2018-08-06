### ec2-backup.py 

Script to take backup of all ec2 instances, create AMIs with `DeleteOn` tag with value of future date to delete, and Deletes AMI's which having `DeleteOn` tag with today's date. 

## Pre-requists: 
1) Install AWSCLI and Configure. 
2) Install python aws boto3 module. 



## References: 
* AWS BOTO Documentation: 
https://boto3.readthedocs.io/en/latest/reference/services/index.html

