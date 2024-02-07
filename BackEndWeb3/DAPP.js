var cryptoNovusAddress; //contract address
var cryptoNovus; //contract variable object
var costInWei; //costInWei of minting a car

Web3 = require("web3");

/*****************************************/
/* Detect the MetaMask Ethereum provider */
/*****************************************/
window.addEventListener("load", async function () {
  // this returns the provider, or null if it wasn't detected
  const provider = await detectEthereumProvider();
  if (provider) {
    startApp(provider); // Initialize your app
  } else {
    alert("Please install metamask :)", null, null);
    console.log("Please install MetaMask!");
    window.open("https://metamask.io/", "_blank");
  }
});

function startApp(provider) {
  // If the provider returned by detectEthereumProvider is not the same as
  // window.ethereum, something is overwriting it, perhaps another wallet.
  if (provider !== window.ethereum) {
    console.error("Do you have multiple wallets installed?");
    alert("Do you have multiple wallets installed?", null, null);
  }
  window.web3 = new Web3(window.ethereum);

  cryptoNovusAddress = CORRECT_ADDRESS;
  cryptoNovus = new window.web3.eth.Contract(
    cryptoNovusABI,
    cryptoNovusAddress
  );
  // get the minting cost of a car by calling the smart contract method and update the UI
  getSingleCarMintingCostInWEI().then(function (result) {
    console.log("The cost in wei is: " + result);
    costInWei = result;
    document.getElementById("carMintCostText").innerHTML =
      '<h2 style="text-align: center;color: white">Cost of creating a car: <br><br>' +
      result / 10 ** 18 +
      " Ξ</h2>";
  });

  // Access the decentralized web!
  console.log("DAPP STARTED");

  //display the cars
  console.log("mostro le macchine se esistono");
  addressToOwnedTokenIds(currentAccount).then(displayCars);
}

/**********************************************************/
/* Handle chain (network) and chainChanged (per EIP-1193) */
/**********************************************************/

/*
const chainId = ethereum.request({ method: "eth_chainId" });
handleChainChanged(chainId);

ethereum.on("chainChanged", handleChainChanged);

function handleChainChanged(_chainId) {
  // We recommend reloading the page, unless you must do otherwise
  window.location.reload();
}
/*

/***********************************************************/
/* Handle user accounts and accountsChanged (per EIP-1193) */
/***********************************************************/

let currentAccount = null;
ethereum
  .request({ method: "eth_accounts" })
  .then(handleAccountsChanged)
  .catch((err) => {
    // Some unexpected error.
    // For backwards compatibility reasons, if no accounts are available,
    // eth_accounts will return an empty array.
    console.error(err);
  });

// Note that this event is emitted on page load.
// If the array of accounts is non-empty, you're already
// connected.
ethereum.on("accountsChanged", handleAccountsChanged);

// For now, 'eth_accounts' will continue to always return an array
function handleAccountsChanged(accounts) {
  if (accounts.length == 0) {
    console.log("accounts.length è 0");
    // MetaMask is locked or the user has not connected any accounts
    console.log("Please connect to MetaMask.");
    document.getElementById("accountAddressText").innerHTML =
      '<h2 style="text-align: center;color: white">Driver address: <br><br>' +
      "{Please connect to MetaMask}" +
      "</h2>";
    $("#mintButton").css("background", "#F5F5F5");
    $("#mintButton").css("color", "#C3C3C3");
    $("#mintButton").css("cursor", "none");
    $("#mintButton").css("pointer-events", "none");
    $("#mintButton").prop("disabled", true);
  } else if (accounts[0] !== currentAccount) {
    $("#mintButton").removeAttr("style");
    $("#mintButton").removeAttr("disabled", true);
    currentAccount = accounts[0];
    document.getElementById("accountAddressText").innerHTML =
      '<h2 style="text-align: center;color: white">Driver address: <br><br>' +
      currentAccount +
      "</h2>";
    console.log(currentAccount);

    //display current user cars
    //display the cars
    console.log("mostro le macchine se esistono");
    addressToOwnedTokenIds(currentAccount).then(displayCars);
  }
}

