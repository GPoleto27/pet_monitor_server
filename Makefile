install:
	@echo "Installing packages..."
	@sudo apt-get update -y
	@sudo apt-get install -y pip mosquitto mosquitto-clients mariadb-server
	@sudo mosquitto_passwd -c /etc/mosquitto/passwd petmonitor
	@sudo cp mosquitto.conf /etc/mosquitto.conf
	@sudo mysql -u root -p < ./setup.sql
	@echo "Installing requirements..."
	@pip install -r requirements.txt --no-cache-dir

restart:
	@echo "Restarting MQTT broker..."
	@sudo systemctl restart mosquitto.service
	@echo "Restarting MariaDB..."
	@sudo systemctl restart mariadb.service

status_mqtt:
	@echo "Checking MQTT broker status..."
	@sudo systemctl status mosquitto.service

status_mariadb:
	@echo "Checking MariaDB status..."
	@sudo systemctl status mariadb.service

start:
	@echo "Starting Mosquitto..."
	@mosquitto -d
	@echo "Starting MariaDB..."
	@sudo systemctl start mariadb.service
	@echo "Starting the application..."
	@cd src && flask --env-file ../.env run 

stop:
	@echo "Stopping Mosquitto..."
	@sudo systemctl stop mosquitto.service
	@echo "Stopping MariaDB..."
	@sudo systemctl stop mariadb.service
	@echo "Stopping the application..."
	@sudo pkill -f flask