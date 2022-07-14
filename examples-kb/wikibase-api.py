"""
Examples of working with https://github.com/samuelmeuli/wikibase-api against a local/cloud-based Wikibase instance
Forked at https://github.com/KBNLresearch/wikibase-api
Wikibase instance is on https://kbtestwikibase.wikibase.cloud/
Docs/manual are on https://wikibase-api.readthedocs.io/en/latest/
See config.json for configuration variables and login credentials
See also https://github.com/samuelmeuli/python-wikibase
"""

from wikibase_api import Wikibase
wb = Wikibase(config_path="config.json")

############## Entities - items and properties (Qs and Ps) ====================
"""
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/entity.html
See also https://kbtestwikibase.wikibase.cloud/w/api.php?action=help&modules=wbeditentity
"""
# Add new empty entity, no content- It must be set to one of ["item", "property", "lexeme", "form", "sense"]
# Add empty Qnumber/item
r=  wb.entity.add("item", content=None)

# Add empty Property of datatype string
r=  wb.entity.add("property", content={"datatype":"string"})
# ... of datatype URL
r=  wb.entity.add("property", content={"datatype":"url"})
# ... of datatype ExternalId
r=  wb.entity.add("property", content={"datatype":"external-id"})
# ... of datatype Item
#r=  wb.entity.add("property", content={"datatype":"wikibase-item"})
# ... of datatype Monolingualtext
r=  wb.entity.add("property", content={"datatype":"monolingualtext"})
# ... of datatype Time
r=  wb.entity.add("property", content={"datatype":"time"})

# Remove property P34 (limited to users in the group: [[Project:Administrators|beheerders]].")
#r=  wb.entity.remove("Property:P34")

# Search (exact word match) for entities (items or properties) based on their labels and aliases
r=wb.entity.search("Koninklijke","nl", entity_type="item", limit=10, offset=None)

# Retrieve data - attributes =  ["info", "sitelinks", "aliases", "labels", "descriptions", "claims", "datatype"]
r = wb.entity.get(["Q1"], attributes=["labels"], languages=["nl"])

############## Claims (P-Q-pairs) ====================
"""
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/claim.html
# A statement consists of a property(P)-value(Q) pair, for example, "location: Germany."
# Statements can also be expanded upon, annotated, or contextualized with the addition of optional qualifiers, references, and ranks.
# The core part of a statement without references and ranks is also called claim. A claim without qualifiers is also referred to as snak.
"""
#r = wb.claim.get("Q1") # Does not work, as get() is not part of the wikibase-api code (see https://github.com/samuelmeuli/wikibase-api/blob/master/wikibase_api/models/claim.py)

# To item Q13 Add P3 ("is een") with value= Q2 ("nationale bibliotheek")
#r=wb.claim.add("Q13", "P3", {"entity-type":"item","numeric-id":2} , snak_type="value") # for the form of the value dict, see examples at https://kbtestwikibase.wikibase.cloud/w/api.php?action=help&modules=wbcreateclaim

# Remove the above claim from Q13 again - claim_id (GUID) = Q13$4D0A82B6-7845-4C32-8645-E1E2BF7E1968
# Claim ids in given Qitem (such as Q13) can be found via https://kbtestwikibase.wikibase.cloud/w/api.php?action=wbgetclaims&entity=Q13&format=json
#r=wb.claim.remove("Q13$D278686A-096F-4FA2-ACCF-482D4F9CFF73")

# Update claim: In Q13, in P3 (is een) replace Q2 ("nationale bibliotheek") with Q4 ("Centsprent")
#r=wb.claim.update("Q13$2527350F-F62C-4C46-8B99-A35D871F02B4", {"entity-type":"item","numeric-id":4} , snak_type="value")

################## Labels, Descriptions, Aliases ###########################
"""
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/label.html
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/description.html
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/alias.html
"""
## Add label in given language
#r = wb.label.set("Q13", "Une 2nd label en Francais", "fr") # Set label in fr
#Remove label
# r = wb.label.set("Q13", "", "fr") # Remove label in fr
## Add description in given language
#r = wb.description.set("Q13", "alalalal", "fr") #Set description in fr
#Remove description
#r = wb.description.set("Q13", "", "fr") # Remove description in fr
## Add 2 aliases in french
#r = wb.alias.add("Q13", ["fr alias 1", "fr alsias 2"], "fr")
## Add 1 more aliases in french
#r = wb.alias.add("Q13", "fr alias 3", "fr")
#Replace these 3 with 3 other aliases in french
#r = wb.alias.replace_all("Q13", ["fr alias 4", "fr alias 5", "fr alias 6"], "fr")
# Remove the 3rd alias
#r = wb.alias.remove("Q13", "fr alias 6", "fr")

############# Qualifiers ##############
"""
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/qualifier.html
"""
# Add qualifiers to claim
# Request claim ids (GUID) and qualifier hashes https://kbtestwikibase.wikibase.cloud/w/api.php?action=wbgetclaims&entity=Q13&format=json
claim_id = "Q13$2527350F-F62C-4C46-8B99-A35D871F02B4"
#r = wb.qualifier.add(claim_id, "P20", "De grote inkleurder")
r = wb.qualifier.add(claim_id, "P15", {"entity-type":"item","numeric-id":1} , snak_type="value")

# Remove last qualifier
qualifier_id="ad302cdb3e276bf57ecf049d9b17cb6213931d21"
#r = wb.qualifier.remove(claim_id, qualifier_id)

# Update first qualifiers to P15=Q1
qualifier_id="c8785aafbc7c6c6a768f5d13470f2ff68ff39527"
r = wb.qualifier.update(claim_id, qualifier_id, "P15", {"entity-type":"item","numeric-id":1} , snak_type="value")
print(r)

################ References #############################
"""
https://wikibase-api.readthedocs.io/en/latest/api_reference/models/reference.html
"""
# To add
