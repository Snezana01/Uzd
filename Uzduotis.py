#Ideja istraukti nereikalingus simbolius, visus zodzius nuskaityti is mazosios raides, bei sujungti dazniausiai 
#pasikartojancius "article, preposition" ir t.t
#juos apskaiciuoti kaip viena "OTHER" zodi, nes jie neturi dideles prasmes. 
#Bei paiziureti ar jie yra dazniausiai pasitaikanciose zodziose (greiciausiai taip ir bus)
#Atspausdinti 10 dazniausiai pasitaikanciu zodziu
from collections import Counter
import re
import os
list_of_files = ["text1.txt","text2.txt","text3.txt", "text4.txt"]
symbols = [',','\n','\t','\'','.','\"','!','?','-', '~']
basic = ["an", "a", "the", "as", "above", "across", "after", "at", "around", "before",
         "behind","below", "beside", "between", "by", "down", "during", "for", "from",
        "in", "inside", "onto", "of", "off", "on", "out", "through","to", "under",
         "up", "with", "and", "but", "because", "so", "or", "yet", "you", "his", "him",
         "her","he", "she", "it", "her", "far", "do", "did", "is", "was", "be", "we",
         "has", "are", "had", "not", "any", "no"]

def count_word(origin):
  #origin = open(file_name, 'r').read().lower()
  #print("Failui" + str(file_name) + "dažniausiai pasitaikantys žodžiai:")
  for i in symbols:
    origin = origin.replace(i, ' ')
  for j in basic:
    origin = re.sub(r"\b%s\b" % j, "OTHERS", origin)
  res = Counter(origin.split())
  to_list = [list(i) for i in res.items()]
  sortt = sorted(to_list, key = lambda x: x[1], reverse=True)
  return(sortt[:10])

from mpi4py import MPI

comm = MPI.COMM_WORLD   # komunikatorius
rank = comm.Get_rank()  # proceso numeris
size = comm.Get_size()  # procesų skaičius
print(size)
if rank == 0:
  for i in range(0, (len(list_of_files))):
    data = open(list_of_files[i], 'r').read().lower()
    comm.send(data, dest= (i+1), tag = (i+1))
    print("Procesui" + str(i+1) +"nusiusti failo" + str(list_of_files[i]) + "duomenys")
else:
  data = comm.recv(source=0, tag=rank)
  print("Proceso" + str(rank) + "skaiciavimai:")
  final = count_word(data)
  print(final)
