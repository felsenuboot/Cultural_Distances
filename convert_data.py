# %%
import pandas as pd
import json
from io import StringIO 

# %%
culture_map_data = [
    {"id":1,"name":"Argentina","datamapId":"ARG","isoCode":32,"isoShortCode":"AR","scores":{"communicating":55,"evaluating":35,"leading":60,"deciding":65,"trusting":72,"disagreeing":32,"scheduling":76,"persuading":25}},
    {"id":2,"name":"Australia","datamapId":"AUS","isoCode":36,"isoShortCode":"AU","scores":{"communicating":4,"evaluating":32,"leading":18,"deciding":48,"trusting":16,"disagreeing":34,"scheduling":26,"persuading":86}},
    {"id":3,"name":"Botswana","datamapId":"BWA","isoCode":72,"isoShortCode":"BW","scores":{"communicating":80,"evaluating":73,"leading":90,"deciding":94,"trusting":96,"disagreeing":80,"scheduling":96,"persuading":-1}},
    {"id":4,"name":"Brazil","datamapId":"BRA","isoCode":76,"isoShortCode":"BR","scores":{"communicating":62,"evaluating":65,"leading":57,"deciding":57,"trusting":75,"disagreeing":62,"scheduling":77,"persuading":39}},
    {"id":5,"name":"Canada","datamapId":"CAN","isoCode":124,"isoShortCode":"CA","scores":{"communicating":8,"evaluating":50,"leading":21,"deciding":48,"trusting":6,"disagreeing":54,"scheduling":26,"persuading":92}},
    {"id":6,"name":"Chile","datamapId":"CHL","isoCode":152,"isoShortCode":"CL","scores":{"communicating":58,"evaluating":60,"leading":65,"deciding":60,"trusting":70,"disagreeing":56,"scheduling":76,"persuading":44}},
    {"id":7,"name":"China","datamapId":"CHN","isoCode":156,"isoShortCode":"CN","scores":{"communicating":92,"evaluating":68,"leading":90,"deciding":88,"trusting":88,"disagreeing":80,"scheduling":82,"persuading":-1}},
    {"id":8,"name":"Colombia","datamapId":"COL","isoCode":170,"isoShortCode":"CO","scores":{"communicating":65,"evaluating":65,"leading":70,"deciding":70,"trusting":75,"disagreeing":66,"scheduling":72,"persuading":44}},
    {"id":9,"name":"Denmark","datamapId":"DNK","isoCode":208,"isoShortCode":"DK","scores":{"communicating":27,"evaluating":12,"leading":0,"deciding":16,"trusting":10,"disagreeing":26,"scheduling":24,"persuading":58}},
    {"id":10,"name":"Egypt","datamapId":"EGY","isoCode":818,"isoShortCode":"EG","scores":{"communicating":74,"evaluating":65,"leading":84,"deciding":80,"trusting":76,"disagreeing":64,"scheduling":84,"persuading":-1}},
    {"id":11,"name":"U.A.E (Emirati)","datamapId":"ARE","isoCode":784,"isoShortCode":"AE","scores":{"communicating":70,"evaluating":68,"leading":84,"deciding":80,"trusting":78,"disagreeing":74,"scheduling":70,"persuading":-1}},
    {"id":12,"name":"Finland","datamapId":"FIN","isoCode":246,"isoShortCode":"FI","scores":{"communicating":34,"evaluating":18,"leading":24,"deciding":26,"trusting":24,"disagreeing":60,"scheduling":20,"persuading":56}},
    {"id":13,"name":"France","datamapId":"FRA","isoCode":250,"isoShortCode":"FR","scores":{"communicating":66,"evaluating":17,"leading":67,"deciding":67,"trusting":58,"disagreeing":3,"scheduling":55,"persuading":1}},
    {"id":14,"name":"Germany","datamapId":"DEU","isoCode":276,"isoShortCode":"DE","scores":{"communicating":24,"evaluating":8,"leading":61,"deciding":28,"trusting":20,"disagreeing":9,"scheduling":3,"persuading":22}},
    {"id":15,"name":"Ghana","datamapId":"GHA","isoCode":288,"isoShortCode":"GH","scores":{"communicating":81,"evaluating":78,"leading":96,"deciding":94,"trusting":96,"disagreeing":75,"scheduling":96,"persuading":-1}},
    {"id":16,"name":"India","datamapId":"IND","isoCode":356,"isoShortCode":"IN","scores":{"communicating":76,"evaluating":65,"leading":85,"deciding":85,"trusting":85,"disagreeing":72,"scheduling":88,"persuading":-1}},
    {"id":17,"name":"Indonesia","datamapId":"IDN","isoCode":360,"isoShortCode":"ID","scores":{"communicating":94,"evaluating":96,"leading":92,"deciding":92,"trusting":94,"disagreeing":96,"scheduling":90,"persuading":-1}},
    {"id":18,"name":"Italy","datamapId":"ITA","isoCode":380,"isoShortCode":"IT","scores":{"communicating":65,"evaluating":25,"leading":68,"deciding":66,"trusting":62,"disagreeing":32,"scheduling":64,"persuading":15}},
    {"id":19,"name":"Japan","datamapId":"JPN","isoCode":392,"isoShortCode":"JP","scores":{"communicating":95,"evaluating":90,"leading":91,"deciding":3,"trusting":77,"disagreeing":95,"scheduling":15,"persuading":-1}},
    {"id":20,"name":"Kenya","datamapId":"KEN","isoCode":404,"isoShortCode":"KE","scores":{"communicating":84,"evaluating":70,"leading":90,"deciding":92,"trusting":88,"disagreeing":72,"scheduling":96,"persuading":-1}},
    {"id":21,"name":"Korea","datamapId":"KOR","isoCode":410,"isoShortCode":"KR","scores":{"communicating":94,"evaluating":78,"leading":96,"deciding":94,"trusting":84,"disagreeing":80,"scheduling":64,"persuading":-1}},
    {"id":22,"name":"Kuwait","datamapId":"KWT","isoCode":414,"isoShortCode":"KW","scores":{"communicating":75,"evaluating":75,"leading":87,"deciding":86,"trusting":94,"disagreeing":76,"scheduling":92,"persuading":-1}},
    {"id":23,"name":"Mexico","datamapId":"MEX","isoCode":484,"isoShortCode":"MX","scores":{"communicating":65,"evaluating":64,"leading":68,"deciding":68,"trusting":75,"disagreeing":66,"scheduling":70,"persuading":50}},
    {"id":24,"name":"Morocco","datamapId":"MAR","isoCode":504,"isoShortCode":"MA","scores":{"communicating":74,"evaluating":62,"leading":84,"deciding":80,"trusting":76,"disagreeing":64,"scheduling":84,"persuading":-1}},
    {"id":25,"name":"Netherlands","datamapId":"NLD","isoCode":528,"isoShortCode":"NL","scores":{"communicating":14,"evaluating":4,"leading":6,"deciding":16,"trusting":8,"disagreeing":18,"scheduling":24,"persuading":66}},
    {"id":26,"name":"Nigeria","datamapId":"NGA","isoCode":566,"isoShortCode":"NG","scores":{"communicating":78,"evaluating":26,"leading":100,"deciding":96,"trusting":90,"disagreeing":24,"scheduling":96,"persuading":-1}},
    {"id":27,"name":"Norway","datamapId":"NOR","isoCode":578,"isoShortCode":"NO","scores":{"communicating":34,"evaluating":30,"leading":4,"deciding":10,"trusting":16,"disagreeing":50,"scheduling":20,"persuading":56}},
    {"id":28,"name":"Pakistan","datamapId":"PAK","isoCode":586,"isoShortCode":"PK","scores":{"communicating":78,"evaluating":68,"leading":90,"deciding":86,"trusting":88,"disagreeing":72,"scheduling":88,"persuading":-1}},
    {"id":29,"name":"Peru","datamapId":"PER","isoCode":604,"isoShortCode":"PE","scores":{"communicating":75,"evaluating":75,"leading":76,"deciding":72,"trusting":80,"disagreeing":70,"scheduling":74,"persuading":44}},
    {"id":30,"name":"Philippines","datamapId":"PHL","isoCode":618,"isoShortCode":"PH","scores":{"communicating":94,"evaluating":88,"leading":92,"deciding":92,"trusting":94,"disagreeing":94,"scheduling":90,"persuading":-1}},
    {"id":31,"name":"Poland","datamapId":"POL","isoCode":616,"isoShortCode":"PL","scores":{"communicating":42,"evaluating":12,"leading":65,"deciding":65,"trusting":45,"disagreeing":26,"scheduling":40,"persuading":30}},
    {"id":32,"name":"Portugal","datamapId":"PRT","isoCode":620,"isoShortCode":"PT","scores":{"communicating":56,"evaluating":35,"leading":64,"deciding":64,"trusting":66,"disagreeing":48,"scheduling":65,"persuading":6}},
    {"id":33,"name":"Romania","datamapId":"ROU","isoCode":642,"isoShortCode":"RO","scores":{"communicating":70,"evaluating":32,"leading":80,"deciding":72,"trusting":74,"disagreeing":32,"scheduling":64,"persuading":10}},
    {"id":34,"name":"Russia","datamapId":"RUS","isoCode":643,"isoShortCode":"RU","scores":{"communicating":70,"evaluating":2,"leading":88,"deciding":76,"trusting":74,"disagreeing":8,"scheduling":64,"persuading":10}},
    {"id":35,"name":"Saudi Arabia","datamapId":"SSD","isoCode":682,"isoShortCode":"SA","scores":{"communicating":82,"evaluating":84,"leading":88,"deciding":86,"trusting":94,"disagreeing":74,"scheduling":92,"persuading":-1}},
    {"id":36,"name":"Singapore","datamapId":"XXX","isoCode":702,"isoShortCode":"SG","scores":{"communicating":72,"evaluating":68,"leading":86,"deciding":72,"trusting":68,"disagreeing":62,"scheduling":26,"persuading":-1}},
    {"id":37,"name":"Spain","datamapId":"ESP","isoCode":724,"isoShortCode":"ES","scores":{"communicating":60,"evaluating":30,"leading":60,"deciding":60,"trusting":66,"disagreeing":26,"scheduling":65,"persuading":10}},
    {"id":38,"name":"Sweden","datamapId":"SWE","isoCode":752,"isoShortCode":"SE","scores":{"communicating":34,"evaluating":50,"leading":2,"deciding":1,"trusting":24,"disagreeing":62,"scheduling":18,"persuading":56}},
    {"id":39,"name":"Thailand","datamapId":"THA","isoCode":764,"isoShortCode":"TH","scores":{"communicating":94,"evaluating":98,"leading":92,"deciding":92,"trusting":94,"disagreeing":98,"scheduling":90,"persuading":-1}},
    {"id":40,"name":"Turkey","datamapId":"TUR","isoCode":792,"isoShortCode":"TR","scores":{"communicating":70,"evaluating":58,"leading":80,"deciding":72,"trusting":80,"disagreeing":60,"scheduling":74,"persuading":-1}},
    {"id":41,"name":"UK","datamapId":"GBR","isoCode":826,"isoShortCode":"GB","scores":{"communicating":32,"evaluating":63,"leading":46,"deciding":46,"trusting":15,"disagreeing":55,"scheduling":30,"persuading":76}},
    {"id":42,"name":"United States","datamapId":"USA","isoCode":840,"isoShortCode":"US","scores":{"communicating":3,"evaluating":45,"leading":24,"deciding":64,"trusting":3,"disagreeing":44,"scheduling":22,"persuading":95}},
    {"id":43,"name":"Venezuela","datamapId":"VEN","isoCode":862,"isoShortCode":"VE","scores":{"communicating":70,"evaluating":65,"leading":72,"deciding":72,"trusting":80,"disagreeing":68,"scheduling":72,"persuading":44}},
    {"id":44,"name":"Zimbabwe","datamapId":"ZWE","isoCode":716,"isoShortCode":"ZW","scores":{"communicating":82,"evaluating":74,"leading":95,"deciding":91,"trusting":94,"disagreeing":80,"scheduling":96,"persuading":-1}},
    {"id":45,"name":"Czech Republic","datamapId":"CZE","isoCode":203,"isoShortCode":"CZ","scores":{"communicating":34,"evaluating":10,"leading":70,"deciding":65,"trusting":30,"disagreeing":65,"scheduling":20,"persuading":36}},
    {"id":46,"name":"Ireland","datamapId":"IRL","isoCode":372,"isoShortCode":"IE","scores":{"communicating":32,"evaluating":60,"leading":30,"deciding":30,"trusting":40,"disagreeing":55,"scheduling":35,"persuading":76}},
    {"id":47,"name":"Greece","datamapId":"GRC","isoCode":300,"isoShortCode":"GR","scores":{"communicating":68,"evaluating":19,"leading":67,"deciding":67,"trusting":72,"disagreeing":9,"scheduling":70,"persuading":5}},
    {"id":48,"name":"Israel","datamapId":"ISR","isoCode":376,"isoShortCode":"IL","scores":{"communicating":35,"evaluating":1,"leading":9,"deciding":48,"trusting":62,"disagreeing":1,"scheduling":65,"persuading":90}},
    {"id":49,"name":"Qatar","datamapId":"QAT","isoCode":634,"isoShortCode":"QA","scores":{"communicating":78,"evaluating":80,"leading":86,"deciding":86,"trusting":93,"disagreeing":74,"scheduling":89,"persuading":-1}},
    {"id":50,"name":"Cameroon","datamapId":"CMR","isoCode":120,"isoShortCode":"CM","scores":{"communicating":90,"evaluating":60,"leading":96,"deciding":94,"trusting":97,"disagreeing":60,"scheduling":96,"persuading":-1}},
    {"id":51,"name":"Tanzania","datamapId":"TZA","isoCode":834,"isoShortCode":"TZ","scores":{"communicating":88,"evaluating":78,"leading":92,"deciding":92,"trusting":92,"disagreeing":86,"scheduling":96,"persuading":-1}},
    {"id":52,"name":"Uganda","datamapId":"UGA","isoCode":800,"isoShortCode":"UG","scores":{"communicating":86,"evaluating":70,"leading":93,"deciding":93,"trusting":93,"disagreeing":74,"scheduling":96,"persuading":-1}},
    {"id":53,"name":"Belgium","datamapId":"BEL","isoCode":56,"isoShortCode":"BE","scores":{"communicating":42,"evaluating":25,"leading":50,"deciding":25,"trusting":40,"disagreeing":40,"scheduling":40,"persuading":10}},
    {"id":54,"name":"Hungary","datamapId":"HUN","isoCode":348,"isoShortCode":"HU","scores":{"communicating":70,"evaluating":10,"leading":76,"deciding":76,"trusting":65,"disagreeing":30,"scheduling":20,"persuading":25}},
    {"id":55,"name":"Bolivia","datamapId":"BOL","isoCode":68,"isoShortCode":"BO","scores":{"communicating":72,"evaluating":75,"leading":76,"deciding":72,"trusting":80,"disagreeing":70,"scheduling":74,"persuading":44}},
    {"id":56,"name":"Ethiopia","datamapId":"ETH","isoCode":231,"isoShortCode":"ET","scores":{"communicating":87,"evaluating":80,"leading":96,"deciding":96,"trusting":98,"disagreeing":86,"scheduling":96,"persuading":-1}},
    {"id":57,"name":"Austria","datamapId":"AUT","isoCode":40,"isoShortCode":"AT","scores":{"communicating":42,"evaluating":34,"leading":68,"deciding":66,"trusting":42,"disagreeing":32,"scheduling":30,"persuading":15}},
    {"id":58,"name":"Switzerland","datamapId":"CHE","isoCode":756,"isoShortCode":"CH","scores":{"communicating":34,"evaluating":34,"leading":46,"deciding":55,"trusting":28,"disagreeing":35,"scheduling":1,"persuading":22}},
    {"id":59,"name":"Tunisia","datamapId":"TUN","isoCode":788,"isoShortCode":"TN","scores":{"communicating":76,"evaluating":60,"leading":86,"deciding":80,"trusting":78,"disagreeing":60,"scheduling":84,"persuading":-1}},
    {"id":60,"name":"Ukraine","datamapId":"UKR","isoCode":804,"isoShortCode":"UA","scores":{"communicating":60,"evaluating":3,"leading":75,"deciding":75,"trusting":71,"disagreeing":20,"scheduling":64,"persuading":10}},
    {"id":61,"name":"Malaysia","datamapId":"MYS","isoCode":458,"isoShortCode":"MY","scores":{"communicating":82,"evaluating":78,"leading":89,"deciding":82,"trusting":80,"disagreeing":75,"scheduling":75,"persuading":-1}},
    {"id":62,"name":"Vietnam","datamapId":"VNM","isoCode":704,"isoShortCode":"VN","scores":{"communicating":94,"evaluating":80,"leading":90,"deciding":88,"trusting":84,"disagreeing":86,"scheduling":84,"persuading":-1}},
    {"id":63,"name":"New Zealand","datamapId":"NZL","isoCode":554,"isoShortCode":"NZ","scores":{"communicating":21,"evaluating":35,"leading":20,"deciding":45,"trusting":45,"disagreeing":50,"scheduling":30,"persuading":80}},
    {"id":64,"name":"Jordan","datamapId":"JOR","isoCode":400,"isoShortCode":"JO","scores":{"communicating":73,"evaluating":72,"leading":85,"deciding":86,"trusting":93,"disagreeing":75,"scheduling":75,"persuading":-1}},
    {"id":65,"name":"South Africa (Afrikaans)","datamapId":"ZAF","isoCode":710,"isoShortCode":"ZA","scores":{"communicating":32,"evaluating":12,"leading":50,"deciding":65,"trusting":20,"disagreeing":25,"scheduling":30,"persuading":-1}},
    {"id":66,"name":"South Africa (Zulu)","datamapId":"ZAF","isoCode":710,"isoShortCode":"ZA","scores":{"communicating":75,"evaluating":60,"leading":80,"deciding":80,"trusting":80,"disagreeing":65,"scheduling":84,"persuading":-1}},
    {"id":67,"name":"Bulgaria","datamapId":"BGR","isoCode":100,"isoShortCode":"BG","scores":{"communicating":70,"evaluating":15,"leading":80,"deciding":72,"trusting":74,"disagreeing":26,"scheduling":64,"persuading":10}},
    {"id":68,"name":"Lebanon","datamapId":"LBN","isoCode":422,"isoShortCode":"LB","scores":{"communicating":70,"evaluating":60,"leading":75,"deciding":75,"trusting":78,"disagreeing":55,"scheduling":70,"persuading":-1}},
    {"id":69,"name":"Costa Rica","datamapId":"CRI","isoCode":188,"isoShortCode":"CR","scores":{"communicating":65,"evaluating":55,"leading":65,"deciding":65,"trusting":75,"disagreeing":62,"scheduling":65,"persuading":50}},
    {"id":70,"name":"Jamaica","datamapId":"JAM","isoCode":388,"isoShortCode":"JM","scores":{"communicating":65,"evaluating":30,"leading":78,"deciding":78,"trusting":80,"disagreeing":32,"scheduling":80,"persuading":60}},
    {"id":71,"name":"Dominican Republic","datamapId":"DOM","isoCode":214,"isoShortCode":"DO","scores":{"communicating":75,"evaluating":65,"leading":80,"deciding":80,"trusting":85,"disagreeing":65,"scheduling":80,"persuading":75}}
]
hofstede_data = """
ctr,country,cultural dimension,Value
AFE,Africa East,idv,27
AFE,Africa East,ivr,40
AFE,Africa East,ltowvs,32
AFE,Africa East,mas,41
AFE,Africa East,pdi,64
AFE,Africa East,uai,52
AFW,Africa West,idv,20
AFW,Africa West,ivr,78
AFW,Africa West,ltowvs,9
AFW,Africa West,mas,46
AFW,Africa West,pdi,77
AFW,Africa West,uai,54
ALB,Albania,idv,27
ALB,Albania,ivr,15
ALB,Albania,ltowvs,61
ALB,Albania,mas,80
ALB,Albania,pdi,90
ALB,Albania,uai,70
ALG,Algeria,idv,29
ALG,Algeria,ivr,32
ALG,Algeria,ltowvs,26
ALG,Algeria,mas,35
ALG,Algeria,pdi,80
ALG,Algeria,uai,70
ARA,Arab countries,idv,38
ARA,Arab countries,ivr,34
ARA,Arab countries,ltowvs,23
ARA,Arab countries,mas,53
ARA,Arab countries,pdi,80
ARA,Arab countries,uai,68
ARG,Argentina,idv,46
ARG,Argentina,ivr,62
ARG,Argentina,ltowvs,20
ARG,Argentina,mas,56
ARG,Argentina,pdi,49
ARG,Argentina,uai,86
ARM,Armenia,idv,17
ARM,Armenia,ivr,25
ARM,Armenia,ltowvs,61
ARM,Armenia,mas,50
ARM,Armenia,pdi,85
ARM,Armenia,uai,88
AUL,Australia,idv,90
AUL,Australia,ivr,71
AUL,Australia,ltowvs,21
AUL,Australia,mas,61
AUL,Australia,pdi,38
AUL,Australia,uai,51
AUT,Austria,idv,55
AUT,Austria,ivr,63
AUT,Austria,ltowvs,60
AUT,Austria,mas,79
AUT,Austria,pdi,11
AUT,Austria,uai,70
AZE,Azerbaijan,idv,28
AZE,Azerbaijan,ivr,22
AZE,Azerbaijan,ltowvs,61
AZE,Azerbaijan,mas,50
AZE,Azerbaijan,pdi,85
AZE,Azerbaijan,uai,88
BAN,Bangladesh,idv,20
BAN,Bangladesh,ivr,20
BAN,Bangladesh,ltowvs,47
BAN,Bangladesh,mas,55
BAN,Bangladesh,pdi,80
BAN,Bangladesh,uai,60
BEL,Belgium,idv,75
BEL,Belgium,ivr,57
BEL,Belgium,ltowvs,82
BEL,Belgium,mas,54
BEL,Belgium,pdi,65
BEL,Belgium,uai,94
BLR,Belarus,idv,48
BLR,Belarus,ivr,15
BLR,Belarus,ltowvs,81
BLR,Belarus,mas,20
BLR,Belarus,pdi,95
BLR,Belarus,uai,95
BOS,Bosnia,idv,40
BOS,Bosnia,ivr,44
BOS,Bosnia,ltowvs,70
BOS,Bosnia,mas,48
BOS,Bosnia,pdi,90
BOS,Bosnia,uai,87
BRA,Brazil,idv,38
BRA,Brazil,ivr,59
BRA,Brazil,ltowvs,44
BRA,Brazil,mas,49
BRA,Brazil,pdi,69
BRA,Brazil,uai,76
BUF,Burkina Faso,idv,15
BUF,Burkina Faso,ivr,18
BUF,Burkina Faso,ltowvs,27
BUF,Burkina Faso,mas,50
BUF,Burkina Faso,pdi,70
BUF,Burkina Faso,uai,55
BUL,Bulgaria,idv,30
BUL,Bulgaria,ivr,16
BUL,Bulgaria,ltowvs,69
BUL,Bulgaria,mas,40
BUL,Bulgaria,pdi,70
BUL,Bulgaria,uai,85
CAN,Canada,idv,80
CAN,Canada,ivr,68
CAN,Canada,ltowvs,36
CAN,Canada,mas,52
CAN,Canada,pdi,39
CAN,Canada,uai,48
CHI,China,idv,20
CHI,China,ivr,24
CHI,China,ltowvs,87
CHI,China,mas,66
CHI,China,pdi,80
CHI,China,uai,30
CHL,Chile,idv,23
CHL,Chile,ivr,68
CHL,Chile,ltowvs,31
CHL,Chile,mas,28
CHL,Chile,pdi,63
CHL,Chile,uai,86
COL,Colombia,idv,13
COL,Colombia,ivr,83
COL,Colombia,ltowvs,13
COL,Colombia,mas,64
COL,Colombia,pdi,67
COL,Colombia,uai,80
CRO,Croatia,idv,33
CRO,Croatia,ivr,33
CRO,Croatia,ltowvs,58
CRO,Croatia,mas,40
CRO,Croatia,pdi,73
CRO,Croatia,uai,80
CZE,Czech Rep,idv,58
CZE,Czech Rep,ivr,29
CZE,Czech Rep,ltowvs,70
CZE,Czech Rep,mas,57
CZE,Czech Rep,pdi,57
CZE,Czech Rep,uai,74
DEN,Denmark,idv,74
DEN,Denmark,ivr,70
DEN,Denmark,ltowvs,35
DEN,Denmark,mas,16
DEN,Denmark,pdi,18
DEN,Denmark,uai,23
DOM,Dominican Rep,idv,38
DOM,Dominican Rep,ivr,54
DOM,Dominican Rep,ltowvs,13
DOM,Dominican Rep,mas,65
DOM,Dominican Rep,pdi,65
DOM,Dominican Rep,uai,45
EGY,Egypt,idv,13
EGY,Egypt,ivr,4
EGY,Egypt,ltowvs,7
EGY,Egypt,mas,55
EGY,Egypt,pdi,80
EGY,Egypt,uai,55
EST,Estonia,idv,60
EST,Estonia,ivr,16
EST,Estonia,ltowvs,82
EST,Estonia,mas,30
EST,Estonia,pdi,40
EST,Estonia,uai,60
ETH,Ethiopia,idv,7
ETH,Ethiopia,ivr,46
ETH,Ethiopia,ltowvs,14
ETH,Ethiopia,mas,65
ETH,Ethiopia,pdi,70
ETH,Ethiopia,uai,55
FIN,Finland,idv,63
FIN,Finland,ivr,57
FIN,Finland,ltowvs,38
FIN,Finland,mas,26
FIN,Finland,pdi,33
FIN,Finland,uai,59
FRA,France,idv,71
FRA,France,ivr,48
FRA,France,ltowvs,63
FRA,France,mas,43
FRA,France,pdi,68
FRA,France,uai,86
GBR,Great Britain,idv,89
GBR,Great Britain,ivr,69
GBR,Great Britain,ltowvs,51
GBR,Great Britain,mas,66
GBR,Great Britain,pdi,35
GBR,Great Britain,uai,35
GEO,Georgia,idv,15
GEO,Georgia,ivr,32
GEO,Georgia,ltowvs,38
GEO,Georgia,mas,55
GEO,Georgia,pdi,65
GEO,Georgia,uai,85
GER,Germany,idv,67
GER,Germany,ivr,40
GER,Germany,ltowvs,83
GER,Germany,mas,66
GER,Germany,pdi,35
GER,Germany,uai,65
GRE,Greece,idv,35
GRE,Greece,ivr,50
GRE,Greece,ltowvs,45
GRE,Greece,mas,57
GRE,Greece,pdi,60
GRE,Greece,uai,100
HOK,Hong Kong,idv,25
HOK,Hong Kong,ivr,17
HOK,Hong Kong,ltowvs,61
HOK,Hong Kong,mas,57
HOK,Hong Kong,pdi,68
HOK,Hong Kong,uai,29
HUN,Hungary,idv,80
HUN,Hungary,ivr,31
HUN,Hungary,ltowvs,58
HUN,Hungary,mas,88
HUN,Hungary,pdi,46
HUN,Hungary,uai,82
ICE,Iceland,idv,83
ICE,Iceland,ivr,67
ICE,Iceland,ltowvs,28
ICE,Iceland,mas,10
ICE,Iceland,pdi,30
ICE,Iceland,uai,50
IDO,Indonesia,idv,14
IDO,Indonesia,ivr,38
IDO,Indonesia,ltowvs,62
IDO,Indonesia,mas,46
IDO,Indonesia,pdi,78
IDO,Indonesia,uai,48
IND,India,idv,48
IND,India,ivr,26
IND,India,ltowvs,51
IND,India,mas,56
IND,India,pdi,77
IND,India,uai,40
IRA,Iran,idv,41
IRA,Iran,ivr,40
IRA,Iran,ltowvs,14
IRA,Iran,mas,43
IRA,Iran,pdi,58
IRA,Iran,uai,59
IRE,Ireland,idv,70
IRE,Ireland,ivr,65
IRE,Ireland,ltowvs,24
IRE,Ireland,mas,68
IRE,Ireland,pdi,28
IRE,Ireland,uai,35
IRQ,Iraq,idv,25
IRQ,Iraq,ivr,17
IRQ,Iraq,ltowvs,25
IRQ,Iraq,mas,53
IRQ,Iraq,pdi,97
IRQ,Iraq,uai,96
ITA,Italy,idv,76
ITA,Italy,ivr,30
ITA,Italy,ltowvs,61
ITA,Italy,mas,70
ITA,Italy,pdi,50
ITA,Italy,uai,75
JOR,Jordan,idv,20
JOR,Jordan,ivr,43
JOR,Jordan,ltowvs,16
JOR,Jordan,mas,45
JOR,Jordan,pdi,70
JOR,Jordan,uai,65
JPN,Japan,idv,46
JPN,Japan,ivr,42
JPN,Japan,ltowvs,88
JPN,Japan,mas,95
JPN,Japan,pdi,54
JPN,Japan,uai,92
KOR,Korea South,idv,18
KOR,Korea South,ivr,29
KOR,Korea South,ltowvs,100
KOR,Korea South,mas,39
KOR,Korea South,pdi,60
KOR,Korea South,uai,85
LAT,Latvia,idv,70
LAT,Latvia,ivr,13
LAT,Latvia,ltowvs,69
LAT,Latvia,mas,9
LAT,Latvia,pdi,44
LAT,Latvia,uai,63
LIT,Lithuania,idv,60
LIT,Lithuania,ivr,16
LIT,Lithuania,ltowvs,82
LIT,Lithuania,mas,19
LIT,Lithuania,pdi,42
LIT,Lithuania,uai,65
LUX,Luxembourg,idv,60
LUX,Luxembourg,ivr,56
LUX,Luxembourg,ltowvs,64
LUX,Luxembourg,mas,50
LUX,Luxembourg,pdi,40
LUX,Luxembourg,uai,70
MAC,Macedonia Rep,idv,40
MAC,Macedonia Rep,ivr,35
MAC,Macedonia Rep,ltowvs,62
MAC,Macedonia Rep,mas,45
MAC,Macedonia Rep,pdi,90
MAC,Macedonia Rep,uai,87
MAL,Malaysia,idv,26
MAL,Malaysia,ivr,57
MAL,Malaysia,ltowvs,41
MAL,Malaysia,mas,50
MAL,Malaysia,pdi,100
MAL,Malaysia,uai,36
MEX,Mexico,idv,30
MEX,Mexico,ivr,97
MEX,Mexico,ltowvs,24
MEX,Mexico,mas,69
MEX,Mexico,pdi,81
MEX,Mexico,uai,82
MLT,Malta,idv,59
MLT,Malta,ivr,66
MLT,Malta,ltowvs,47
MLT,Malta,mas,47
MLT,Malta,pdi,56
MLT,Malta,uai,96
MNG,Montenegro,idv,27
MNG,Montenegro,ivr,20
MNG,Montenegro,ltowvs,75
MNG,Montenegro,mas,48
MNG,Montenegro,pdi,88
MNG,Montenegro,uai,90
MOL,Moldova,idv,27
MOL,Moldova,ivr,19
MOL,Moldova,ltowvs,71
MOL,Moldova,mas,39
MOL,Moldova,pdi,90
MOL,Moldova,uai,95
MOR,Morocco,idv,46
MOR,Morocco,ivr,25
MOR,Morocco,ltowvs,14
MOR,Morocco,mas,53
MOR,Morocco,pdi,70
MOR,Morocco,uai,68
NET,Netherlands,idv,80
NET,Netherlands,ivr,68
NET,Netherlands,ltowvs,67
NET,Netherlands,mas,14
NET,Netherlands,pdi,38
NET,Netherlands,uai,53
NIG,Nigeria,idv,0
NIG,Nigeria,ivr,84
NIG,Nigeria,ltowvs,13
NIG,Nigeria,mas,60
NIG,Nigeria,pdi,80
NIG,Nigeria,uai,55
NOR,Norway,idv,69
NOR,Norway,ivr,55
NOR,Norway,ltowvs,35
NOR,Norway,mas,8
NOR,Norway,pdi,31
NOR,Norway,uai,50
NZL,New Zealand,idv,79
NZL,New Zealand,ivr,75
NZL,New Zealand,ltowvs,33
NZL,New Zealand,mas,58
NZL,New Zealand,pdi,22
NZL,New Zealand,uai,49
PAK,Pakistan,idv,14
PAK,Pakistan,ivr,0
PAK,Pakistan,ltowvs,50
PAK,Pakistan,mas,50
PAK,Pakistan,pdi,55
PAK,Pakistan,uai,70
PER,Peru,idv,16
PER,Peru,ivr,46
PER,Peru,ltowvs,25
PER,Peru,mas,42
PER,Peru,pdi,64
PER,Peru,uai,87
PHI,Philippines,idv,32
PHI,Philippines,ivr,42
PHI,Philippines,ltowvs,27
PHI,Philippines,mas,64
PHI,Philippines,pdi,94
PHI,Philippines,uai,44
POL,Poland,idv,60
POL,Poland,ivr,29
POL,Poland,ltowvs,38
POL,Poland,mas,64
POL,Poland,pdi,68
POL,Poland,uai,93
POR,Portugal,idv,27
POR,Portugal,ivr,33
POR,Portugal,ltowvs,28
POR,Portugal,mas,31
POR,Portugal,pdi,63
POR,Portugal,uai,99
PUE,Puerto Rico,idv,43
PUE,Puerto Rico,ivr,90
PUE,Puerto Rico,ltowvs,0
PUE,Puerto Rico,mas,56
PUE,Puerto Rico,pdi,68
PUE,Puerto Rico,uai,38
ROM,Romania,idv,30
ROM,Romania,ivr,20
ROM,Romania,ltowvs,52
ROM,Romania,mas,42
ROM,Romania,pdi,90
ROM,Romania,uai,90
RUS,Russia,idv,39
RUS,Russia,ivr,20
RUS,Russia,ltowvs,81
RUS,Russia,mas,36
RUS,Russia,pdi,93
RUS,Russia,uai,95
SAF,South Africa,idv,23
SAF,South Africa,ivr,63
SAF,South Africa,ltowvs,34
SAF,South Africa,mas,63
SAF,South Africa,pdi,49
SAF,South Africa,uai,49
SAL,El Salvador,idv,19
SAL,El Salvador,ivr,89
SAL,El Salvador,ltowvs,20
SAL,El Salvador,mas,40
SAL,El Salvador,pdi,66
SAL,El Salvador,uai,94
SAU,Saudi Arabia,idv,48
SAU,Saudi Arabia,ivr,52
SAU,Saudi Arabia,ltowvs,36
SAU,Saudi Arabia,mas,43
SAU,Saudi Arabia,pdi,72
SAU,Saudi Arabia,uai,64
SER,Serbia,idv,25
SER,Serbia,ivr,28
SER,Serbia,ltowvs,52
SER,Serbia,mas,43
SER,Serbia,pdi,86
SER,Serbia,uai,92
SIN,Singapore,idv,20
SIN,Singapore,ivr,46
SIN,Singapore,ltowvs,72
SIN,Singapore,mas,48
SIN,Singapore,pdi,74
SIN,Singapore,uai,8
SLK,Slovak Rep,idv,52
SLK,Slovak Rep,ivr,28
SLK,Slovak Rep,ltowvs,77
SLK,Slovak Rep,mas,100
SLK,Slovak Rep,pdi,100
SLK,Slovak Rep,uai,51
SLV,Slovenia,idv,27
SLV,Slovenia,ivr,48
SLV,Slovenia,ltowvs,49
SLV,Slovenia,mas,19
SLV,Slovenia,pdi,71
SLV,Slovenia,uai,88
SPA,Spain,idv,51
SPA,Spain,ivr,44
SPA,Spain,ltowvs,48
SPA,Spain,mas,42
SPA,Spain,pdi,57
SPA,Spain,uai,86
SWE,Sweden,idv,71
SWE,Sweden,ivr,78
SWE,Sweden,ltowvs,53
SWE,Sweden,mas,5
SWE,Sweden,pdi,31
SWE,Sweden,uai,29
SWI,Switzerland,idv,68
SWI,Switzerland,ivr,66
SWI,Switzerland,ltowvs,74
SWI,Switzerland,mas,70
SWI,Switzerland,pdi,34
SWI,Switzerland,uai,58
TAI,Taiwan,idv,17
TAI,Taiwan,ivr,49
TAI,Taiwan,ltowvs,93
TAI,Taiwan,mas,45
TAI,Taiwan,pdi,58
TAI,Taiwan,uai,69
TAN,Tanzania,idv,25
TAN,Tanzania,ivr,38
TAN,Tanzania,ltowvs,34
TAN,Tanzania,mas,40
TAN,Tanzania,pdi,70
TAN,Tanzania,uai,50
THA,Thailand,idv,20
THA,Thailand,ivr,45
THA,Thailand,ltowvs,32
THA,Thailand,mas,34
THA,Thailand,pdi,64
THA,Thailand,uai,64
TRI,Trinidad and Tobago,idv,16
TRI,Trinidad and Tobago,ivr,80
TRI,Trinidad and Tobago,ltowvs,13
TRI,Trinidad and Tobago,mas,58
TRI,Trinidad and Tobago,pdi,47
TRI,Trinidad and Tobago,uai,55
TUR,Turkey,idv,37
TUR,Turkey,ivr,49
TUR,Turkey,ltowvs,46
TUR,Turkey,mas,45
TUR,Turkey,pdi,66
TUR,Turkey,uai,85
UKR,Ukraine,idv,55
UKR,Ukraine,ivr,14
UKR,Ukraine,ltowvs,86
UKR,Ukraine,mas,27
UKR,Ukraine,pdi,92
UKR,Ukraine,uai,95
URU,Uruguay,idv,36
URU,Uruguay,ivr,53
URU,Uruguay,ltowvs,26
URU,Uruguay,mas,38
URU,Uruguay,pdi,61
URU,Uruguay,uai,98
USA,U.S.A.,idv,91
USA,U.S.A.,ivr,68
USA,U.S.A.,ltowvs,26
USA,U.S.A.,mas,62
USA,U.S.A.,pdi,40
USA,U.S.A.,uai,46
VEN,Venezuela,idv,12
VEN,Venezuela,ivr,100
VEN,Venezuela,ltowvs,16
VEN,Venezuela,mas,73
VEN,Venezuela,pdi,81
VEN,Venezuela,uai,76
VIE,Vietnam,idv,20
VIE,Vietnam,ivr,35
VIE,Vietnam,ltowvs,57
VIE,Vietnam,mas,40
VIE,Vietnam,pdi,70
VIE,Vietnam,uai,30
ZAM,Zambia,idv,35
ZAM,Zambia,ivr,42
ZAM,Zambia,ltowvs,30
ZAM,Zambia,mas,40
ZAM,Zambia,pdi,60
ZAM,Zambia,uai,50
"""



# Save to JSON
output_path="culture_map_data.json"
with open(output_path, "w") as json_file:
    json.dump(culture_map_data, json_file, indent=4)
print(f"Data saved to {output_path}")

data = pd.read_csv(StringIO(hofstede_data))

# Convert the data into the hierarchical JSON structure
hierarchical_data = []
unique_countries = data["country"].unique()

for country in unique_countries:
    country_data = data[data["country"] == country]
    scores = {
        row["cultural dimension"]: int(row["Value"])  # Convert to Python int
        for _, row in country_data.iterrows()
    }
    hierarchical_data.append({
        "id": int(country_data.index[0]),  # Convert index to int
        "name": country,
        "datamapId": country_data.iloc[0]["ctr"],
        "isoCode": None,  # Add ISO codes if available
        "isoShortCode": None,  # Add short ISO codes if available
        "scores": scores
    })

# Save to a JSON file
output_path = "hofstede_data.json"
with open(output_path, "w") as json_file:
    json.dump(hierarchical_data, json_file, indent=4)

print(f"Data saved to {output_path}")