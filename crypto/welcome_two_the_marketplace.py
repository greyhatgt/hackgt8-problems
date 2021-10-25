# Welcome two the marketplace! 6a63616965763a795532574e465d5b32575d4e3349315d513257525d5a32505d51364e36463d7f
#######################################################################################################################

plain = "hackgt8{W0ULD_Y0U_L1K3_S0UP_X0R_S4L4D?}"

xorcipher = ""

key = 0x02

for i in range(0, len(plain)):
    xorcipher += (hex(ord(plain[i])^key)[2:])

print(xorcipher)

#xorcipher = "6a63616965763a795532574e465d5b32575d4e3349315d513257525d5a32505d51364e36463d7f"

xorplain = ""
for i in range(0, len(xorcipher), 2):
    xorplain += chr(int(xorcipher[i:i+2],16)^key)

print(xorplain)
