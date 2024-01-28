# Load settings from file
def load_settings():
    with open('settings.txt') as f:
        settings = f.read()
    settings = settings.split('\n')
    d = {}
    for i in settings:
        pair = i.split('=')
        d[pair[0]]=int(pair[1])
    return d

# Print commands to console
def print_menu():
    print('''
            So here's the deal...
            
            map\t\tDisplays hex map
            \t\tInput "l", "ul", "ur", "r", "dr", "dl" to move on the map
            \t\tInput "loc" for output of current grid location
            \t\tInput "debug" for debug output
            play *\tSets track to *. use "help" for * to get options
            show *\tDisplays image to *. use "help" for * to get options
            help\tFor help output. You just did this to get here, or you're really struggling...
            exit\tExits mixmancer
            ''')