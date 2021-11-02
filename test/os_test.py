import platform

def os_test():
    get_os = platform.system()
    if get_os == "Windows":
        print("Windows")
    elif get_os == "Linux":
        print("Linux")
    elif get_os == "Darwin":
        print("Mac")
    else:
        print("Other System")

if __name__ == "__main__":
    os_test()
