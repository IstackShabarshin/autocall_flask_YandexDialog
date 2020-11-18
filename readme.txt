Requirements:
    ubuntu_server_16.04
    python 3.5
    python3-venv

Install (all commands from project dir):
	Create a new venv python in project direction:
		python3 -m venv env
        
	Install libs:
        Open venv:
            source env/bin/activate
            
        Install:
            pip install update
            pip install --upgrade pip
            pip install -r requirements.txt
            
        Close venv:
            deativate
        
    Install systemd:
        Create new user for executing project:
            sudo useradd PROJECT_USER -g www-data
                where PROJECT_USER == name of new user

        Change project permissions:
            chmod -R 770 ./
            sudo chown -R U_ACCOUNT:www-data ./
                where U_ACCOUNT == name of your account
                
        Open install_packages/services/autocall_flask_YandexDialog.service and install_packages/services/natasha_parser.service:
            Replace PROJECT_USER -> name of executing account; 
                PROJECT_DIRECTORY -> global path of project directory
                
        Copy install_packages/services/*:
            sudo cp install_packages/services/* /etc/systemd/system/
            
        Enable service:
            sudo systemctl daemon-reload
            sudo systemctl enable autocall_flask_YandexDialog
            
        Check working:
            sudo systemctl start autocall_flask_YandexDialog
            systemctl status autocall_flask_YandexDialog
            
    Install nginx:
        sudo apt install nginx
        
        Copy conf file for nginx:
            sudo cp install_packages/nginx/autocall_flask_YandexDialog /etc/nginx/sites-availabe/
            
        Configuring nginx:
            sudo ln -s /etc/nginx/sites-availabe/autocall_flask_YandexDialog /etc/nginx/sites-enabled
            sudo rm /etc/nginx/sites-enabled/default
                remove default nginx page
            sudo systemctl nginx -t
                check that all correct 
            sudo systemctl restart nginx
Using:
	Nginx listening on localhost:80
    You can use port forwarding or change configuration of Nginx.
    So you can send test url's (need cookies) on "localhost:80/"
        or use "localhost:80/yandexDialog/" as webhook