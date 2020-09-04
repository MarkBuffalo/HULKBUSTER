# HULKBUSTER

## What does it do?

Checks if the Rogue Fitness products are in stock, and tells you which ones and which options are in stock, then opens a web browser and plays an alarm. Some features do not work. This is a work-in-progress.

### ![HULKBUSTER Terminal Output](https://i.imgur.com/8s4dtDo.gif)

After the script runs and detects an in-stock item, a web browser opens:

### ![Opened web browsers](https://i.imgur.com/QCPwowr.png)


## Install
```
git clone https://github.com/MarkBuffalo/HULKBUSTER.git
cd HULKBUSTER 
pip3 install -r requirements.txt
```
You now need to edit `products.txt`. Visit roguefitness.com and add products you want to search to products.txt, separated by new lines. A default list of products is included.

### Installation problems. 

Please note that Windows is not supported, only Linux/macOS. 

#### macOS

You may need to install homebrew. This is beyond the scope of the readme. Sorry!

#### Linux

Install Instructions should work out of the box.

#### Windows  
Not supported, but probably works.

## Run 
```
$ python3 hulkbuster.py


Welcome to HULKBUSTER! Let's park in front of 
Rogue Fitness until our gear is in stock!

  _  _ _   _ _    _  _____ _   _ ___ _____ ___ ___ 
 | || | | | | |  | |/ / _ ) | | / __|_   _| __| _ \
 | __ | |_| | |__| ' <| _ \ |_| \__ \ | | | _||   /
 |_||_|\___/|____|_|\_\___/\___/|___/ |_| |___|_|_\

[2020-07-27 @ 00:13:56] IN STOCK [Rogue Calibrated LB Steel Plates] [0.25LB Calibrated Plate - Pair]
[2020-07-27 @ 00:13:59] IN STOCK [Rogue Calibrated KG Steel Plates] [0.25KG Calibrated Plate - Pair]
[2020-07-27 @ 00:14:00] IN STOCK [Rogue Calibrated KG Steel Plates] [0.5KG Calibrated Plate - Pair]
```
