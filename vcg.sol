//Author: Lucas Massoni Sguerra
//Institution: CRI - MINES ParisTech
//contact: lucas.sguerra@mines-paristech.fr

pragma solidity >=0.7.0 <0.8.0;

contract owned {

    constructor() { owner = msg.sender; }

    address payable owner;

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }


    function transferOwnership (address payable newOwner) external onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
}



contract VCG is owned {

    bool isOpen;
    uint[] private ctrs;
    uint[] private bids;
    address[] private agents;
    uint[] private prices;

    //Events
    event Open(
        uint[]  ctrs
        );

    event EndAuction(
        address[] agents,
        uint[] prices
        );

    event ErrorEvent(
       string error
        );


    constructor() {
        owner = msg.sender;
        isOpen = false;
    }

    function openAuction( uint[] calldata newCTRs ) external onlyOwner {
        if (!isOpen) {
            isOpen = true;
            delete prices;
            delete bids;
            delete agents;
            ctrs = newCTRs;
            emit Open(ctrs);
        }
        else{
            emit ErrorEvent("Ongoing auction");
        }
    }


    function updateCTRs ( uint[] calldata newCTRs ) external onlyOwner {
        if (!isOpen) {
                ctrs = newCTRs;
        }
    }


    function bid ( uint amount) external returns (uint numberOfBids){
        if (!isOpen) {
            emit ErrorEvent("auction not open yet");
            return 0;
        }
        else {
            bids.push(amount);
            agents.push(msg.sender);
            return bids.length;
        }
    }


    function closeAuction () public onlyOwner returns (uint[] memory Prices){
        isOpen = false;
        uint length = bids.length;
        if( bids.length > 0){

        uint[] memory data = bids;
        uint[] memory labels = bids;

        for (uint j = 0; j < length; j++) {
            labels[j] = j;
        }

        for (uint j = 0; j < length; j++) {
            uint i = j ;
            while ((i > 0) && (data[i] >= data[i - 1])) {
                swap(i, data, labels);
                i--;
            }
        }

        uint[] memory result = calculatePrice(labels);

        return result;
        }
        else {
            emit ErrorEvent ("No bids to be auctioned");
        }

    }


    function calculatePrice (uint[] memory labels) internal returns (uint[] memory ){
            for (uint i = 0; (i < ctrs.length && i < agents.length ) ; i++){
                uint price_i = 0;

                for (uint j = (i + 1); j < (ctrs.length + 1)  ; j++){
                    price_i = price_i + (getElement(bids,labels[j]) * (getElement(ctrs, j - 1) - getElement(ctrs, j)))  ;
                }
                prices.push(price_i);

            }
            emit EndAuction( agentsSlice() , prices);
            return prices;
    }


    function swap ( uint i, uint[] memory data, uint[] memory labels ) pure internal {
        uint tempData = data[i];
        uint tempLabels = labels[i];
        data[i] = data[i-1];
        labels[i] = labels[i-1];
        data[i-1] = tempData;
        labels[i-1] = tempLabels;
    }


    function agentsSlice () private view returns (address[] memory winners) {
        winners = new address[](ctrs.length);

        if(ctrs.length < agents.length) {
            for(uint i = 0; i < ctrs.length; i++){
                winners[i]  = (agents[i]);
            }
            return winners;
        }
        else {
            return agents;
        }
    }


    function cancelAuction () public {
        if (isOpen) {
            isOpen = false;
            if( bids.length > 0){
                delete bids;
                delete agents;
                delete ctrs;
            }
        }
    }


    function getElement (uint[] storage list, uint i) internal view returns (uint value) {
        if (i < list.length )
            return list[i];
        else return 0;
    }


    function isOPen() public view returns (bool) {
        return isOpen;
    }


}
