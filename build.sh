# install gh cli
#TODO

# C++ Installation
if [ "$INSTALL_CPP" = "true" ]; then
    apt-get update
    apt-get install -y g++ cmake make libboost-all-dev libeigen3-dev
fi

# Java Installation
if [ "$INSTALL_JAVA" = "true" ]; then
    apt-get update
    apt-get install -y openjdk-17-jdk
fi