import web3
import json


class Run():
    def __init__(self):
        with open("abi.txt", "r") as f:
            abi = json.load(f)
        self.w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.109:8545'))
        contractAddress = web3.Web3.toChecksumAddress("0xbB830B8fd3c520D9820062B1E8463835B3d047a0")

        self.con = self.w3.eth.contract(
            abi=abi,
            address=contractAddress
        )
#желт

    def reg_users(self, adr, log, fio, vs, kldtp, klnsh, pas):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.reg_driver(log, fio, vs, kldtp, klnsh).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)

    def reg_license(self, number, deadline, category, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.reg_license(number, deadline, category).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)

    def prolong_license(self, number, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.prolong_license(number).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)

    def reg_car(self, category, lifetime, market_price,  adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.reg_car(category, lifetime, market_price).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)

    def add_accident(self, number, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.add_accident(number).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)

    def add_fine(self, number, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.add_fine(number).transact({"from": adr})
        self.w3.eth.waitForTransactionReceipt(tx)


#синяя

    def get_adr(self, log):
        adr = self.con.functions.logins(log).call()
        return adr

    def get_user(self, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        users = self.con.functions.drivers(adr).call()
        return users

    def lisenses(self, nomer):
        licens = self.con.functions.licenses(nomer).call()
        return licens

#крас

    def pay_fee(self, amount, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.pay_fee(amount).transact({"from": adr, "value": amount})
        self.w3.eth.waitForTransactionReceipt(tx)

    def pay_fine(self, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.pay_fine().transact({"from": adr, "value": 10**19})
        self.w3.eth.waitForTransactionReceipt(tx)

    def payment_fee(self, nomer, value, adr):
        adr = web3.Web3.toChecksumAddress(adr)
        tx = self.con.functions.payment_fee(nomer).transact({"from": adr, "value": value})
        self.w3.eth.waitForTransactionReceipt(tx)

r = Run()
# print(r.lisenses(111))
# r.reg_license(111, 12052025, 2,"0x4788E1180653b6515153148eA1B052b89Fe17c2A")
# print(r.get_user("0x0d9831775b504D3d128A45295049A066B01e0e0B"))
# print(r.get_adr("Romanov"))
# r.reg_users("0x0d9831775b504d3d128a45295049a066b01e0e0b","Романов Роман Романович", "Romanov","123")
# adr = web3.Web3.toChecksumAddress("0x4A8Fd2f22f4179Af1DDde5F546BF7E68d2bD65AF")
# print(r.w3.eth.getBalance(adr))
# print(r.con.)
# l = r.fek.functions.retrieve().call()
# print(l)
