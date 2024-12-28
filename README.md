# Mario 2

![double pyramid](https://cs50.harvard.edu/x/2024/psets/1/mario/more/pyramids.png)

# Le problème à résoudre

Dans le jeu vidéo "Super Mario Bros." sorti en 1985, au début du premier niveau, Mario doit sauter
au dessus d'une pyramide de briques avec un trou au milieu.
Dans un fichier nommé `mario.py`, vous devez écrire un programme qui recrée cette pyramide avec le symbole `#` comme dans l'exemple ci-dessous (pyramide de 4).

```bash
$ python mario.py
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

Comme vous le voyez, le programme commence par demander à l'utilisateur la hauteur (`Height`) 
de la pyramide et attend un `int` en réponse. Une fois que l'utilisateur a répondu, le programme affiche la
pyramide sur la sortie standard.

> [!TIP]
> Pour transformer un `str`en `int`, il suffit d'utiliser la fonction `int()`

Si l'utilisateur ne rentre pas un `int` compris entre 1 et 8  inclus, il faut redemander sans afficher de message d'erreur, comme dans l'exemple ci-dessous.

```bash
$ python mario.py
Height: -3
Height: 15
Height: 3
  #  #
 ##  ##
###  ###
```

> [!TIP]
> Pour vérifier qu'une chaîne de caractères (`str`) contient uniquement des chiffres, vous avez la fonction `isdigit()` ([Doc str](https://docs.python.org/fr/3/library/stdtypes.html#str.isdigit))

Vous remarquez que l'espace entre les deux parties de la pyramide est toujours de 2 briques quelque soit la hauteur.


```bash
$ python mario.py
Height: 8
       #  #
      ##  ##
     ###  ###
    ####  ####
   #####  #####
  ######  ######
 #######  #######
########  ########
```


# Les tests

N'oubliez pas qu'il est important de tester son programme.
En effet, lorsque vous décidez de tester un programme cela vous amène à vous poser des questions
sur ce que fait votre programme et les cas particuliers.

Que se passe-t-il si l'utilisateur tape :
* un nombre négatif ?
* 0 ?
* un nombre positif
* des lettres ou des mots ?
* rien du tout ?

Nous avons tendance à faire confiance à la logique des utilisateurs mais, 
lorsque nous concevons un logiciel, nous devons imaginer des réponses qui 
ne correspondent à aucune logique.

> "La logique est le dernier refuge des gens sans imagination.” Oscar Wilde

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle
