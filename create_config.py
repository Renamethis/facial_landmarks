import configparser
config = configparser.ConfigParser()
config['Settings'] = {
  'ip': 'None',
  'port': '80',
  'user': 'admin',
  'password': 'Supervisor'
}
keys = config['Settings'].keys()
print(keys)
for key in keys:
    if(config['Settings'][key] == 'None'):
        print('Enter ', key, ':')
        config['Settings'][key] = input()
    else:
        print('Enter ', key, ' or nothing(default is ', config['Settings'][key], ')')
        val = input()
        if(val):
            config['Settings'][key] = val
with open('settings.ini', 'w') as conf:
    config.write(conf)
