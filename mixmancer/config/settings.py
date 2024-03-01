
# Load settings from file
def LoadSettings():
    with open('./assets/settings.txt') as f:
        settings = f.read()
    settings = settings.split('\n')
    d = {}
    for i in settings:
        pair = i.split('=')
        d[pair[0]]=int(pair[1])
    return d