/*********************************************/
/* Access the user's accounts (per EIP-1102) */
/*********************************************/

//CONNECT TO METAMASK BUTTON
document
  .getElementById("connectToMetaMaskButton")
  .addEventListener("click", function () {
    ethereum
      .request({ method: "eth_requestAccounts" })
      .then(handleAccountsChanged)
      .catch((err) => {
        if (err.code === 4001) {
          // EIP-1193 userRejectedRequest error
          // If this happens, the user rejected the connection request.
          console.log("Please connect to MetaMask.");
          document.getElementById("accountAddressText").innerHTML =
            "<h2>Driver address: <br><br>" +
            "{Please connect to MetaMask}" +
            "</h2>";
        } else {
          console.error(err);
        }
      });
  });

//MINT BUTTON
document
  .getElementById("mintButton")
  .addEventListener("click", async function () {
    console.log("HO CLICCATO IL BOTTONE");
    var _name = document.getElementById("newTokenName").value;
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:5000/output",
      async: "asynchronous",
      data: { _tokenNameData: _name },
      dataType: "text",
      success: function (data) {
        console.log(JSON.stringify(data));
        //dopo aver ricevuto l'URI per il file json da caricare sull'IPFS, invialo come parametro al metodo per mintare
        mint(_name, JSON.stringify(data));
      },
      error: function (request, status, error) {
        console.log(
          "Error: " + error + ", Request: " + request + ", status: " + status
        );
      },
    });
  });

/*********************************************/
/* Smart Contract Method Calls               */
/*********************************************/

function getCarData(tokenId) {
  return cryptoNovus.methods.getCarData(tokenId).call();
}

function getSingleCarMintingCostInWEI() {
  return cryptoNovus.methods.getSingleCarMintingCostInWEI().call();
}

function addressToOwnedTokenIds(ownerAddress) {
  return cryptoNovus.methods.addressToOwnedTokenIds(ownerAddress).call();
}

function mint(name, tokenIPFSHash) {
  // This is going to take a while, so update the UI to let the user know
  // the transaction has been sent
  $("#txStatus").text(
    "Generating your unique car on the blockchain. This may take a while..."
  );
  // Send the tx to our contract:
  return cryptoNovus.methods
    .mint(name, tokenIPFSHash)
    .send({ from: currentAccount, value: costInWei })
    .on("receipt", function (receipt) {
      $("#txStatus").text("Successfully created " + name + "!");
      // Transaction was accepted into the blockchain, let's redraw the UI
      addressToOwnedTokenIds(currentAccount).then(displayCars);
    })
    .on("error", function (error) {
      // Do something to alert the user their transaction has failed
      $("#txStatus").text("error sending the mint transaction");
    });
}

/*********************************************/
/*          Display Cars                     */
/*********************************************/
function displayCars(ids) {
  $("#cars").empty();
  for (id of ids) {
    if (id != -1) {
      var effectiveImagePath = "";
      //ESTRAI IMAGE PATH DAL JSON CARICATO
      getCarData(id).then(function (car) {
        // url (required), options (optional)
        console.log("ATTRIBUTO:");
        console.log(car.imagePath.replaceAll('"', ""));

        $.getJSON(car.imagePath.replaceAll('"', ""), function (jsonData) {
          // JSON result in `data` variable
          console.log("JSON:" + jsonData);
          console.log("JSON IMAGE: " + jsonData["image"]);
          effectiveImagePath = jsonData["image"];

          console.log(car);

          console.log("NIBBER: " + effectiveImagePath);
          $("#cars").append(`<div class="car">
            <ul>
              <li>Name: ${car.name}</li>
              <li>Unique Sequence Number: ${car.uniqueSequenceNumber}</li>
              <li>Image: <img src="${effectiveImagePath}"></li>
            </ul>
          </div>`);
        });

        
      });
    }
  }
}