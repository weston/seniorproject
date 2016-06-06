javac -cp ./lib/bitcoinj-core-0.13.6-bundled.jar ./src/com/ericbirdsall/bolt/TransactionHandler.java ./src/com/ericbirdsall/bolt/AddressFaucet.java
#Compile the code

cd src
#Move into the home directory of the project

java -cp ../bitcoinj-core-0.13.6-bundled.jar: com.ericbirdsall.bolt.TransactionHandler
#java -cp /home/seniorproject/bolt/lib/bitcoinj-core-0.13.6-bundled.jar: com.ericbirdsall.bolt.TransactionHandler
#Run the java program

