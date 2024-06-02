import time

from datalayer.blockchain import Blockchain
from flask import *
# --libraries

# --project files

# --frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20


# --inline methode that runs parallel to the program
app = Flask(__name__)


@app.route('/')
#--the login page, home page
# def home():
#     return render_template('home.html')

#--global variables for flask web application

voterlist = [] #--to keep duplicates out
invisiblevoter = '' #--global variable used to hide voter's identity
voterkeys = {} #--voter's keys stored temporarily in this dictionary


@app.route('/signup', methods = ['POST'])
def votersignup():
    voterid = request.form['voterid']
    pin = request.form['pin']
    voterkeys['pin'] = pin
    voterkeys['aeskey'] = aes.get_private_key(voterid)
    global invisiblevoter

    """
    #####-------ZERO KNOWLEDGE PROOF-------########
    <<<<<<implemented by hashing the voterID appended by PIN>>>>>>
    """
    invisiblevoter = str(sha256((str(voterid)+str(pin)).encode('utf-8')).hexdigest())

#--Voter re-signup check
    if voterid not in voterlist:
        voterlist.append(voterid)

#--If condition satisfied, voter can be allowed to vote
#--his data will be written on the database
        with open('temp/VoterID_Database.txt', 'a') as voterdata:
            voterdata.write(str(sha256(str(voterid).encode('utf-8')).hexdigest()))
            voterdata.write("\n")
        return render_template('vote.html')
#--If not, the voter will be redirected to a different page.
    else:
        return render_template('oops.html')


@app.route('/vote', methods = ['POST'])
def voter():
#--the voter is eligible if reached this page.
#--hence his own keys will be generated.
    voterkeys['sk'],voterkeys['pk'] = enc.rsakeys()         #--voter public/private key pair generated here
    choice = request.form['candidate']


#--vote object created
    v1 = vote(invisiblevoter, int(choice), voterkeys['pk'])
    vote.inc_votecount()

#--votedata digitally signed and encrypted and sent to the temporary pool
    with open('temp/votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        encvotedata = v1.encryptvote()
        writer.writerow(encvotedata)

#--and broadcasted to other peers on the network
    pp.send_votedata_to_peer('192.168.0.135',9999,encvotedata)

    """
    This method mines new blocks after generation of every 2 votes
    Uncomment this method and comment the 'mineblocktimer()' method 
    to switch to 'vote count block mining' method - where block will be mined after 2 votes are generated and not on regular time intervals.
    """

    if vote.count%2==0:
        blockx = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")

    pass

    """
    Now the QR code containing the information about your PIN
    and private key is printed on the thank you page.
    """

    return redirect('/thanks')


@app.route('/thanks', methods = ['GET'])
def thank():
    #--thank you page
    qrname = tykh.generate_QR(voterkeys['sk'],voterkeys['pin'])
    return render_template('thanks.html', qrcode = qrname)






def main():
    # --Blockchain initialized and Genesis block added
    app.run(port = 5000)
    time1 = time.time()
    EVoting1 = Blockchain(1, b"\x02Ed\xc1\xe7\xe1", 20)
    Blockchain.display()
    time2 = time.time()
    duration = time2 - time1
    print("...................")
    print(duration)
    return


if __name__ == '__main__':

    main()
