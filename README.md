# Grabby

Untested code. Use at your own risk. I think it should work, though. I'm running it and we'll find out. :)

# What does it do?

Checks if the Rogue Fitness grab bags and other products are in stock, and tells you which ones are in stock, then opens a web browser and plays an alarm.

# Install
```
git clone https://github.com/MarkBuffalo/grabby.git && cd grabby && pip3 install -r requirements.txt
```
You now need to edit `products.txt`. Visit roguefitness.com and add products you want to search to products.txt, separated by new lines.


# Docker Install
```
docker build -t grab .
docker run -it grab
```


# Run 
```
python3 grab.py
```
