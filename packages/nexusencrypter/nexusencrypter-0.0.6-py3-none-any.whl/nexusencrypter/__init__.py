"""
Nexusencrypter - Python library for encryptind deencrypting and making keys.
"""


__version__ = "0.1.0"


#
# Encryption Logic Made By: Serafim Zmas
# Library Made By: Odysseas Chryssos (@goldenboys2011)
#


import random

print(f"ℹNexus Encrypter Has Been Installed Succesfully in version {__version__}\n")

def encrypt(text, key):
  given = ""
  items = ""
  nothing = []
  all_char = [
      "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d",
      "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
      "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F",
      "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
      "U", "V", "W", "X", "Y", "Z", ".", "?", "!", "<", ">", "(", ")", "{",
      "}", ":", "=", "…", ",", "'", '"', "[", "]", "«", "»", "#", "*", "@",
      "%", "^", "&", "$", ";", "|", "/", "~", "+", "-", "×", "÷", "≠", "≤",
      "≥", "≪", "≫", "√", " ", " ", " ", " ", " "
  ]
  given = ""
  # Checking if User Wants Random Key
  if key == "random":
    # Creating Randon Key
    all_char_to_encrypt=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",".","?","!","<",">","(",")","{","}",":","=","…",",","'",'"',"[","]","«","»","#","*","@","%","^","&","$",";","|","/","~","+","-","×","÷","≠","≤","≥","≪","≫","√"," ","秋","大","知","篋","陽","桑","達","人","父","主","庚","寓","言","劍","馬","遙","運","胠","子","木","駢","論","宗","楚","鬼","世","宥","地","繕","則","水","說","漁","篇","王","在","物","帝","生","拇","道","刻","意","方","雜","德","外","樂","跖","蹄","遊","應","養","符","盜","至","讓","間","寇","內","齊","北","師","御","逍","無","徐","列","性","₩","Ɇ","Ɽ","₮","Ɏ","Ʉ","ł","Ø","₱","₳","₴","Đ","₣","₲","Ⱨ","₭","Ⱡ","Ⱬ","Ӿ","₵","฿","₦","₥","山","乇","尺","ㄒ","ㄚ","ㄩ","卩","卂","丂","ᗪ","Ꮆ","卄","ﾌ","Ҝ","ㄥ","乙","乂","匚","ᐯ","乃","几","爪","甲","山","ヨ","尺","卞","と","凵","工","尸","丹","己","句","乍","呂","廾","勹","片","し","乙","メ","亡","レ","日","几","冊","🟥","🏾","🟨","🟩","⬜","🟧","⬛","❏","❐","❑","❒","◧","◨","◩","◫","∎","■","□","〓","⎔","💠","◎","🃜","🃚","🃖","🃁","🂭","🂺"]
    used2=[]
    key=""
    counter=0
    while counter!=112:

        random_char=random.choice(all_char_to_encrypt)
        if random_char not in used2:
            counter+=1
            all_char_to_encrypt.remove(random_char)
            used2.append(random_char)
            key+=random_char
    # Encrypting Using The Random Key Created
    given += text + "\n"
    all_charachters = key
    gaps = []
    nothing = []
    gaps.append(all_charachters[102])
    gaps.append(all_charachters[103])
    gaps.append(all_charachters[104])
    gaps.append(all_charachters[105])
    gaps.append(all_charachters[106])
    nothing.append(all_charachters[107])
    nothing.append(all_charachters[108])
    nothing.append(all_charachters[109])
    nothing.append(all_charachters[110])
    nothing.append(all_charachters[111])
    for item in given:
      if item == " ":
        items += random.choice(gaps)
      else:
        for i in all_char:
          if (item == i) and (item != " "):
            x = all_char.index(item)
            items += all_charachters[x]
      if (item not in all_char) and (item == "\n"):
        items += "\n"
      elif item not in all_char:
        items += item
    result = items
    # Returning The Encrypted Message
    return result
  else:
    # If User Dont Want Random Key
    # Check If Key Thet User Gave Is 112 char long
    if len(key) != 112:
      #If Not 112 Char Long
      #Check If Is A .Key File
      if key.endswith(".key"):
        try:
          #Open The .key File
          with open(key, "r") as file:
            key = file.read()
            #Check If The If Conent Is 112 Characters Long
            if len(key) != 112:
              print("ℹThe compressed form is incorrect \n")
            else:
              #If It Is 112 Characters Long Start Encrypting Use The Key From File
              given += text + "\n"
              all_charachters = key
              gaps = []
              nothing = []
              gaps.append(all_charachters[102])
              gaps.append(all_charachters[103])
              gaps.append(all_charachters[104])
              gaps.append(all_charachters[105])
              gaps.append(all_charachters[106])
              nothing.append(all_charachters[107])
              nothing.append(all_charachters[108])
              nothing.append(all_charachters[109])
              nothing.append(all_charachters[110])
              nothing.append(all_charachters[111])
              for item in given:
                if item == " ":
                  items += random.choice(gaps)
                else:
                  for i in all_char:
                    if (item == i) and (item != " "):
                      x = all_char.index(item)
                      items += all_charachters[x]
                if (item not in all_char) and (item == "\n"):
                  items += "\n"
                elif item not in all_char:
                  items += item
              result = items
              # Returning The Encrypted Message
              return result
        except FileNotFoundError:
          print("ℹFile not found. Please make sure the file exists. \n")

      else:
        print("ℹThe compressed form is incorrect \n")
    # If Key Length = 112 Characters
    else:
      #Encrypt Using Given Key
      given += text + "\n"
      all_charachters = key
      gaps = []
      nothing = []
      gaps.append(all_charachters[102])
      gaps.append(all_charachters[103])
      gaps.append(all_charachters[104])
      gaps.append(all_charachters[105])
      gaps.append(all_charachters[106])
      nothing.append(all_charachters[107])
      nothing.append(all_charachters[108])
      nothing.append(all_charachters[109])
      nothing.append(all_charachters[110])
      nothing.append(all_charachters[111])
      for item in given:
        if item == " ":
          items += random.choice(gaps)
        else:
          for i in all_char:
            if (item == i) and (item != " "):
              x = all_char.index(item)
              items += all_charachters[x]
        if (item not in all_char) and (item == "\n"):
          items += "\n"
        elif item not in all_char:
          items += item
      result = items
      # Returing The Encrypted Message
      return result

