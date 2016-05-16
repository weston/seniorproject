package com.ericbirdsall.bolt;
import org.bitcoinj.core.*;
import org.bitcoinj.params.TestNet3Params;
import java.io.IOException;
import java.io.*;
import java.net.*;

//This class defines the object for creating and distributing
//addresses in response to localhost client socket connections.
//This class object loops foreveer, waiting until it recieves
//a connection request from the front end.
public class AddressFaucet extends Thread {
	int port = 8050;
	Wallet wallet;
	ServerSocket server;
	public AddressFaucet(Wallet w) {
		wallet = w;
	}
	public void run(){	
		try {
			server = new ServerSocket(port);
		} catch (IOException e) {
			System.out.println("ERROR STARTING THE SERVER");
			e.printStackTrace();
		}
		
		while(true){
			Address newAddr = wallet.freshReceiveAddress();
			String addrString = newAddr.toString();
			System.out.println("LISTENING ON PORT " + port);
			try {
				Socket client = server.accept();
				PrintWriter out = new PrintWriter(client.getOutputStream(),true);
				out.println(addrString);
				client.close();
				
			} catch (IOException e) {
				System.out.println("ERROR WITH SOCKET");
				e.printStackTrace();
				return;
			}

			
			
			
			//Listen on the socket for the connection
			//WHen it recieves a connection
			//Send wallet address
			//Close connection

		}
		
	}
	
	public static void main(String args[]) {

	}
	

}
