
utfCode = 'utf8'

def pullStringArray(buffer):
    l = int(buffer[0])
    if l < 128:
        return buffer[2:1+l]
    else:
        return buffer[3:1+l]
