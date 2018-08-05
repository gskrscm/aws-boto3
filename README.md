### ec2-backup.py 

Script to take backup of all ec2 instances, create AMIs with `DeleteOn` tag with value of future date to delete, and Deletes AMI's which having `DeleteOn` tag with today's date. 