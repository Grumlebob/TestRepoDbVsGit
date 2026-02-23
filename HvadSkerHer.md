To forskellige ting:

1. Git vs DB - (Både gitlab og github)
   (https://gitlab.com/grumlebob-group/grumlebob-project)
   https://github.com/Grumlebob/TestRepoDbVsGit

1. Et eksemplar på hvordan man kan bruge github actions til at ex. flytte filer på en connected DataLocation.
   Hvordan viser vi github actions:
1. En box er linket til github
1. Box har instructions omkring hvad der sker
1. Github actions tager mappen "RawOutputs" som har nogle tilfældige .gmx eller andet og lægger ind i "HandledOutputs", med ny attribute.
1. Github ACtions gør det via en Branch der heder DatoOutputResults, og dermed også viser branching functionen, så de kan gøre ting concurrently.
