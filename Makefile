# makefile to be used for expediently uploading code to connected Adafruit board and updated
MOUNTPOINT = /mnt
DIR = metro_board

code: $(DIR)/code.py
	for file in $(shell cd $(DIR) && ls *.py); do sudo cat $(DIR)/$$file | sudo tee $(MOUNTPOINT)/$$file >/dev/null; done
	# sync is necessary to fully flush buffer to device
	sudo sync

lib: $(DIR)/lib/
	sudo rm -r $(MOUNTPOINT)/lib
	sudo cp -r $(DIR)/lib $(MOUNTPOINT)/
	sudo sync
