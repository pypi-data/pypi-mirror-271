import sys
import os

print("===")
print(sys.executable)
print("===")


if ".exe" in sys.executable and any("ESRI" in sub for sub in sys.path):
    print("fuck ESRI")
    env_base = os.path.dirname(sys.executable)

    paths = [env_base, os.path.dirname(os.path.realpath(__file__))]
    for dir in ["python39.zip", "DLLs", "lib", "site-packages"]:
        paths.append(os.path.join(env_base, dir))

    sys.path = paths

for pth in sys.path:
    print(pth)


sys.exit(0)
