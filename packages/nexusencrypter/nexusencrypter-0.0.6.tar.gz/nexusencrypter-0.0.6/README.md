# Nexus Encrypter Library

Made Using Zerafim Zmas\' Encrypter

Library Made By Odysseas Chryssos (@goldenboys2011)


Nexus Encrypter Is A Fast Encrypting Library Where You Can Use:

-   Random Keys
-   Custom Keys
-   Keys From .key Files

To Encrypt Text.

### Installing 

## Installing

## How to install

Open an new comand promt and type:
``` cmd
pip install nexusencrypter
```

Then you can import the library:

``` python
nexusencrypter.encrypt(text,key)
```
## Upgrading 
### How to upgrade

Open an new command promt and type:

``` cmd
pip install --upgrade nexusencrypter
```
After Finishing They Library Should Be Fully Upgraded
## Full Documentetion

### Full Library Documentetion here: 
#### https://nexus-encrypter.readthedocs.io/en/latest/index.html
  
## Functions

# Encrypt
Encrypts Using Set, Random Or From .key File Key
  Usage:

``` python
nexusencrypter.encrypt(text,key)
```

Can Replace key with filename.key to get key from file


# Decrypt
Decrypts Using Set Or From .key File Key
  Usage:

``` python
nexusencrypter.derypt(text,key)
```
Can Replace key with filename.key to get key from file


# Create

Creates An .key File With Set Or Random Key 

  Usage:

``` python
nexusencrypter.create(keyname,key)
```
Can Leave key empty for random key.


Not neccesary to type the key parameter,

``` python
nexusencrypter.create(keyname,key="")
```

is the same as

``` python
nexusencrypter.create(keyname)
```


## More Sources

-   <https://replit.com/@goldenboys20112/Nexus-Encrypter-Library>
-   <https://replit.com/@goldenboys20112/Nexus-Encrypter>
-   <https://replit.com/@talosuthlab/Nexus-Encrypter>
