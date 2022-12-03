import mailbox
f = open('data.txt', 'w')

def showMbox(mboxPath):
    box = mailbox.mbox(mboxPath)
    for msg in box:
        # print (msg['Subject'])
        if(msg['Subject'] != None):
            f.write(msg['Subject'])
        showPayload(msg)

        f.write('\n**********************************\n')
        # print


def showPayload(msg):
    payload = msg.get_payload()

    if msg.is_multipart():
        div = ''
        for subMsg in payload:
            # print (div)
            f.write(div)
            showPayload(subMsg)
            div = '------------------------------'
    else:
        # print (msg.get_content_type())
        f.write(msg.get_content_type())
        # print (payload[:200])
        f.write(payload[:200])


if __name__ == '__main__':
    showMbox('C:\\Users\\Joel Mathew\\Desktop\\gmail data\\All mail Including Spam and Trash-002.mbox')
    f.close()