from neo4j import GraphDatabase 
class Sloth():
    def __init__(self,uri,Auth):
        self.uri = uri
        self.auth = Auth

    def create_node(self, nodes):
        """
        It creates nodes in the graph, you have to pass the nodes data as a list of dictionaries.
        """
        try:
            with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
                for node in nodes:
                    if "label" in node.keys():
                        labels = ":".join([node["label"]] if isinstance(node["label"],str) else node["label"])
                        query = f"CREATE (:{labels} $props)"
                        try:
                            with driver.session() as session:
                                session.run(query,props=node)
                        except Exception as e:
                            print(e)
                    else:
                        query = f"CREATE ($props)"
                        try:
                            with driver.session() as session:
                                session.run(query,props=node)
                        except Exception as e:
                            print(e)

        except Exception as e:
            print(e)
    # ===========================
    # ===========================
    # ===========================
    def read_node(self,query:str|dict):
        """
        It returns all nodes as a list of dictionary
        """
        try:
            with GraphDatabase.driver(self.uri,auth=self.auth) as driver:
                if query == "*":
                    with driver.session() as session:
                        records = session.run("MATCH (n) RETURN (n)")
                        res = list()
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id':int(node.element_id[-1])})
                            res.append(rec_properties)
                    return res
        except Exception as e:
            print(e)

