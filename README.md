# BM/VSI Storage Info

![GitHub repo size](https://img.shields.io/github/repo-size/vsalmeida/storageinfo)
![GitHub top language](https://img.shields.io/github/languages/top/vsalmeida/storageinfo)
![GitHub last commit](https://img.shields.io/github/last-commit/vsalmeida/storageinfo)
![Release Version](https://img.shields.io/github/v/release/vsalmeida/storageinfo)
![License](https://img.shields.io/github/license/vsalmeida/storageinfo)

Simple script created to get the file/block storage associated with BM and VSI on the IBM Cloud

## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting API Username](#getting-api-username)
- [Getting API Key](#getting-api-key)
- [Usage](#usage)
- [Contributing](#contributing)

## Prerequisites

To run this project you need to have installed

- [IBM Cloud API Username](#getting-api-username)
- [IBM Cloud API Key](#getting-api-key)
- [Python](https://www.python.org/downloads/) (Not required for the executable version)
- [Pip](https://pip.pypa.io/en/stable/) (Not required for the executable version)

## Installation

### Terminal version

First you need to clone this repository

```bash
git clone https://github.com/VSAlmeida/storageinfo.git
```

After that use the [pip](https://pip.pypa.io/en/stable/) package manager to install the dependencies.

```bash
pip install -r requirements.txt
```

### Executable version

For this version it is only necessary to download the [storage.rar](https://github.com/vsalmeida/storageinfo/releases/latest/download/storage.rar) file and extract it. Unfortunately this version is **only available for Windows**

## Getting API Username

- In the manage menu, click on Access(IAM)
- In the side menu, select Users
- Select your user
- Scroll down to the "VPN Password" section
- Copy the username for this session. Usually it will be the user's account number + "\_" + email. <br>Example: 1234567_example@example.com

## Getting API Key

- In the manage menu, click on Access(IAM)
- In the side menu, select Users
- Select your user
- Scroll down to the "API keys" section

If you already **have** an api key

- Click on the 3 dots to the right of your key
- Click details and copy it

If you **don't have** an api key

- Click on "Create classic infrastructure key" and copy it

## Usage

### Terminal version

After you have done the [installation](#installation) open the terminal in the directory where you cloned the project and run

```bash
python storage.py
```

### Executable version

After [downloading](#installation) the application, enter the project's root folder and double-click on the file storage.exe

### Common for both versions

- After starting the application you will be asked for your [api username](#getting-api-username) and [api key](#getting-api-key)
- After entering your credentials, you will be able to select with numbers 1- just vsi, 2- just bm and 3- both the resources (bm/vsi) that you want to list the associated file/block storage
- After the data is loaded, you can choose whether to export the data as excel with the letters Y(yes) or N(no)

### Nice Tip

Every time you start the application, it asks for your credentials, api username and api key. In case you didn't want to repeat this process every time, you can create a file with the name **.env** in the project's root folder with the following specifications

```.env
API_USERNAME=Your_API_Username
API_KEY=Your_API_Key
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
