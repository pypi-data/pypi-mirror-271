Nexus Encrypter Library
=======================

Made Using Zerafim Zmas' Encrypter

Library Made By Odysseas Chryssos (@goldenboys2011)

____________________________________________________________________________________

Nexus Encrypter Is A Fast Encrypting Library Where You Can Use:

- Random Keys
- Custom Keys
- Keys From .key Files

To Encrypt Text. 

____________________________________________________________________________________

Functions
=========
Encrypt

   Usage:

.. code-block:: python

   nexusencrypter.encrypt(text,key)

  Can Replace key with filename.key to get key from file
Decrypt

   Usage:

.. code-block:: python

   nexusencrypter.derypt(text,key)

  Can Replace key with filename.key to get key from file

Create 
    Creates An .key File With Set Or Random Key

    Usage:

.. code-block:: python

   nexusencrypter.create(keyname,key)
    
  Can Leave key empty for random key.

Not neccesary to type the key parameter, 

.. code-block:: python

   nexusencrypter.create(keyname,key="")


is the same as

.. code-block:: python

   nexusencrypter.create(keyname)

‎ 
________________________________________________________________
More Sources
============

- https://replit.com/@goldenboys20112/Nexus-Encrypter-Library

- https://replit.com/@goldenboys20112/Nexus-Encrypter

- https://replit.com/@talosuthlab/Nexus-Encrypter

