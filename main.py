import grakn

grakn_uri = 'localhost:48555'
grakn_keyspace = 'grakn'

client = grakn.Grakn(grakn_uri)
session = client.session(grakn_keyspace)

tx = session.transaction(grakn.TxType.WRITE)
tx.query("""
    define
        name sub attribute datatype string;
        person sub entity, has name, plays parent, plays child;
        parentchild sub relationship, relates parent, relates child;
    """)
tx.commit()

tx = session.transaction(grakn.TxType.WRITE)
tx.query('insert isa person has name "Johnny Sr.";')
tx.query('insert isa person has name "Johnny Jr.";')
tx.query('match $prnt isa person has name "Johnny Sr."; $chld isa person has name "Johnny Jr."; insert (parent: $prnt, child: $chld) isa parentchild;')
tx.commit()

tx = session.transaction(grakn.TxType.READ)
people = tx.query('match $prnt isa person has name "Johnny Sr."; $chld isa person has name "Johnny Jr."; $prntchld(parent: $prnt, child: $chld) isa parentchild; get;')
for p in people:
    # print("{} name = {} (prnt) --> (chld) {} via relationship {}".format(p.get('p').id, "a", "a", "a"))
    pass
tx.close()

session.close()