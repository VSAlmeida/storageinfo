from pathlib import Path
import SoftLayer
import os
import sys
import pandas as pd
from prettytable import PrettyTable
from dotenv import load_dotenv
load_dotenv()
env_path = Path(os.path.dirname(os.path.abspath(__file__))) / '.env'
load_dotenv(dotenv_path=env_path)

if(os.getenv("API_USERNAME") == None or os.getenv("API_KEY") == None):
    print('''
To use this script it is necessary to provide some information
In case you didnt know where to get this information, go to the official github of the project:
https://github.com/vsalmeida/storageinfo
    ''')
    API_USERNAME = input('Enter your username: ')
    API_KEY = input('Enter your api key: ')
else:
    API_USERNAME = os.getenv("API_USERNAME")
    API_KEY = os.getenv("API_KEY")

client = SoftLayer.Client(username=API_USERNAME, api_key=API_KEY)
virtualManager = SoftLayer.VSManager(client)
bareMetalManager = SoftLayer.HardwareManager(client)
blockManager = SoftLayer.BlockStorageManager(client)
fileManager = SoftLayer.FileStorageManager(client)
option = "0"


def roundIOPS(capacity, iops, base=.25):
    iops_per_gb = int(iops) / int(capacity)
    return base * round(iops_per_gb/base)


def getStorageDetails(devices, mgr, deviceType):
    table = {"Device Type": [], "Device Name": [], "Storage Type": [],
             "Storage Name": [], "Capacity (GB)": [], "IOPs": [], "IOPs/GB": []}
    currentStorage = 0

    for device in devices:
        currentStorage += 1
        print("Loading " + deviceType + " Info: " +
              str(currentStorage) + "/" + str(len(devices)))
        blockStorage = mgr.get_storage_details(device['id'], 'ISCSI')
        fileStorage = mgr.get_storage_details(device['id'], 'NAS')
        for fs in fileStorage:
            if(fs != []):
                fileVolume = fileManager.get_volume_details(fs['id'])
                table['Device Type'].append(deviceType)
                table['Device Name'].append(device['hostname'])
                table['Storage Type'].append('File Storage')
                table['Storage Name'].append(fs['username'])
                table['Capacity (GB)'].append(fs['capacityGb'])
                table['IOPs'].append(fileVolume['provisionedIops'])
                table['IOPs/GB'].append(roundIOPS(fs['capacityGb'],
                                                  fileVolume['provisionedIops']))
        for bs in blockStorage:
            if(bs != []):
                blockVolume = blockManager.get_volume_details(bs['id'])
                table['Device Type'].append(deviceType)
                table['Device Name'].append(device['hostname'])
                table['Storage Type'].append('Block Storage')
                table['Storage Name'].append(bs['username'])
                table['Capacity (GB)'].append(bs['capacityGb'])
                table['IOPs'].append(blockVolume['provisionedIops'])
                table['IOPs/GB'].append(roundIOPS(bs['capacityGb'],
                                                  blockVolume['provisionedIops']))
    storageDetails = PrettyTable(
        ['Device Type', 'Device Name', 'Storage Type', 'Storage Name', 'Capacity (GB)', 'IOPs', 'IOPs/GB'])
    storageDetails.align['ID'] = 'l'
    for i in range(len(table['Device Name'])):
        storageDetails.add_row(
            [table['Device Type'][i], table['Device Name'][i], table['Storage Type'][i],
             table['Storage Name'][i], table['Capacity (GB)'][i], table['IOPs'][i], table['IOPs/GB'][i]])
    return {'table': storageDetails, 'data': table}


def virtualServer():
    try:
        return getStorageDetails(virtualManager.list_instances(), virtualManager, "Virtual Server")
    except SoftLayer.SoftLayerAPIError as e:
        print('Unable to authorize hosts. %s, %s ' %
              (e.faultCode, e.faultString))
        input()
        sys.exit()


def bareMetalServer():
    try:
        return getStorageDetails(bareMetalManager.list_hardware(), bareMetalManager, "Bare Metal Server")
    except SoftLayer.SoftLayerAPIError as e:
        print('Unable to authorize hosts. %s, %s ' %
              (e.faultCode, e.faultString))
        input()
        sys.exit()


def exportExcel(vsData, bmData, fileName):
    df = pd.DataFrame(
        {"Device Type": vsData['Device Type'] + bmData['Device Type'],
         "Device Name": vsData['Device Name'] + bmData['Device Name'],
         "Storage Type": vsData['Storage Type'] + bmData['Storage Type'],
         "Storage Name": vsData['Storage Name'] + bmData['Storage Name'],
         "Capacity (GB)": vsData['Capacity (GB)'] + bmData['Capacity (GB)'],
         "IOPs": vsData['IOPs'] + bmData['IOPs'],
         "IOPs/GB": vsData['IOPs/GB'] + bmData['IOPs/GB']})
    writer = pd.ExcelWriter(os.path.expanduser(
        "~/Desktop/") + fileName + '.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


def menu(option):
    if option == "1":
        vs = virtualServer()
        print(vs['table'])
        export = str(input('Export as Excel? (Y/N): '))
        if(export.upper() == "Y"):
            exportExcel(vs['data'], {"Device Type": [], "Device Name": [], "Storage Type": [
            ], "Storage Name": [], "Capacity (GB)": [], "IOPs": [], "IOPs/GB": []}, 'Export_vsi')
        return str(input('Another option? (Y/N): '))
    elif option == "2":
        bm = bareMetalServer()
        print(bm['table'])
        export = str(input('Export as Excel? (Y/N): '))
        if(export.upper() == "Y"):
            exportExcel(bm['data'], {"Device Type": [], "Device Name": [], "Storage Type": [
            ], "Storage Name": [], "Capacity (GB)": [], "IOPs": [], "IOPs/GB": []}, 'Export_bm')
        return str(input('Another option? (Y/N): '))
    elif option == "3":
        vs = virtualServer()
        bm = bareMetalServer()
        print('''
Virtual Server Infos
        ''')
        print(vs['table'])
        print('''
Bare Metal Server Infos
        ''')
        print(bm['table'])
        export = str(input('Export as Excel? (Y/N): '))
        if(export.upper() == "Y"):
            exportExcel(vs['data'], bm['data'], 'Export_vsi_and_bm')
        return str(input('Another option? (Y/N): '))
    elif option == "4":
        print("Bye Bye")
        return "4"


while option != "4" and option != "N":
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
MENU:
[1] - Virtual Server
[2] - Bare Metal Server
[3] - Virtual and Bare Metal Server
[4] - Exit
        ''')
    option = str(input('Choose an option: '))
    option = (menu(option)).upper()
