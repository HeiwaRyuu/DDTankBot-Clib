####### WIND DIGITS ####### PROBLEM WITH 1, 4 AND 6
WIND_BASE_AOB = rb'\x13\x25\xA3\xFF\x17\x33\x6A\xFF\x15\x4B\xAB\xFF\x04\x43\xBD\xFF\x02\x49\xD0\xFF\x0B\x2F\x82\xFF\x0D\x55\xDB\xFF\x01\x74\xF3\xFF\x42\x60\x1B\xFF\x01\x74\xF3\xFF\x01\x4E\xEA\xFF\x05\x32\xA2\xFF\x01\x65\xF2\xFF\x02\x7F\xF5\xFF\x01\x93\xF7\xFF\x0A\xA1\xF8\xFF\x05\x9B\xF9\xFF\x01\x74\xF3\xFF\x01\x55\xEF\xFF\x03\x37\xB0\xFF\x01\x7C\xF5\xFF\x01\x90\xF7\xFF\x01\x67\xEE\xFF\x17\xB8\xFC\xFF\x2F\xCE\xFB\xFF\x19\xBA\xFC\xFF\x03\xAD\xFF\xFF\x01\x41\xC7\xFF\x03\x2C\xBB\xFF\x01\x1A\xAC\xFF\x02\x1C\xA8\xFF'
WIND_FIRST_DIGIT_OFFSET = 0x140 # 0x180
WIND_SECOND_DIGIT_OFFSET = WIND_FIRST_DIGIT_OFFSET + 0x80
POSITIVE_CODE_DICT = {-8930185:'0', -9519169:'1', -10871:'2', -4231313:'3', -16777216:'4', -9655700:'5', -15127271:'6', -8361406:'7', -138:'8', -9276737:'9'}
NEGATIVE_CODE_DICT = {-15456748:'0', -16777216:'1', -11518435:'2', -8370104:'3', -1710610:'4', -14862819:'5', -16777216:'6', -535144:'7', -15198195:'8', -16382456:'9'}



####### WIND DIGITS ####### PROBLEM WITH 0, 1 AND 5
WIND_BASE_AOB = rb'\x05\x15\x79\xFF\x13\x47\xAD\xFF\x03\x3F\xBF\xFF\x03\x54\xCE\xFF\x03\x3D\xCA\xFF\x16\x4C\x9D\xFF\x01\x75\xF3\xFF\x02\x88\xF7\xFF\x07\x6B\xDF\xFF\x0C\x90\xEF\xFF\x02\x43\xD7\xFF\x01\x4D\xE6\xFF\x01\x71\xF3\xFF\x05\x9B\xF9\xFF\x1A\xB7\xFC\xFF\x2E\xD6\xFE\xFF\x26\xC6\xFC\xFF\x07\x9D\xF7\xFF\x01\x74\xF3\xFF\x01\x55\xEF\xFF\x01\x4B\xD9\xFF\x01\x5E\xEE\xFF\x18\xB5\xFB\xFF\x94\xEC\xFC\xFF\x68\xE9\xFC\xFF\x41\xDC\xFD\xFF\x16\xB6\xFB\xFF\x0D\xAA\xFA\xFF\x0D\xAA\xFA\xFF\x01\x1A\xAC\xFF\x02\x23\xB5\xFF'
WIND_FIRST_DIGIT_OFFSET = 0x140 # 0x180
WIND_SECOND_DIGIT_OFFSET = WIND_FIRST_DIGIT_OFFSET + 0x80
POSITIVE_CODE_DICT = {-14205913:'0', -8323073:'1', -3167385:'2', -7912123:'3', -9605689:'4', -14205913:'5', -10113435:'6', -5270688:'7', -13290202:'8', -14342848:'9'}
NEGATIVE_CODE_DICT = {-10243485:'0', -8323073:'1', -541874:'2', -3185050:'3', -16777216:'4', -10243485:'5', -13929173:'6', -13620705:'7', -106:'8', -3881729:'9'}



####### WIND DIGITS ####### SEEMS TO HAVE NO PROBLEMS --> SEEMS TO WORK ON EXPEDITION, WILL TRY TO TEST IT ON REGULAR PVP AND DIFFERENT CLIENT
WIND_BASE_AOB = rb'\x15\x4B\xAB\xFF\x04\x43\xBD\xFF\x02\x49\xD0\xFF\x0B\x2F\x82\xFF\x0D\x55\xDB\xFF\x01\x74\xF3\xFF\x42\x60\x1B\xFF\x01\x74\xF3\xFF\x01\x4E\xEA\xFF\x05\x32\xA2\xFF\x01\x65\xF2\xFF\x02\x7F\xF5\xFF'
WIND_FIRST_DIGIT_OFFSET = 0x140 # 0x180
WIND_SECOND_DIGIT_OFFSET = WIND_FIRST_DIGIT_OFFSET + 0x80
POSITIVE_CODE_DICT = {-12295612:'0', -15853544:'1', -8885938:'2', -11522257:'3', -15066568:'4', -7814008:'5', -14602207:'6', -12569827:'7', -15724537:'8', -14277040:'9'}
NEGATIVE_CODE_DICT = {-9982873:'0', -13412264:'1', -12166:'2', -4231570:'3', -1:'4', -11566001:'5', -16248824:'6', -4744347:'7', -1579152:'8', -9210961:'9'}


# pos			neg	
# 0	4282671684		0	4284984423
# 1	4279113752		1	4281555032
# 2	4286081358		2	4294955130
# 3	4283445039		3	4290735726
# 4	4279900728		4	UNKNOWN
# 5	4287153288		5	4283401295
# 6	4280365089		6	4278718472
# 7	4282397469		7	4290222949
# 8	4279242759		8	4293388144
# 9	4280690256		9	4285756335



## SAME AS LAST AOB BUT DIFFERENT VALUES:
WIND_BASE_AOB = rb'\x15\x4B\xAB\xFF\x04\x43\xBD\xFF\x02\x49\xD0\xFF\x0B\x2F\x82\xFF\x0D\x55\xDB\xFF\x01\x74\xF3\xFF\x42\x60\x1B\xFF\x01\x74\xF3\xFF\x01\x4E\xEA\xFF\x05\x32\xA2\xFF\x01\x65\xF2\xFF\x02\x7F\xF5\xFF'
WIND_FIRST_DIGIT_OFFSET = 0x140 # 0x180
WIND_SECOND_DIGIT_OFFSET = WIND_FIRST_DIGIT_OFFSET + 0x80
# POSITIVE_CODE_DICT = {:'0', :'1', :'2', :'3', :'4', :'5', :'6', :'7', :'8', :'9'}
# NEGATIVE_CODE_DICT = {-10493985:'0', :'1', :'2', :'3', -1:'4', :'5', :'6', :'7', :'8', :'9'}

# pos			neg	
# 0	4281430128		0	4284473311
# 1	4278190080		1	4285179242
# 2	4280973432		2	4287102975
# 3	4288102464		3	4288102464
# 4	4282532480		4	4278190080
# 5	4282941568		5	4282683279
# 6	4278190080		6	4294967179
# 7	4286611515		7	4290756476
# 8	4280564260		8	4284581985
# 9	4280231711		9	4280231711