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

  cryptoNovusAddress = "0xfdA3F0d48EEa60BD8e0508DE5D8b160701d6d664";
  cryptoNovus = new window.web3.eth.Contract(
    cryptoNovusABI,
    cryptoNovusAddress
  );

  // Access the decentralized web!
  console.log("DAPP STARTED");

  //display the cars
  console.log("mostro le macchine se esistono");
  addressToOwnedTokenIds(currentAccount).then(displayCars);
}

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

/*********************************************/
/* Smart Contract Method Calls               */
/*********************************************/

function getCarData(tokenId) {
  return cryptoNovus.methods.getCarData(tokenId).call();
}

function addressToOwnedTokenIds(ownerAddress) {
  return cryptoNovus.methods.addressToOwnedTokenIds(ownerAddress).call();
}

/*********************************************/
/*          Display Cars                     */
/*********************************************/


function displayCars(ids) {
  //$("#cars").empty();
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

          /* SLIDESHOW */
          var divNode = document.createElement("DIV");
          divNode.setAttribute("class", "mySlides fade");
          var imgNode = document.createElement("IMG");
          imgNode.setAttribute("src", effectiveImagePath);
          imgNode.setAttribute("style", "width: 100%");

          divNode.appendChild(imgNode);

          var textNode = document.createElement("DIV");
          textNode.setAttribute("class", "text");
          var testo = document.createTextNode("Name: " + car.name + " USQ: " + car.uniqueSequenceNumber);
          textNode.appendChild(testo);

          divNode.appendChild(textNode);

          document.getElementById("slideshow-container").appendChild(divNode);

          document.getElementById('next').click();
        });

        
      });
    }
  }
  
}
