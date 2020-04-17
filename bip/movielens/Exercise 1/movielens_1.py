#######################################################################################################################
"""
# Exercise 1
Write a program which performs the following tasks:
1. Download the Movielens datasets from the url ‘http://files.grouplens.org/datasets/movielens/ml25m.zip’
2. Download the Movielens checksum from the url ‘http://files.grouplens.org/datasets/movielens/ml25m.zip.md5’
3. Check whether the checksum of the archive corresponds to the downloaded one
4. In case of positive check, print the names of the files contained by the downloaded archive

## Answer to Exercise 1
"""
from urllib.request import urlretrieve, urlopen
import zipfile as zf
import hashlib as hl
import io
import os
import pandas as pd


print("Start of Exercise 1.\n")

## 1.1. download ml-25m.zip
zip_url = 'http://files.grouplens.org/datasets/movielens/ml-25m.zip'
zip_file_name = 'ml-25m.zip'
print("## 1.1. downloading '{}'...".format(zip_file_name))
urlretrieve(zip_url, zip_file_name)
print("## 1.1. '{}' has been downloaded in {}\n".format(zip_file_name, os.getcwd()))

## 1.2. download ml-25m.zip.md5
md5_url = 'http://files.grouplens.org/datasets/movielens/ml-25m.zip.md5'
md5_file_name = 'ml-25m.zip.md5'
print("## 1.2. downloading '{}'...".format(md5_file_name))
urlretrieve(md5_url, md5_file_name)
print("## 1.2. '{}' has been downloaded in {}\n".format(md5_file_name, os.getcwd()))

## 1.3. checksum check
print("## 1.3. checksum check")
### 1.3.1. evaluate checksum of ml-25m.zip file
print("### 1.3.1. evaluate checksum of ml-25m.zip file")
ml_zip_resp = urlopen(zip_url)
ml_zip_file = zf.ZipFile(io.BytesIO(ml_zip_resp.read()), mode='r')


def get_md5_checksum(file_path):
    with open(file_path, 'rb') as fh:
        md5 = hl.md5()
        while True:
            data = fh.read(8192)  # read in 8192-byte chunks
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()

checksum = get_md5_checksum(file_path=os.path.join(os.getcwd(), zip_file_name))
print("The MD5 checksum of '{}' is '{}'.".format(zip_file_name, checksum))

### 1.3.2. get checksum in md5 file
print("### 1.3.2. get checksum in md5 file")
ml_zip_md5_req = urlopen(md5_url)
checksum_md5 = ml_zip_md5_req.read().decode().split(' ')[0]
print("The MD5 checksum stated in '{}' is '{}'.".format(md5_file_name, checksum_md5))

### 1.3.3. final check
print("### 1.3.3. final check")
if checksum == checksum_md5:
    print('The two checksums match.\n')
else:
    print('The two checksums do not match.\n')

## 1.4. print names of the files in archive
print("## 1.4. print names of the files in archive")
print("Here is the list of the names of the files of '{}'.\n{}\n".format(zip_file_name, ml_zip_file.namelist()))

print("End of Exercise 1.\n")

#######################################################################################################################