def decrypt(text, key):
  given = ""
  items = ""
  nothing = []
  all_char = [
      "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d",
      "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
      "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F",
      "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
      "U", "V", "W", "X", "Y", "Z", ".", "?", "!", "<", ">", "(", ")", "{",
      "}", ":", "=", "…", ",", "'", '"', "[", "]", "«", "»", "#", "*", "@",
      "%", "^", "&", "$", ";", "|", "/", "~", "+", "-", "×", "÷", "≠", "≤",
      "≥", "≪", "≫", "√", " ", " ", " ", " ", " "
  ]
  given = ""
  # Check If User Wants to use random key
  if key == "random":
    # Tease Message
    print("Bro You Can't Decrypt Using a Random Key. That's Stupid.🤦‍♂️ I'm Disappointed In You! \n")
  #If User Is Smart And Dont Want Random Key
  else:
    #Check If Key Thet User Gave Is 112 char long
    if len(key) != 112:
      #Check If Is A .key File
      if key.endswith(".key"):
        try:
          #Open The .key File
          with open(key, "r") as file:
            key = file.read()
            #Check If The If Conent Is 112 Characters Long
            if len(key) != 112:
              print("ℹThe compressed form is incorrect \n")
            else:
              #If It Is 112 Characters Long Start Decrypting Using The Key From File
              given += text + "\n"
              all_charachters = key
              gaps = []
              nothing = []
              gaps.append(all_charachters[102])
              gaps.append(all_charachters[103])
              gaps.append(all_charachters[104])
              gaps.append(all_charachters[105])
              gaps.append(all_charachters[106])
              nothing.append(all_charachters[107])
              nothing.append(all_charachters[108])
              nothing.append(all_charachters[109])
              nothing.append(all_charachters[110])
              nothing.append(all_charachters[111])
              for item in given:
                for i in all_charachters:
                  if item == i:
                    if item in gaps:
                      items += " "
                    elif item not in nothing:
                      x = all_charachters.index(item)
                      items += all_char[x]
                if (item not in all_charachters) and (item == "\n"):
                  items += "\n"
                elif (item not in all_charachters) and (item not in nothing):
                  items += item
              result = items
              # Return The Decrypted Message
              return result
        except FileNotFoundError:
          print("ℹFile not found. Please make sure the file exists. \n")

      else:
        print("ℹThe compressed form is incorrect \n")
    #If Key Len = 112
    else:
      # Decrypt Uing Given Key
      given += text + "\n"
      all_charachters = key
      gaps = []
      nothing = []
      gaps.append(all_charachters[102])
      gaps.append(all_charachters[103])
      gaps.append(all_charachters[104])
      gaps.append(all_charachters[105])
      gaps.append(all_charachters[106])
      nothing.append(all_charachters[107])
      nothing.append(all_charachters[108])
      nothing.append(all_charachters[109])
      nothing.append(all_charachters[110])
      nothing.append(all_charachters[111])
      for item in given:
        for i in all_charachters:
          if item == i:
            if item in gaps:
              items += " "
            elif item not in nothing:
              x = all_charachters.index(item)
              items += all_char[x]
        if (item not in all_charachters) and (item == "\n"):
          items += "\n"
        elif (item not in all_charachters) and (item not in nothing):
          items += item
      result = items
      # Return The Decrypted Message
      return result
        
