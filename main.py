import grakn

grakn_uri = 'localhost:48555'
grakn_keyspace = 'grakn3'

client = grakn.Grakn(grakn_uri)
session = client.session(grakn_keyspace)

tx = session.transaction(grakn.TxType.WRITE)
# tx.query("""
#     define
#         name sub attribute datatype string;
#         person sub entity, has name, plays parent, plays child;
#         parentchild sub relationship, relates parent, relates child;
#     """)
# tx.commit()

# tx = session.transaction(grakn.TxType.WRITE)
# tx.query('insert isa person has name "Johnny Sr.";')
# tx.query('insert isa person has name "Johnny Jr.";')
# tx.commit()

# tx = session.transaction(grakn.TxType.WRITE)
# tx.query('match $prnt isa person has name "Johnny Sr."; $chld isa person has name "Johnny Jr."; insert (parent: $prnt, child: $chld) isa parentchild;')
# tx.commit()

tx = session.transaction(grakn.TxType.WRITE)
name_type = tx.put_attribute_type("name", grakn.DataType.STRING)
person_type = tx.put_entity_type("person")
person_type.has(name_type)
parentchild_type = tx.put_relationship_type("parentchild")
parent_role = tx.put_role('parent')
child_role = tx.put_role('child')
parentchild_type.relates(parent_role)
parentchild_type.relates(child_role)
person_type.plays(parent_role)
person_type.plays(child_role)

person_johnny_sr = person_type.create()
person_johnny_jr = person_type.create()
sr = name_type.create("Johnny Sr.")
jr = name_type.create("Johnny Jr.")
person_johnny_sr.has(sr)
person_johnny_jr.has(jr)

parentchild = parentchild_type.create()
parentchild.assign(parent_role, person_johnny_sr)
parentchild.assign(child_role, person_johnny_jr)

tx.commit()


tx = session.transaction(grakn.TxType.READ)
people = tx.query('match $prnt isa person has name "Johnny Sr."; $chld isa person has name "Johnny Jr."; $prntchld(parent: $prnt, child: $chld) isa parentchild; get;')
for p in people:
    print("{} name = \"Johnny Sr.\" (prnt) --> (chld) name = \"Johnny Jr.\" via relationship {}".format(p.get('prnt').id, p.get('chld').id, p.get('prntchld').id))
tx.close()

session.close()