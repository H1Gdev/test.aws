#! /bin/bash

# System
echo [whoami]$(whoami)
echo [uname]$(uname -a)

# AWS
echo [CLI]$(aws --version)
echo [SAM]$(sam --version)

# C/C++
echo [gcc]$(gcc --version) # not installed.
echo [g++]$(g++ --version) # not installed.
echo [Make]$(make --version) # not installed.

# .NET
echo [.NET]$(dotnet --version) # not installed.

# Node.js
echo [Node.js]$(node --version)
echo [npm]$(npm --version)
echo [versions]$(node -p process.versions)

# Python
echo [Python]$(python --version)
echo [pip]$(pip --version)
echo [Python3]$(python3 --version)
echo [pip3]$(pip3 --version)
echo [sys.path]$(python -c "import sys;print(sys.path)")
echo [boto3]$(python -c "import boto3;print(boto3. __version__)")

# Java
echo [Java]$(java --version)
echo [Gradle]$(gradle --version) # not installed.
echo [Maven]$(mvn --version) # not installed.

# Git
echo [Git]$(git --version)
