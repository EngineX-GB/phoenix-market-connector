# Portable version

1. On Android, download Termux

2. Open Termux and run the command `termux-setup-storage`. This will allow termux to have access to the file system on the device.
You will be required to manually grant permissions on Android for Termux to have all permissions to the filesystem on the device.

3. Once granted, you'll see a folder called 'storage` appear in the current directory of the termux session:

>> `/data/data/com.termux/files/home`
>> `ls`

`storage`

4. cd into `/data/data/com.termux/files/home/storage`

You now have access to the device's file system. The same view that you see when connecting the device to your PC.


5. If you use Windows to access the device filesystem, then what you see in this filesystem view
   (e.g. This PC\MTP USB Device\Internal shared storage) will be mapped to the device location:
    `/data/data/com.termux/files/home/storage/shared`

6. Run `apt update`

7. Sometimes, python version 3.10 may not be available in the linux package repository. So run this command to check what version of 
python3 exists (if any) in the repo:

`apt-cache showpkg python3`

8. Install the variation of python 3 that is available in the linux package manager (e.g. python 3.12.11-1):

`apt-get install python` (downloads the available version in the linux repository manager e.g. python 3.12.11-1)

9. Check the version of python:
`python --version`

(e.g. `python 3.12.11`)


10. Do the required pip installations:

pip install beautifulsoup4==4.12.3 --no-input
pip install requests==2.31.0 --no-input
pip install cloudscraper==1.2.71 --no-input


11. In the device directory (`/data/data/com.termux/files/home/storage/shared`) create a folder called 'apps'

12. Copy the `install.sh` script from the connector project into the `/data/data/com.termux/files/home/storage/shared/apps`

13. CD into `/data/data/com.termux/files/home/storage/shared/apps`

14. Run the command to allow the install.sh script to execute.
`chmod +x script.sh`

15. Run the command to install a fresh copy of the connector
`sh install.sh --fresh`

16. NOTE: You must provide/ compose the config.properties and headers.json file and add/update these in the
    phoenix-v3/properties directory. Create it manually if required.


17. Now CD into the directory where the connector is installed:
`/data/data/com.termux/files/home/storage/shared/apps/phoenix-v3/src/bin`

18. Run the connector with any of the available commands: e.g.

`sh run.sh --region 1`

Library versions as of 18/10/2025:

bs4 4.12.3
requests 2.31.0
cloudscraper 1.2.71


Report to view on chrome brower on the device:

(Huawei Device, opera browser)
`file:///storage/emulated/0/dcim/phoenix/reports/main.html`

Motorola Device:
Note the modern chrome browsers don't support launching local html pages that run with 'file:///' protocol. 

