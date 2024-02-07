//SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "./tokens/nf-token-metadata.sol";
import "./ownership/ownable.sol";

/**
 * @author Simone Pio Tosatto
 * @title CryptoNovusRacing
 * @dev New NFT
 */
contract CryptoNovusRacing is NFTokenMetadata, Ownable {
    /**
     * @dev the balance of the smart contract.
     */
    uint256 private SmartContractBalance;
    /**
     * @dev the tokenId for minting a new NFT.
     */
    uint256 private tokenId;
    /**
     * @dev cost of minting a car.
     */
    uint256 private singleCarMintingCost;
    /**
     * @dev The struct of a single CarNFT.
     */
    struct CarNFT {
        string name;
        string imagePath;
        uint256 uniqueSequenceNumber;
    }

    /**
     * @dev The collection of all cars.
     */
    CarNFT[] private cars;

    /**
     * @dev Contract constructor. Sets metadata extension `name` and `symbol`.
     */
    constructor() {
        tokenId = 0;
        nftName = "Crypto Novus Racing";
        nftSymbol = "CNR";
        singleCarMintingCost = 0.01 ether;
        SmartContractBalance = 0;
    }

    /**
     * @dev function for minting a new NFT token
     */
    function mint(string calldata _name, string calldata _tokenIPFSURI) external payable {
        require(msg.value >= singleCarMintingCost);
        SmartContractBalance+=singleCarMintingCost;
        super._mint(msg.sender, tokenId);
        super._setTokenUri(tokenId, _tokenIPFSURI);

        //create the Car object and assign the uniqueSequenceNumber
        CarNFT memory car = CarNFT(_name, _tokenIPFSURI, tokenId);

        cars.push(car);

        tokenId += 1;

        //refund if the msg.sender pays too much for the car
        if (msg.value > singleCarMintingCost)
            payable(msg.sender).transfer(msg.value - singleCarMintingCost);
    }

    /**
     * @dev Returns the data from given _tokenId
     * @param _tokenId of the car which needs to be returned.
     * @return name
     * @return imagePath
     * @return uniqueSequenceNumber
     */
    function getCarData(uint256 _tokenId)
        external
        view
        returns (string memory name, string memory imagePath, uint256 uniqueSequenceNumber)
    {
        CarNFT memory car = cars[_tokenId];
        return (car.name, car.imagePath, car.uniqueSequenceNumber);
    }

    /**
     * @dev Sets the cost of a single car ONLY THE OWNER OF THE SMART CONTRACT CAN CALL THIS FUNCTION
     * @param _singleCarMintingCost the cost in wei
     */
    function setSingleCarMintingCostInWEI(uint256 _singleCarMintingCost)
        external
        onlyOwner
    {
        singleCarMintingCost = _singleCarMintingCost;
    }

    /**
     * @dev Get the cost of a single car
     * @return _singleCarMintingCost the cost in wei
     */
    function getSingleCarMintingCostInWEI()
        external
        view
        returns (uint256 _singleCarMintingCost)
    {
        return singleCarMintingCost;
    }

    function addressToOwnedTokenIds(address _ownerAddress)
        external
        view
        returns (int256[] memory tokenIds)
    {
        // Instantiate a new array in memory with a length of the tokenId
        int256[] memory _tokenIds = new int256[](tokenId);
        for (uint256 t = 0; t < tokenId; t++) _tokenIds[t] = -1;
        // Search what tokens are owned by the _ownerAddress
        uint256 k = 0;
        for (uint256 i = 0; i < tokenId + 1; i++) {
            if (idToOwner[i] == _ownerAddress) {
                _tokenIds[k] = int256(i);
                k++;
            }
        }
        return _tokenIds;
    }

    function withdraw() onlyOwner external{
        payable(owner).transfer(SmartContractBalance);
    }
}