def removeWhiteSpace(str):
    tmp = ''
    for i in str.split():
        tmp = tmp + i + ' '
    return tmp[0:-1]

def NormalizeURL(URL):
    if URL[0:2] == '//':
        return 'http:' + URL
    if URL[0:5] == '/app/':
        return 'https://cafebazaar.ir' + URL
    return URL
