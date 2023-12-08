from transitions import Machine, EventData
from functools import partial
from networkx import DiGraph


def state_machine_from_graph(g: DiGraph):

    class StateMachine:
        """
        A global state machine. Use it as a singleton, or bad things will happen.
        """

        done = set([])

        def done_state(self, state):
            """
            done_state marks a state done from the outside
            """
            StateMachine.done.add(state)

        @classmethod
        def on_exit_state(cls, event: EventData):
            """
            on_exit_state is used on internal transitions
            """
            exited = event.transition.source
            print(f"exited: {exited}")
            cls.done.add(exited)

        @classmethod
        def on_enter_state(cls, event: EventData):
            """
            just informative for debug
            """
            print(f"entered: {event.state._name}")

        def check_condition_for(graph, dest, event):
            """
            check if the transition condition is met. returns True if the destination
            state can be reached from where we're at.
            """
            needed = set(list(graph.predecessors(dest)))

            if len(needed) == 1:
                # a node with a single predecessor can only advance to a single state
                return True

            current = event.state._name
            can_transition = set(StateMachine.done).union(set([current])).intersection(
                needed) == set(needed)
            return can_transition

        def advance(self):
            """
            move the state machine to the next available state. If there're more than one
            just pick one randomly - the others will act like a semaphore
            """
            _next = list(g.neighbors(self.state))
            if len(_next) == 0:
                print("we're done!")
                return True
            else:
                _next = _next[0]
                transition = (f"{self.state}_to_{_next}")
                fn = getattr(self, transition)
                return fn()

        def waiting_on(self):
            """
            return the set of the states we're currently waiting on
            """
            _next = list(g.neighbors(self.state))
            if len(_next) != 1:
                return []

            needed = set(list(g.predecessors(_next[0])))
            return needed.difference(set([self.state]).union(self.done))

    states = [
        {"name": node,
         "on_exit": "on_exit_state",
         "on_enter": "on_enter_state"}
        for node in g.nodes()
    ]

    # TODO: initial should be parsed from the yaml data tree (terminal too, this is validation)
    machine = Machine(
        model=StateMachine, states=states, initial="data", send_event=True
    )

    # Generate transitions based on DAG edges
    for edge in g.edges:
        trigger_name = f"{edge[0]}_to_{edge[1]}"
        transition = {
            "trigger": trigger_name,
            "source": edge[0],
            "dest": edge[1],
            "conditions": partial(StateMachine.check_condition_for, g, edge[1]),
        }
        machine.add_transition(**transition)

    sm = StateMachine()
    # a state machine acts as a singleton, and here we're setting the class attribute
    # to the empty set. this will break if you try to use more than one state machine at the time!
    sm.done = set([])
    return sm
