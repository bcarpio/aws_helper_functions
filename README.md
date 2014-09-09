# AWS Helper Functions

This is a basic set of helper functions which you can use to get info from your AWS account. 

## Installation

`sudo apt-get install python-pip`
`sudo pip install fabric`
`sudo pip install boto`

## Configuration

Rename `config_example.ini` to `config.ini`. Update `access_key` and `secret_key` with your API keys from AWS. 

## Running

Type `fab -l` this will output the 'things' you can do. So for example:

`fab get_instance_list:us-east-1`

Will print all the instances in the us-east-1 region. 

`fab get_instance_list:us-west-2`

Will print all the instances in the us-west-2 region, etc..


