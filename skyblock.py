#import baseItems

#async def getBaseItem(item_name, auction){
#    tiers = baseItems.tiers
#    reforges = baseItems.reforges
#    bases = baseItems.bases

    #Step 0: If this is an enchanted book, handle it with getBookBase()
#    if item_name == "Enchanted Book":
#        return getBookBase(auction)
#    }

#async def getBookBase(auction):
#    lore = auction.item_lore
#    base_name = lore.split("\n")[0] #Take the first line of the item lore
#    colors = ['4', 'c', '6', 'e', '2', 'a', 'b', '3', '1', '9', 'd', '5', 'f', '7', '8', '0', 'k', 'l', 'r', 'm', 'n', 'o']
#    for color in colors:
#        base_name = base_name.replace(f'§{}','') #removes all incidences of color codes
#    
#    return base_name
#}

#checkedItems = []

#async def assessAuction(auction, item, price, binn){
#    item_name = getBaseItem(auction[item], auction)
#    if item_name in itemlist:
#        if binn = True:
#            if(item_name not in checkedItems):
#                itemArray = []
#                itemArray.push('
#                    price: auction["starting_bid"],
#                    auctioneer: auction["auctioneer"],
#                    bin: auction.
#                ')
#                allAuctions.push({name: item_name,itemArray: itemArray})
#                checkedItems.push(item_name)
#            }
#            else{
#                let itemIndex = checkedItems.indexOf(item_name);
#                allAuctions[itemIndex].itemArray.push({
#                    price: auction.starting_bid,
#                    auctioneer: auction.auctioneer,
#                    bin: auction.hasOwnProperty('bin')
#                });
#            }
#            }
#    }
#}