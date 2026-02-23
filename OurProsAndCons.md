1. Git vs DB - (Både gitlab og github)
   (https://gitlab.com/grumlebob-group/grumlebob-project)
   https://github.com/Grumlebob/TestRepoDbVsGit

DB naturally supports Authorization.

Den kan ikke modelere dependencies

DB tools have plenty of common operations, like CRUD, etc. Also things like creating indexes, for what is being looked up. Git DOESN'T. It wants manual handling of files and then commiting changes.

Also DataLocations are often composite, based on Experiment and Inputbox - Git doesn't support composite keys naturally. This makes it more easy to reuse datalocations, like having a different experiment and inputbox point to same data location without storing it twice.

DB have stored procedures and triggers, and in general consumer producer patterns, with ACID properties.
Git have github actions.

Git = Utrolig visible. Inbygget UI. Query med clicks. DB kræver næsten en lille SQL forståelse eller egne byggede tools.

Git = Skal have beskeder.
DB = Mere silent, fordi det blot er row operationer.
