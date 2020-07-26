# HULKBUSTER

![Image of Yaktocat](https://i.imgur.com/yO15yxI.png)

## What does it do?

Checks if the Rogue Fitness products are in stock, and tells you which ones and which options are in stock, then opens a web browser and plays an alarm. Some features do not work. This is a work-in-progress.

## Install
```
git clone https://github.com/MarkBuffalo/HULKBUSTER.git
cd HULKBUSTER 
pip3 install -r requirements.txt
```
You now need to edit `products.txt`. Visit roguefitness.com and add products you want to search to products.txt, separated by new lines. A default list of products is included.

### Windows users.

Please note that Windows is not supported, only Linux/macOS. I have no idea if this will work correctly on a windows machine or not, and I don't care. If you don't have a mac or Linux machine, my advice is to try the following:

1. Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Download [Ubuntu](https://ubuntu.com/download/desktop)
3. [Install Ubuntu](https://www.youtube.com/watch?v=diIW3fgewhI) on the virtual box.
4. Run the install commands again.

## Run 
```
$ python3 hulkbuster.py
```
