# COMP7005_Assignment2 Repository Guide

Welcome to the `COMP7005_Assignment2` repository. This guide will help you set up and run the provided scripts.

## **Table of Contents**

1. [Cloning the Repository](#cloning-the-repository)
2. [Prerequisites](#Prerequisites)
3. [Building and running the programs](#building-and-running-the-programs)

## **Prerequisites**

- Install [python](https://www.python.org/downloads/)

## **Cloning the Repository**

Clone the repository using the following command:

```bash
git clone https://github.com/iamBillyNguyen/COMP7005_Assignment2.git
```

Navigate to the cloned directory:

```bash
cd COMP7005_Assignment2
```

## **Building and running the programs**

### **Server**

To build and run the server program run:

```bash
python3 ./server.py -i <ip_address> -p <port>
```

### **Client**

To build and run the client program run:

```bash
python3 ./client.py -i <ip_address> -p <port> -f <filename>
```

### **Multiple Clients**

_(Disclaimer: This script is meant for testing)_

To build and run multiple clients run:

```bash
python3 ./run-multiple-clients.py -c <num_clients> -i <ip_address> -p <port> -f <filename>
```