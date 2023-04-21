import os

for i in os.listdir("./mfw"):
    if i.endswith(".gif"):
        print(i)
        os.remove(f"./mfw/{i}")