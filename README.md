# Every_day_Comics

We will create VK public group to post Randall Munroe Comics. 

## Let's start

### Prerequisites

Please be sure that **Python3** is already installed. 

### Installing
1. Clone the repository:
```
git clone https://github.com/MiraNizam/Every_day_Comics.git
```
2. Create a new virtual environment env in the directory
```
pip install virtualenv
```
```
cd <project_path>
```
```
python -m virtualenv env
```
3. Activate the new environment
```
source env/bin/activate (for Linux or any Posix)
``` 
```
env\Scripts\activate (for Windows)
```

4. Use pip (or pip3, if there is a conflict with Python2) to install dependencies in new environment:
```
pip install -r requirements.txt
```
5. Create empty file **.env** for your private data

6. Go to your [VK page](https://vk.com) and:
    - create a new group 
    - create a new app [manage_app](https://vk.com/apps?act=manage) *with standalone* type
    - add your **CLIENT_ID** in .env
    - get key access using [Implicit Flow](https://vk.com/dev/implicit_flow_user) You will need the following permissions: *photos*, *groups*, *wall* and *offline*. Remove the *redirect_uri* parameter
    - add your **VK_TOKEN** and **GROUP_ID** in .env
    - find actual VK version, now it 5.131 
    - add actual version as **VERSION** in .env
    - get group_owner_id: [ID](https://regvk.com/id/)
    - add your **GROUP_OWNER_ID** in .env
   
### How to run code 

```commandline
python vk_api.py
```
Go to the group and look at the new post. 