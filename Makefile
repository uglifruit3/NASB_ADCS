MOUNTPOINT = /mnt
DIR = metro_board

code: code.py
	sudo rm $(MOUNTPOINT)/*.py
	sudo cp $(DIR)/*.py $(MOUNTPOINT)/

lib: lib/
	sudo rm -r $(MOUNTPOINT)/lib
	sudo cp -r $(DIR)/lib $(MOUNTPOINT)/
