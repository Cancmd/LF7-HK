# config.py
# this file contains a function with the credentials for connecting to the database. This is done for security reasons
# The port is being defined to port 80 due to restrictive firewall access and routing issues with Ubuntu
db_config = {
    "host" : "hostip",
    "port" : 80,
    "user" : "username",
    "password" : "password",
    "database" : "dbname"
}

smb_config = {
    server="-", 
    username="-", 
    password="-"
}