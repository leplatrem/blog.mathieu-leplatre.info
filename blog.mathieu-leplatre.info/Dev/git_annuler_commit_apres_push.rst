Git : annuler proprement un commit après un push
################################################

:date: 2011-11-03 14:15
:tags: git, tips
:lang: fr

====================
Ce qu'il faut éviter
====================

Pour annuler des commits, il existe la commande ``git reset``. 

.. code-block :: bash

    git reset --hard HEAD~1
    HEAD is now at 444b1cf Rhoo

Celle-ci est pertinente tant que les commits n'ont pas été poussés. Git vous retiendra au ``push`` d'ailleurs :

.. code-block :: bash

    git push
    To /tmp/repo
     ! [rejected]        master -> master (non-fast-forward)
    error: failed to push some refs to '/tmp/repo'

En effet, à partir du moment où un commit existe sur le serveur, il est potentiellement utilisé
par des collaborateurs (*mergé, à la base d'une branche, etc.*). On pourrait faire le sale et forcer le push :

.. code-block :: bash

    git push -f
    Total 0 (delta 0), reused 0 (delta 0)
    To /tmp/repo
     + b67c343...444b1cf master -> master (forced update)

Mais il y a beaucoup mieux !

===================
Ce qu'il faut faire
===================

Annuler un commit, c'est finalement appliquer l'inverse de son **diff** ! 

On peut rediriger le diff des commits à annuler vers la commande ``patch --reverse`` :) 

.. code-block :: bash

    git diff HEAD^ | patch --reverse


Pour faire plus simple, il y a ``git revert`` !

Par exemple pour annuler les trois derniers commits : 

.. code-block :: bash

    git revert HEAD~3..HEAD

Ou pour annuler un commit en particulier : 

.. code-block :: bash

    git revert 444b1cff

Il suffit alors de pousser proprement le commit obtenu sur le
serveur. Les éventuels collaborateurs qui avaient basé leur travail sur les commits
annulés devront gérer les conflits au moment venu...
