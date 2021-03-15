#Author: Lucas Massoni Sguerra
#Institution: CRI - MINES ParisTech
#contact: lucas.sguerra@mines-paristech.fr
import smartpy as sp


class SponsoredVCG(sp.Contract):
    def __init__(self, owner):
        self.init(
            owner = owner,
            isOpen = sp.bool(False),
            ctrs = sp.map(l = {}),
            bids = sp.map(l = {}),
            agents = sp.map(l = {}),
            prices = sp.map(l = {}),
         )


    @sp.entry_point
    def transferOwnership(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.data.owner = params


    @sp.entry_point
    def updateCTRs(self, params):
        sp.verify(sp.sender == self.data.owner)
        sp.if (self.data.isOpen == False) :
            self.data.ctrs = params


    @sp.entry_point
    def openAuction(self, params):
        sp.verify(sp.sender == self.data.owner)
        sp.if (self.data.isOpen == False) :
            self.data.isOpen = True
            self.data.prices = ({})
            self.data.bids = ({})
            self.data.agents = ({})
            self.data.ctrs = params


    @sp.entry_point
    def bid(self, params):
        l = sp.local('l', sp.len(self.data.bids))
        self.data.bids[l.value] = (params)
        self.data.agents[l.value] = sp.sender


    @sp.entry_point
    def cancelAuction(self):
        sp.verify(sp.sender == self.data.owner)
        sp.if (self.data.isOpen) :
            self.data.isOpen = False
            self.data.bids = ({})
            self.data.agents = ({})
            self.data.ctrs = ({})


    @sp.entry_point
    def sorting(self):
        sp.verify(sp.sender == self.data.owner)
        l = sp.local('l', sp.len(self.data.bids))
        j = sp.local('j', l.value - sp.nat(1))
        sp.for x in self.data.bids.items():
            self.insertSort( x.key )
        self.closeAuction(2)


    @sp.sub_entry_point
    def insertSort(self, param):
        self.data.isOpen = False
        jx = sp.local('jx', param)
        jint = sp.local('jint', sp.to_int(param))

        def swap(i):
            tempBid = sp.local("tempBid", self.data.bids[nat(i)])
            tempAgent = sp.local("tempAgent", self.data.agents[nat(i)])
            self.data.bids[nat(i)] = self.data.bids[nat(i - 1)]
            self.data.agents[nat(i)] = self.data.agents[nat(i - 1)]
            self.data.bids[nat(i - 1)] = tempBid.value
            self.data.agents[nat(i - 1)] = tempAgent.value

        def nat(x):
            return sp.as_nat(x)

        sp.while ((nat(jint.value) > 0) & (self.data.bids[nat(jint.value)] >= self.data.bids[nat(jint.value - 1)]) ) :
            swap(jint.value)
            jint.value -= 1


    @sp.sub_entry_point
    def closeAuction(self, param):
        sp.if ( sp.len(self.data.bids) > 0 ) :
            lenCtr = sp.local("lenctr", sp.len(self.data.ctrs))
            self.data.ctrs[lenCtr.value] = 0
            i = sp.local('i', 0)
            jc = sp.local('jc', 0)
            price_i = sp.local("price_i", 0)
            oneNat = sp.as_nat(1)
            sp.while ( (i.value < lenCtr.value) & (i.value < sp.len(self.data.bids)) ):
                price_i.value =  0
                jc.value =  i.value + oneNat
                sp.while ( jc.value < (lenCtr.value  + 1) ):
                    price_i.value = price_i.value + (self.data.bids[jc.value] * (self.data.ctrs[sp.as_nat(sp.to_int(jc.value) - 1)] - self.data.ctrs[jc.value]))
                    jc.value += 1
                self.data.prices[i.value] = price_i.value
                i.value += 1
            del self.data.ctrs[lenCtr.value]
