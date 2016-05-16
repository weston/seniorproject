package com.ericbirdsall.bolt;
import com.google.common.collect.ImmutableSet;
import org.bitcoinj.core.*;
import org.bitcoinj.core.Wallet.SendRequest;
import org.bitcoinj.core.Wallet.SendResult;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.kits.WalletAppKit;
import org.bitcoinj.params.MainNetParams;
import org.bitcoinj.params.TestNet3Params;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;
import org.bitcoinj.script.ScriptOpCodes;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongycastle.util.encoders.Hex;
import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutionException;
import java.io.*;
import java.net.*;
import com.ericbirdsall.bolt.*;

public class TransactionHandler {

	//Note: Sometimes this hangs 
	public static void main(String[] args) throws AddressFormatException, InsufficientMoneyException, IOException {
    	NetworkParameters networkParameters = new TestNet3Params();
    	//NetworkParameters networkParameters = new MainNetParams();
    	//Toggle this to use the main net or testnet
        //Logger LOGGER = LoggerFactory.getLogger(TransactionHandler.class);

    	
    	File walletFile = new File("./wallet");	
    	WalletAppKit kit = new WalletAppKit(networkParameters, walletFile, "bolt-wallet");
        System.out.println("Starting to sync blockchain. This might take a few minutes");
        kit.setAutoSave(true);
        kit.startAsync();
        kit.awaitRunning();
        
        kit.wallet().allowSpendingUnconfirmedTransactions();
        System.out.println("Synced blockchain.");
        
        AddressFaucet addrFaucet = new AddressFaucet(kit.wallet());
    	addrFaucet.start();
    	
	    Wallet wallet = kit.wallet();
	    System.out.println("Your wallet address is " + wallet.currentReceiveAddress());
        System.out.println("You've got " + kit.wallet().getBalance() + " in your pocket");
        String faucetAddr = "mwmabpJVisvti3WEP5vhFRtn3yqHRD9KNP";
	    
        Address faucet = new Address(networkParameters, faucetAddr);
 
	    PeerGroup peerGroup = kit.peerGroup();
	    
    
//	    SendRequest request = SendRequest.to(faucet, Coin.MILLICOIN);
//	    Transaction t = request.tx;
//	    t.addOutput(Transaction.MIN_NONDUST_OUTPUT, new ScriptBuilder().op(ScriptOpCodes.OP_RETURN).data("fuck dennis".getBytes()).build());
//	    wallet.completeTx(request);
//	    wallet.commitTx(request.tx);
//	    kit.peerGroup().broadcastTransaction(request.tx);
//	    
//
//	    TransactionBroadcast tb = peerGroup.broadcastTransaction(request.tx);
//	    try {
//			tb.future().get();
//		} catch (InterruptedException e) {
//			System.out.println("FIRST LINE ERROR UH OH");
//			e.printStackTrace();
//		} catch (ExecutionException e) {
//			System.out.println("FIRST LINE ERROR UH OH");
//			e.printStackTrace();
//		}
//	    System.out.println("Sent transaction");
//	    System.out.println(t.getHashAsString());
	    
	    
	    

        
        kit.stop();

	}

}
  