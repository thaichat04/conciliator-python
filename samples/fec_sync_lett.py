import conciliator as cc
import json

# TODO: change to CLI
# https://github.com/google/python-fire

cc_env = 'preprod' # or 'prod'
fec_file = 'data/cogedispro/24531-fec.TXT'
tenant = 'cpf_cogedispro'
entity = '24531'
dry_run = False

config_file = 'password.json'
config = json.load(open(config_file, 'r'))

if cc_env == 'preprod':
    cc.url('https://preprod.app.expert.dhatim.com/')

cc.connect(config[cc_env]['username'], config[cc_env]['password'], tenant)
e = cc.Entity.load(entity)
if not e: raise ValueError('Cannot find entity')

# default values
LET_START = 'IAA'
THIRD_P = ('401', '411')
JOUR_CC = ('IA', 'IV')

#TODO: comment recuperer
JOUR_BQ = ('03', '05', '07')


conns = cc.Connector.list()
for conn in conns:
    if conn.type == 'ISACOMPTA':
        JOUR_CC = (conn.param('purchaseCode'), conn.param('saleCode'))
        scode = conn.param('thirdParty_supplier_code')
        ccode = conn.param('thirdParty_client_code')
        THIRD_P = (scode[0: scode.find('$')], ccode[0: ccode.find('$')])
        LET_START = conn.param('thirdParty_client_code')
    if conn.type == 'RECONCILIATOR_BANK':
        LET_START = conn.param('lettering')




# Passe 1: identification des journaux
# - A-Nouveau si date de piece = debut d'exo
# - Banque si la plupart des ecritures sont en 512



# Passe 2:
# si Achat/Vente: recherche facture par numero de facture
# restriction sur compte Tiers, date et montant
# - si lettrage FEC et lettrage < IAA => exclue
#
# si Banque: recherche operation date, libelle, montant
# - si lettrage FEC et lettrage < IAA et si pas (NO_INVOICE ou NO_SUPPLIER)
#  - si Tiers selon la pattern CC (401/411) => Piece hors CC
#  - sinon => Tiers Hors CC

fec = open(fec_file,'r')

def amount(debit, credit):
    return float(credit.replace(',', '.') if credit else '0') - float(debit.replace(',', '.') if debit else '0')

def fdate(d):
    return d[0:4] + '-' + d[4:6] + '-' +  d[6:8]

bo_report = {'found': 0, 'noact': 0, 'notfound': 0, 'multiple':0, 'maxdate_notfound': '19700101'}

def find_bo(ecr):
    bo_id = None
    cur.execute("select id, disabled from bank_operation where date = %s and amount = %s and entity_id = %s",
                (ecr.date, ecr.ttc, entity_id))
    if cur.rowcount == 0:
        #print(f"No match for bo with ref {ecr.ttc} and date {ecr.date} at line {ecr.line_nb} ")
        bo_report['notfound'] += 1
        bo_report['maxdate_notfound'] = max(bo_report['maxdate_notfound'], ecr.date)
    if cur.rowcount > 1:
        #print(f"Too many matches for bo at line {ecr.line_nb}")
        bo_report['multiple'] += 1
    if cur.rowcount == 1:
        bo_id,  disabled = cur.fetchone()
        if disabled in ('NO_INVOICE', 'NO_SUPPLIER'):
            bo_id = None
            bo_report['noact'] += 1
        bo_report['found'] += 1
    ecr.cc_id = bo_id
    return ecr

invoice_report = {'found': 0, 'noact': 0, 'notfound': 0, 'multiple':0}

def find_invoice(ecr):
    invoice_id = None
    cur.execute("select id, bank_enabled from invoice where date = %s and (reference like %s or reference is null) and abs(total_incl_tax) = %s and entity_id = %s",
                (fdate(ecr.date), '%' + ecr.ref + '%', abs(ecr.ttc), entity_id))
    if cur.rowcount == 0:
        #print(f"No match for invoice with ref {ecr.ref} and date {ecr.date} at line {ecr.line_nb} ")
        invoice_report['notfound'] += 1
    if cur.rowcount > 1:
        #print(f"Too many matches for invoice at line {ecr.line_nb}")
        invoice_report['multiple'] += 1
    if cur.rowcount == 1:
        invoice_id, bank_enabled = cur.fetchone()
        if not bank_enabled:
            invoice_report['noact'] += 1
            invoice_id = None
        invoice_report['found'] += 1
    ecr.cc_id = invoice_id
    return ecr

def mark_invoice(ecr):
    if not ecr.cc_id: return
    if not dry_run:
        cur.execute("update invoice set bank_enabled = False where id = %s", (ecr.cc_id,))
        conn.commit()
    print(f"Updating invoice,{ecr.ref},{ecr.ttc},{ecr.date},{ecr.tiers},{ecr.cc_id},{ecr.let}")

# def mark_bo(ecr):
#     if not ecr.cc_id: return
#     #if ecr.tiers:
#     #    disable_type = 'NO_INVOICE'
#     #else:
#     #    disable_type = 'NO_SUPPLIER'
#     if not dry_run:
#         cur.execute("update bank_operation set disabled = %s, ratio = 1, manual = True, supplier_id = null where id = %s",
#                     (disable_type, bo_id))
#         conn.commit()
#     print(f"Updating bo {ecr.ttc},{ecr.date},{ecr.tiers},{ecr.cc_id},{ecr.let}")

class Ecr:
    def __getattr__(self, name):
        # returns None on access to an attribute that doesn't exist
        return None


ecr = Ecr()
line_nb = 0

# 0-4   JournalCode	JournalLib	EcritureNum	EcritureDate	CompteNum
# 5-9   CompteLib	CompAuxNum	CompAuxLib	PieceRef	PieceDate
# 10-14 EcritureLib	Debit	Credit	EcritureLet	DateLet
# 15-19 ValidDate	Montantdevise	Idevise	DateRglt	ModeRglt
# 20-21 NatOp	IdClient

for line in fec:
    line_nb += 1
    fields = line.split('\t')
    # ID = JournalCode  + EcritureNum + EcritureDate
    fec_id = fields[0] + '/' + fields[2] + '/' + fields[3]

    if ecr.fec_id and ecr.fec_id != fec_id:
        #process complete ECR
        #if ecr.type and ecr.tiers: print(ecr.line_nb, ecr.type, ecr.tiers, ecr.ttc)
        if ecr.type == 'CC' and ecr.let and ecr.let < LET_START:
            find_invoice(ecr)
            mark_invoice(ecr)
        #if ecr.type == 'BQ' and ecr.let and ecr.let < LET_START:
        #    find_bo(ecr)
        #    mark_bo(ecr)
        ecr = Ecr()

    # process line
    if ecr.fec_id:
        if ecr.fec_id != fec_id:
            print(f"inconsistent ID in line {line_nb}")
    else:
        ecr.fec_id = fec_id
        ecr.line_nb = line_nb
        if fields[0] in JOUR_CC:
            ecr.type = 'CC'
        elif fields[0] in JOUR_BQ:
            ecr.type = 'BQ'
    if ecr.type and fields[4][0:len(THIRD_P[0])] in THIRD_P:
        if ecr.tiers:
            print(f"WARNING: Un seul tiers possible ligne {line_nb}")
            ecr.tiers = '*MULTIPLE*'
        else:
            ecr.tiers = fields[4].strip()
            ecr.ref = fields[8].strip()
            ecr.date = fields[9].strip()
            ecr.let = fields[13].strip()
            ecr.ttc = amount(fields[11], fields[12])

print ("Invoice report", invoice_report)
print ("BO report", bo_report)

