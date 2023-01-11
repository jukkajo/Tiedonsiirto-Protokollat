import struct as s
#opkoodit
opk = [1, 2, 3, 4, 5]
#error-viestit
err_v = ["Not defined, see error message (if any).", "File not found.", "Access violation",\
         "Disk full or allocation exceeded.", "Illegal TFTP operation", "Unknown transfer ID",\
         "File already exists.", "No such user"]

#nollatavu
nt = bytes(opk[0])
moodi = "netascii"
kumpi= ["RRQ","WRQ"]
# 2 bytes     string    1 byte     string   1 byte
# ------------------------------------------------
# | Opcode |  Filename  |   0  |    Mode    |   0  |

#Read request (RRQ) - paketin luonti ja palautus
#tai WRQ request
#param 2, kertoo kumpi operaatio, 01 -> read 
def palauta_RRQ_tai_WRQ(tied_nimi, opr):
    q = nt
    if opr.upper() == kumpi[0]:
        q += bytes([opk[0]])
    
    elif opr.upper() == kumpi[1]:
        q += bytes([opk[1]])

    q += str.encode(tied_nimi) + nt
    q += str.encode(moodi) + nt
    
    return q

   
#========================================================

# 2 bytes     2 bytes      n bytes
# ----------------------------------
# | Opcode |   Block #  |   Data     |
    
#Data (DATA) - paketin luonti ja palautus
def palauta_DATA(data, tunniste):
    #block
    t_hex_mjono = s.pack(">H", tunniste)
    dat_paketti = nt + bytes([opk[2]]) + t_hex_mjono + data
    return dat_paketti
    
    
# 2 bytes     2 bytes
# ---------------------
# | Opcode |   Block #  |
                                                                          
#Acknowledgment (ACK) - paketin luonti ja palautus
def palauta_ACK(block_num):
    ack = nt + bytes([opk[3]]) + block_num
    return ack


#tämä saattaa jäädä hyödyntämättä

# 2 bytes     2 bytes      string    1 byte
# -----------------------------------------
# | Opcode |  ErrorCode |   ErrMsg   |   0  |
# err_v opk
#Error (ERROR) - paketin luonti ja palautus
def palauta_ERROR(err_koodi):
    error = nt + bytes([opk[4]]) + nt + bytes([err_koodi]) + s.pack(">H", err_v[err_koodi]) + nt
    return error

#=== Muuta kuin paketin generointia ===

# ack-paketti, onko validi
def varmista_ack(ack_data, tunniste):

    if ack_data[:2] == (nt + bytes([opk[3]])):
            #testataan block
            if int.from_bytes(ack_data[2:4], byteorder="big") == tunniste:
                return True
    else:
        return False
        
# data, onko validi
def varmista_data(data, tunniste):

    if data[:2] == (nt + bytes([opk[2]])):
            #testataan block
            if int.from_bytes(data[2:4], byteorder="big") == tunniste:
                return True
    else:
        return False
    
# palauttaa infon req-paketista
def palauta_req_info(data):
    osa_data = data[2:]
    t = osa_data.split(nt)[0].decode()
    return t
