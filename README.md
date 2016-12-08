# Air Breizh data

Quelques essais de récupération et danalyse des données de qualité de l'air
en Bretagne grâce au site http://www.airbreizh.asso.fr


## Petit reverse engineering

8 déc 2016 : analyse réseau de la page d'accueil (applet Flash).
Les données semblent passer par requête HTTP POST

(cf. [archive HAR](rev_eng/2016-12-08 Airbreizh Indices.har) + http://www.softwareishard.com/har/viewer/)

POST URL: http://www.airbreizh.asso.fr/index.php?id=36, with param q=demain

Réponse brute

done=1&Val=8&SO2=1&NO2=3&O3=2&PM10=8&city=1&1[Val]=5&1[SO2]=1&1[NO2]=2&1[O3]=2&1[PM10]=5&1[city]=2&2[Val]=6&2[SO2]=1&2[NO2]=2&2[O3]=2&2[PM10]=6&2[city]=4&3[Val]=6&3[SO2]=1&3[NO2]=2&3[O3]=2&3[PM10]=6&3[city]=5&4[Val]=8&4[SO2]=1&4[NO2]=5&4[O3]=2&4[PM10]=8&4[city]=6&5[Val]=8&5[SO2]=1&5[NO2]=2&5[O3]=2&5[PM10]=8&5[city]=9&laDate=01/12/2016&sortie=1480546800

Champs de la réponse splittée:

done=1
Val=8
SO2=1
NO2=3
O3=2
PM10=8
city=1

1[Val]=5
1[SO2]=1
1[NO2]=2
1[O3]=2
1[PM10]=5
1[city]=2

2[Val]=6
2[SO2]=1
2[NO2]=2
2[O3]=2
2[PM10]=6
2[city]=4

3[Val]=6
3[SO2]=1
3[NO2]=2
3[O3]=2
3[PM10]=6
3[city]=5

4[Val]=8
4[SO2]=1
4[NO2]=5
4[O3]=2
4[PM10]=8
4[city]=6

5[Val]=8
5[SO2]=1
5[NO2]=2
5[O3]=2
5[PM10]=8
5[city]=9

laDate=01/12/2016
sortie=1480546800

NB: il semble que la date soit fausse. Plus tard dans la journée du 8/12, la date
devient juste et les données changent.

