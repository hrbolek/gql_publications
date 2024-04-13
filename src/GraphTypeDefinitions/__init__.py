from typing import List, Union
import typing
import strawberry

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#

import datetime
import uuid

@strawberry.type(description="""Type for query root""")
class Query:
    from .Others import (
        publication_by_id,
        publication_page,
        publication_type_by_id,
        publication_type_page,
        author_by_id,
        author_page
    )

    publication_by_id = publication_by_id
    publication_page = publication_page
    publication_type_by_id = publication_type_by_id
    publication_type_page = publication_type_page
    author_by_id = author_by_id
    author_page = author_page


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

   
@strawberry.federation.type(extend=True)
class Mutation:
    from .Others import (
        publication_author_insert, 
        publication_author_update, 
        publication_author_delete,

        publication_insert,
        publication_update,
        publication_delete,

        publication_type_insert,
        publication_type_update,
        publication_type_delete
    )
    
    publication_author_insert = publication_author_insert
    publication_author_update = publication_author_update
    publication_author_delete = publication_author_delete

    publication_insert = publication_insert
    publication_update = publication_update
    publication_delete = publication_delete

    publication_type_insert = publication_type_insert
    publication_type_update = publication_type_update
    publication_type_delete = publication_type_delete

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, mutation=Mutation)
