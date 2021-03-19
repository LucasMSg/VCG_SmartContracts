import sys
import os
import random


ctrs = sys.argv[2].split(',')


MichMapctrs = "{"
for x in range(len(ctrs)):
    MichMapctrs = MichMapctrs + str(x) + ": "
    MichMapctrs = MichMapctrs + str(ctrs[x] + ", ")
MichMapctrs = MichMapctrs[:-2] + "}"

#open files
fe = open("scriptE.js", "w")
ft = open("scriptT.js", "w")

#start_tezos
ft.write("const start = Date.now();\n")
ft.write("  console.log(start);\n")

fe.write("const start = Date.now();\n")
fe.write("  console.log(start);\n")

ft.write("const { MichelsonMap } = require('@taquito/taquito');\n")
ft.write("const VCG = artifacts.require('vcg2');\n")
ft.write("const newMap = new MichelsonMap({prim: 'map',args: [{ prim: 'int' }, { prim: 'int' }],})\n")
for x in ctrs:
    ft.write("newMap.set( " + str(ctrs.index(x)) + ", " + str(x) +" )\n")
ft.write("module.exports = async function(callback, accounts) {\n")
ft.write("const VCGdepl = await VCG.deployed();")

#start_ethereum
fe.write("const VCG = artifacts.require('VCG');\n")
fe.write("module.exports = async function(callback) {\n")
fe.write("        let accounts = await web3.eth.getAccounts();\n")

fe.write("const VCGdepl = await VCG.deployed();")
#Open auction Tezos
ft.write("  console.log("'"open auction"'");\n")
ft.write("const startOpen = Date.now();\n")
ft.write("  await VCGdepl.openAuction(newMap);\n")
ft.write("  const millisOpen = Date.now() - startOpen;\n")
ft.write("  console.log(`end test seconds elapsed = ${Math.floor(millisOpen / 1000)}`);\n")


#Open auction Ethereum
fe.write("	console.log("'"open auction here"'");\n")
fe.write("const startOpen = Date.now();\n")

fe.write("let openResult = await VCGdepl.openAuction([")

for x in ctrs:
        fe.write(str(x)+",")

fe.seek(fe.tell() - 1, os.SEEK_SET)
fe.truncate()

fe.write("],{from: accounts[0]});\n")

fe.write("  const millisOpen = Date.now() - startOpen;\n")
fe.write("  console.log(`end test seconds elapsed = ${Math.floor(millisOpen / 1000)}`);\n")

#BID LOOP
for x in range(int(sys.argv[1])):

    ft.write("const start" + str(x) + "= Date.now();\n")
    fe.write("const start" + str(x) + "= Date.now();\n")

    ft.write("	console.log("'"bid '+ str(x) +'"'");\n")
    fe.write("	console.log("'"bid '+ str(x) +'"'");\n")

    bid = random.randint(1, 100)
    ft.write("  await VCGdepl.bid( " + str(bid) + ");\n")
    fe.write("let result"+ str(x) +" =  await VCGdepl.bid( " + str(bid) + ", {from: accounts[0]});\n")

    ft.write("  const millis" + str(x) + " = Date.now() - start" + str(x) + ";\n")
    ft.write("  console.log(`end test seconds elapsed = ${Math.floor(millis" + str(x) + " / 1000)}`);\n")
    fe.write("  const millis" + str(x) + " = Date.now() - start" + str(x) + ";\n")
    fe.write("  console.log(`end test seconds elapsed = ${Math.floor(millis" + str(x) + " / 1000)}`);\n")


#close auctions
ft.write("	console.log("'"close auction"'");\n")
fe.write("	console.log("'"close auction"'");\n")
ft.write("const startClose = Date.now();\n")
fe.write("const startClose = Date.now();\n")

ft.write("  await VCGdepl.sorting([["'"unit"'"]]);\n")
fe.write("  let result = await VCGdepl.sortAndPrice({gas: 8000000, from: accounts[0]});\n")


ft.write("  const millisClose = Date.now() - startClose;\n")
ft.write("  console.log(`end test seconds elapsed = ${Math.floor(millisClose / 1000)}`);\n")

fe.write("  const millisClose = Date.now() - startClose;\n")
fe.write("  console.log(`end test seconds elapsed = ${Math.floor(millisClose / 1000)}`);\n")

#end
ft.write("  const millis = Date.now() - start;\n")
ft.write("  console.log(`end test seconds elapsed = ${Math.floor(millis / 1000)}`);\n")
ft.write("	callback();\n")
ft.write("}\n")

fe.write("  const millis = Date.now() - start;\n")
fe.write("  console.log(`end test seconds elapsed = ${Math.floor(millis / 1000)}`);\n")
#results
fe.write("	console.log(openResult);\n")
fe.write("	let logsOPen = openResult.logs\n")
fe.write("	console.log(logsOPen);\n")

for x in range(int(sys.argv[1])):
    fe.write("	console.log(result"+ str(x) +");\n")
    fe.write("	let logsBid"+ str(x) +" = result"+ str(x) +".logs;\n")
    fe.write("	console.log(logsBid"+ str(x) +");\n")

fe.write("	console.log(result);\n")
fe.write("	let logsClose = result.logs;\n")
fe.write("	console.log(logsClose);\n")
fe.write("	callback();\n")
fe.write("}\n")

#close files
fe.close()
ft.close()
