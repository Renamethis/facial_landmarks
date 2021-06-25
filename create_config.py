### CONFIG GENERATOR
import configparser
config = configparser.ConfigParser()
config['ONVIFSettings'] = {
  'ptz': 'False',
  'speed': '0.1',
  'ip': 'None',
  'port': '80',
  'user': 'admin',
  'password': 'Supervisor',
  'profile': '0',
}
config['MAINSettings'] = {
    'source' : '0',
    'leftpoint' : '41',
    'rightpoint' : '46',
    'nosepoint' : '28',
    'centerpoint' : '30',
    'turndifferent' : '10',
    'thirddifferent' : '50',
    'imagewidth' : '500'
}
keys = config['ONVIFSettings'].keys()
for key in keys:
    if(config['ONVIFSettings'][key] == 'None'):
        print('Enter ', key, ':')
        config['ONVIFSettings'][key] = input()
    else:
        print('Enter ', key, ' or nothing(default is ', config['ONVIFSettings'][key], ')')
        val = input()
        if(val):
            config['ONVIFSettings'][key] = val
keys = config['MAINSettings'].keys()
for key in keys:
    if(config['MAINSettings'][key] == 'None'):
        print('Enter ', key, ':')
        config['MAINSettings'][key] = input()
    else:
        print('Enter ', key, ' or nothing(default is ', config['MAINSettings'][key], ')')
        val = input()
        if(val):
            config['MAINSettings'][key] = val
with open('settings.ini', 'w') as conf:
    config.write(conf)
