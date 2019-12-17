cd ~/Desktop/Door-Schedule-Display/DoorScheduleDisplay

clear

echo What is the document ID you got from the Google Docs URL?
read varname

python3 door_schedule_client.py doc $varname
