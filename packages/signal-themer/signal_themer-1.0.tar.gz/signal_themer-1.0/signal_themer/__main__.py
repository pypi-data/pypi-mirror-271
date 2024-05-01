import os 
import platform
import sys
import shutil
import asarPy


# main function that extracts the asar, calls other functions and packs it
def theme_injector():
    app = app_path()
    temp = temp_path()
    theme_path = selected_theme()
    theme_name = os.path.split(theme_path)[1]

    if os.path.isdir(temp):
        shutil.rmtree(temp)
        
    asarPy.extract_asar(app, temp)
    shutil.copy(theme_path, os.path.join(temp, "stylesheets")) 
    import_theme(os.path.join(temp, "stylesheets", "manifest.css"), theme_name)
    asarPy.pack_asar(temp, app)

    shutil.rmtree(temp)

# returns path of signal-desktop
def app_path():
    match platform.system():
        case "Linux":
            return "/usr/lib/signal-desktop/resources/app.asar"
        case "Windows":
            return os.path.join(os.getenv("LOCALAPPDATA"), r"Programs\signal-desktop\resources\app.asar")

# returns temp directory depending on os in order to temporily store extracted asar
def temp_path():
    match platform.system():
        case "Linux":
            return "/temp/signal-themer/"
        case "Windows":
            return os.path.join(os.getenv("LOCALAPPDATA"), r"temp\signal-themer")

# add @import css in front of a file
def import_theme(file_path, theme):
    with open(file_path, "r+") as f:
        if f.readline().split(" ",1)[0] != "@import":
            f.seek(0)
        data = f.read()
        f.seek(0)
        f.truncate()
        f.write(f"@import '{theme}';\n"+data)

# reads user argument to read theme path
def selected_theme():
    if(len(sys.argv) != 2):
        sys.exit("Wrong number of argument, try `signal-themer <path-to-theme.css>`")
    elif(not os.path.isfile(sys.argv[1])):
        sys.exit("The theme you entered doesn't exist! Try again.")
    elif(not sys.argv[1].endswith(".css")):
        sys.exit("The theme must be a css file.")
    return sys.argv[1]

if __file__ == "__main__":
    theme_injector()
