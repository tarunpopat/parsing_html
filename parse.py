import requests
import re
import urllib.request, urllib.parse, urllib.error
from openpyxl import Workbook

link = 'https://www.census2011.co.in/data/district/365-satara-maharashtra.html'
f = requests.get(link)



text = f.text
le = len(text)

taluka_pages = list()
taluka_names = list()

mts = text.find('<div class="table-responsive">')
#print('Table start:-',mts)
text_tabs = text[mts:]
#t1 = text_tabs[mts:mts+20]
#print(t1)
mte = text_tabs.find('</div>')

mt = text[mts:mts+mte]

all = re.findall('<a',mt )
al = len(all)

print('Total links:-', al)
mt1 = mt


for i in range(len(all)): # getting all the taluka links

    lts = mt.find('<a ') #linkTaluka start
    lte = mt.find('</a') #linkTaluka end
    lita = mt[lts:lte+4]
    #print('Link Taluka:-',lita)

    ls = lita.find('=') # Extrackting Link
    le = lita.find('>')
    li = lita[ls+2:le-1]
    link =  'https://www.census2011.co.in' + li #+'\''
    #print('Link:-',link)
    taluka_pages.append(link)

    tas = lita.find('>') #Extracting Taluka
    tae = lita[tas:].find('<')
    taluka = lita[tas+1:tas+tae]
    #print('Taluka:-',taluka, '\n')
    mt = mt[lte+2:]
    taluka_names.append(taluka)
    #print(mt[0:100])
'''
k=1
for i in taluka_names:
    print(k, "  ", i)
    k=k+1
'''
'''
k=1
for i in taluka_pages:
    #print(k, "  ", i)
    k=k+1
'''

village_names = list()
village_pages = list()
r = 0
#getting all the village links insdie the taluka
for i in taluka_pages:



        url = i
        w = requests.get(url)
        taluka_page_text = w.text
        #print(taluka_page_text)
        #print('Before finding main table')

        mts1 = taluka_page_text.find('<th class="alignleft">Villages</th>')
        text_tabs1 = taluka_page_text[mts1:]
        mte1 = text_tabs1.find('</tbody')
        mt_taluka = taluka_page_text[mts1:mts1+mte1]
        #print(mt_taluka)

        all1 = re.findall('<a', mt_taluka)
        al1 = len(all1)

        print('Total links in',i[35:65], ':-', al1)


        for n in range(len(all1)):
            #print('Inside 2nd For', q+1)

            ltvs = mt_taluka.find('<a') #linkevillage start
            ltve = mt_taluka.find('</a') #linkvillage end
            livi = mt_taluka[ltvs:ltve+4]  # link name and village name
            #print(livi)
            lvs = livi.find('=') # Extrackting Link
            lve = livi.find('>')
            lv = livi[lvs+2:lve-1]
            #print(lv)
            link1 =  'https://www.census2011.co.in' + lv #+'\''
            #print('Link:-',link)
            village_pages.append(link1)

            vis = livi.find('>') #Extracting Taluka
            vie = livi[vis:].find('<')
            village = livi[vis+1:vis+vie]
            #print(village)
            #print('Taluka:-',taluka, '\n')
            mt_taluka = mt_taluka[ltve+2:]
            village_names.append(village)



'''
c=0
o = len(village_names)
print('Total Villages:- ', o)
for v in village_pages:
    if c>10:
        break

    print(v)
    c=c+1
'''
male_pop = list()
female_pop = list()
for p in village_pages:

    url1 = p
    w1 = requests.get(url1)
    village_page_text = w1.text

    mfts = village_page_text.find('<th>Male</th>')
    mfte = village_page_text.find('Child (0-6)</td>')
    mft = village_page_text[mfts:mfte]

    pop = mft.find('Population')

    mft1 = mft[pop+2:]

    bend = mft1.find('</b>')
    b = mft1[bend:]
    tdst = b.find('<td>')
    tds = b[tdst:]
    ms = tds.find('<td>')
    me = tds.find('</td>')
    male = tds[ms+4:me]
    mf = tds[me+2:]
    fs = mf.find('<td>')
    fe = mf.find('</td>')

    female = mf[fs+4:fe]

    male_pop.append(male)
    female_pop.append(female)


workbook = Workbook()
sheet = workbook.active

ColA=list()
ColB=list()
ColC=list()

sheet["A1"]='Village'
sheet["B1"]='Male pop'
sheet["C1"]='Female pop'
sheet["D1"]='Village url'
q = 1
for y in village_names:
    A = 'A'+str(q+1)
    sheet[A] = y
    q=q+1

print('Column A - VILLAGE NAMES DONE!!!')

q=1
for m in male_pop:
    B = 'B'+str(q+1)
    sheet[B] = m
    q=q+1

print('Column B - Male population DONE!!!')

q=1
for f in female_pop:
    C = 'C'+str(q+1)
    sheet[C] = f
    q = q+1

print('Female Population done')

q=1
for c in village_pages:
    D = 'D'+str(q+1)
    sheet[D] = c
    q=q+1


print('length of vilage pages:-', len(village_pages))
print('length of vilages:-', len(village_names))
print('length of male pop list:-', len(male_pop))
print('length of female pop list:-', len(female_pop))


workbook.save(filename="Village_Male_female_pop.xlsx")











#print('\n\n Tatal text length:-',le, '\n')