### Create Key To File Function
def create(name, key=""):
  # Check If key is not "" to create key(if key = "" then creates random key if its not)
  if key != "":
    # Checks If key is 112 characters long
    if len(key) != 112:
      print("ℹThe compressed form is incorrect \n")
    else:
      #Creates .key File With Given Key
      with open(f"{name}.key", "w") as file:
        file.write(key)
    print(f"ℹThe key has been created succesfully and saved as {name}.key \n")
  else:
    #if key="" it creates random key
    all_char_to_encrypt=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",".","?","!","<",">","(",")","{","}",":","=","…",",","'",'"',"[","]","«","»","#","*","@","%","^","&","$",";","|","/","~","+","-","×","÷","≠","≤","≥","≪","≫","√"," ","秋","大","知","篋","陽","桑","達","人","父","主","庚","寓","言","劍","馬","遙","運","胠","子","木","駢","論","宗","楚","鬼","世","宥","地","繕","則","水","說","漁","篇","王","在","物","帝","生","拇","道","刻","意","方","雜","德","外","樂","跖","蹄","遊","應","養","符","盜","至","讓","間","寇","內","齊","北","師","御","逍","無","徐","列","性","₩","Ɇ","Ɽ","₮","Ɏ","Ʉ","ł","Ø","₱","₳","₴","Đ","₣","₲","Ⱨ","₭","Ⱡ","Ⱬ","Ӿ","₵","฿","₦","₥","山","乇","尺","ㄒ","ㄚ","ㄩ","卩","卂","丂","ᗪ","Ꮆ","卄","ﾌ","Ҝ","ㄥ","乙","乂","匚","ᐯ","乃","几","爪","甲","山","ヨ","尺","卞","と","凵","工","尸","丹","己","句","乍","呂","廾","勹","片","し","乙","メ","亡","レ","日","几","冊","🟥","🏾","🟨","🟩","⬜","🟧","⬛","❏","❐","❑","❒","◧","◨","◩","◫","∎","■","□","〓","⎔","💠","◎","🃜","🃚","🃖","🃁","🂭","🂺"]
    used2=[]
    key=""
    counter=0
    while counter!=112:

        random_char=random.choice(all_char_to_encrypt)
        if random_char not in used2:
            counter+=1
            all_char_to_encrypt.remove(random_char)
            used2.append(random_char)
            key+=random_char
            #saves key to file
            with open(f"{name}.key", "w") as file:
              file.write(key)
    print(f"ℹThe key has been created succesfully and saved as {name}.key \n")
