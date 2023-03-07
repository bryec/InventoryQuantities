from ftplib import FTP
from datetime import datetime
import pandas as pd
import shutil

start = datetime.now()
ftp = FTP('ftp2.gzanders.com')
ftp.login('4CGunworks','McKinney801')

# Get All Files
files = ftp.nlst()

# Print out the files

print("Downloading...Zanders liveinv.csv")
ftp.retrbinary("RETR Inventory/zandersinv.csv" ,open("./zandersinv.csv", 'wb').write)

ftp.close()

end = datetime.now()
diff = end - start
print('All files downloaded for ' + str(diff.seconds) + 's')

df = pd.read_csv(
    "./zandersinv.csv",
    dtype={"upc": str, "msrp": float, "price1": float, "available": str},
    usecols=["upc","msrp","price1","available"]
)
df = df[["upc","msrp","price1","available"]]
df["upc"] = df["upc"].astype(str)  # convert UPC column to string
df.rename(columns = {'upc':'UPC','msrp':'MSRP','price1':'price1','available':'available'})
df.to_csv('./ZandersInventory.csv', index=False)


src_path = "./ZandersInventory.csv"
dst_path= "./Result/"
shutil.copy(src_path, dst_path)
