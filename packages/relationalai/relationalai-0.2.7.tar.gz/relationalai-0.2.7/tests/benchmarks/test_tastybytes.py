#pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.clients.snowflake import Snowflake
from relationalai.clients import config as cfg
from relationalai.std import aggregates, rel
from relationalai.std.graphs import Graph

from relationalai import debugging

def test_tastybytes(engine_config: cfg.Config):
    # TODO: move benchmark span to hook?
    with debugging.span("benchmark", name="tastybytes"):
        name = "LOYALTY_ORDERS_REGION_CALIFORNIA"
        # provider = rai.Resources(config=engine_config)
        # with debugging.span("clone"):
        #     name = "LOYALTY_ORDERS_REGION_CALIFORNIA_" + str(random.randint(1000000000, 9999999999))
        #     provider.clone_graph(name, "LOYALTY_ORDERS_REGION_CALIFORNIA")
        #     atexit.register(lambda: provider.delete_graph(name))
        
        model = rai.Model(name, config=engine_config)
        model._config.set("compiler.use_multi_valued", True)
        sf = Snowflake(model)
        Record = sf.TASTYBYTES.HARMONIZED.LOYALTY_ORDERS_REGION_CALIFORNIA

        Customer = model.Type("Customer")
        Truck = model.Type("Trucks")
        Transaction = model.Type("Transaction")
        RelevantConnection = model.Type("RelevantConnection")
        
        with model.query(tag="count_all") as select:
            record = Record()
            num_records = aggregates.count(record)
            select(num_records)

        # Define Customer Type
        with model.rule(dynamic=True):
            r = Record()
            Customer.add(customer_id=r.customer_id)

        # Check total number of customers
        with model.query(tag="count_customers") as select:
            record = Customer()
            num_records = aggregates.count(record)
            select(num_records)

        # Define Truck Type
        with model.rule():
            r = Record()
            Truck.add(truck_id=r.truck_id)

        # Check total number of trucks
        with model.query(tag="count_trucks") as select:
            record = Truck()
            num_records = aggregates.count(record)
            select(num_records)

        with model.rule():
            r = Record()
            Transaction.add(
                customer_id=r.customer_id,
                order_id=r.order_id,
                truck_id=r.truck_id,
                order_ts=r.order_ts,
                order_ts_seconds=r.order_ts_seconds,
                location_id=r.location_id,
            )

        with model.rule():
            t1 = Transaction()
            t2 = Transaction()

            t1.truck_id == t2.truck_id
            t1.customer_id != t2.customer_id
            rel.abs(t1.order_ts_seconds - t2.order_ts_seconds) <= 1200

            t1.connected.add(t2)

        with model.query(tag="count_connected_customers") as select:
            t = Transaction()
            num_records = aggregates.count(t.customer_id, t.order_ts, t.connected, t.connected.customer_id)
            select(num_records)

        with model.rule():
            t = Transaction()
            total_connections = aggregates.count(
                t, per=[t.customer_id, t.connected.customer_id]
            )
            total_connections > 4
            RelevantConnection.add(
                customer_1=Customer(customer_id=t.customer_id),
                customer_2=Customer(customer_id=t.connected.customer_id),
                total_connections=total_connections,
            )        

        # Get the total occurrences where pairs of customers coexisted together more than once
        with model.query(tag="count_meaningful_connected_customers") as select:
            record = RelevantConnection()
            num_records = aggregates.count(record)
            select(num_records)

        community_graph = Graph(model, undirected=True)

        # Add edges to the graph between customers / Nodes will be added automatically
        with model.rule():
            connection = RelevantConnection()
            community_graph.Edge.add(
                connection.customer_1,
                connection.customer_2,
                weight=connection.total_connections,
            )

        with model.rule():
            customer = Customer()
            community_id = community_graph.compute.louvain(customer)
            customer.set(community_id=community_id)

            community_graph.Node.add(
                customer,
                community_id=community_id,
                customer_id=customer.customer_id
            )

        with debugging.span("fetch", graph="louvain"):
            community_graph.fetch()