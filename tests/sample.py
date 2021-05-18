import conciliator as cc
import json
import datetime

config_file = 'password.json'
config = json.load(open(config_file, 'r'))

#cc.connect(config['onetenant']['username'], config['onetenant']['password'])
cc.connect(config['selecttenant']['username'], config['selecttenant']['password'],
           config['selecttenant']['selectedtenant'])


cs = cc.Connector.list()
for c in cs:
    if c.type == 'CSV':
        print(c.param('purchaseCode'))
    #c.config[name = 'purchasCode'] .value
pass

e = cc.Entity.load(query='DH')
es = cc.Entity.list()
e.set_current()
#cc.current_entity = e
#f = cc.File.load(name='in1HnhltCcKlYJxALVbRmifsM2.pdf')
#i = cc.Invoice.list("1442", filter={'date': datetime.date(2020, 11, 19)})
invoices = cc.Invoice.search("intercom")
print(invoices)
