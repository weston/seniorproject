package com.ericbirdsall.bolt;
import com.google.common.collect.ImmutableSet;
import org.bitcoinj.core.*;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.kits.WalletAppKit;
import org.bitcoinj.params.MainNetParams;
import org.bitcoinj.params.TestNet3Params;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongycastle.util.encoders.Hex;
import java.io.File;
import java.net.InetAddress;
import java.net.UnknownHostException;
//import org.bitcoinj.kits.WalletAppKit;

public class TransactionHandler {

	//Note: Sometimes this hangs 
	public static void main(String[] args) {
    	//NetworkParameters networkParameters = new TestNet3Params();
    	NetworkParameters networkParameters = new MainNetParams();
    	//Toggle this to use the main net or testnet
        //Logger LOGGER = LoggerFactory.getLogger(TransactionHandler.class);

    	WalletAppKit kit = new WalletAppKit(networkParameters, new File("./wallet"), "bolt-wallet-main");
        System.out.println("Starting to sync blockchain. This might take a few minutes");
        kit.setAutoSave(true);
        kit.startAsync();
        kit.awaitRunning();
        
        kit.wallet().allowSpendingUnconfirmedTransactions();
        System.out.println("Synced blockchain.");
	    Wallet wallet = kit.wallet();
	    System.out.println("Your wallet address is " + wallet.currentReceiveAddress());
        System.out.println("You've got " + kit.wallet().getBalance() + " in your pocket");
	    kit.stop();

	}

}
  