import numpy as np

class Cliente_uno():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "ClienteUNO {} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Cliente_dos():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "ClienteDOS {} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Event():
    NEW_TIPOUNO_ARRIVAL = 1
    NEW_TIPODOS_ARRIVAL = 2
    SUPERVISOR_EXIT = 3

    def __init__(self, time, event_type, client):
        self.time=time
        self.event_type=event_type
        self.client = client

    def __repr__(self):
        if self.event_type==self.NEW_CUSTOMER_ARRIVAL:
            return "{:6.2f} - Entro al sistema la Pieza {}".format(self.time, self.client.id)
        elif self.event_type==self.SUPERVISOR_EXIT:
            return "{:6.2f} - Pieza {} salio de supervision".format(self.time, self.client.id)
        else:
            return "{:6.2f} - Evento Desconocido".format(self.time)

    
        
def getTime(event):
    return event.time       

class Simulation():

    EMPTY = 0
    BUSY = 1

    def __init__(self, simulation_time=10000):
        self.simulation_time = simulation_time
        self.clock=0
        self.events=[]
        self.queue_clienteuno=[]
        self.queue_clientedos=[]
        self.exits=[]
        self.supervisor_state = self.EMPTY
        self.prepare_entries()

    def prepare_entries(self):
        time = 0
        id = 1
        while True:
            time += np.random.uniform(100,150)
            cliente_uno = Cliente_uno(id)
            id+=1
            cliente_uno.arrival_time = time
            self.events.append(Event(time,Event.NEW_TIPOUNO_ARRIVAL, cliente_uno))
            if time > self.simulation_time:
                self.events.pop()
                break
        time = 0
        id=1
        while True:
            time += 120
            cliente_dos = Cliente_dos(id)
            id+=1
            cliente_dos.arrival_time = time
            self.events.append(Event(time,Event.NEW_TIPODOS_ARRIVAL, cliente_dos))
            if time > self.simulation_time:
                self.events.pop()
                break
        self.events.sort(key=getTime)

    def next_event(self):
        event = self.events.pop(0);
        if event.event_type == Event.NEW_TIPOUNO_ARRIVAL:
            self.clock = event.time
        if event.event_type == Event.NEW_TIPODOS_ARRIVAL:
            self.clock = event.time
        return event


    def run(self):
        self.max_clientes_sistema = 0
        while self.events:
            event = self.next_event()
            self.clock = event.time
            if event.event_type == event.NEW_TIPOUNO_ARRIVAL:
                event.client.enter_queque_time = self.clock
                self.queue_clienteuno.append(event.client)
            elif event.event_type == event.NEW_TIPODOS_ARRIVAL:
                event.client.enter_queque_time = self.clock
                self.queue_clienteuno.append(event.client)
            elif event.event_type == event.SUPERVISOR_EXIT:
                self.supervisor_state = self.EMPTY
                event.client.exit_supervisor_time=self.clock
                self.exits.append(event.client)

            if self.supervisor_state == self.EMPTY and len(self.queue_clienteuno)>0:
                self.supervisor_state = self.BUSY
                next_client = self.queue_clienteuno.pop(0)
                #Se debera buscar cual es el cliente que llevan mas timepo esperando

                if type(next_client).__name__ == "Cliente_uno":
                    busy_time = np.random.exponential(25)
                else:
                    #Distribucion erlang no se como se pone
                    busy_time = np.random.gamma(2,35/2)

                next_client.enter_supervisor_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.SUPERVISOR_EXIT, next_client))
                self.events.sort(key=getTime)
            clientes_sistema = len(self.queue_clienteuno) + (self.supervisor_state == self.BUSY)
            if self.max_clientes_sistema < clientes_sistema:
                self.max_clientes_sistema = clientes_sistema
            if self.clock > self.simulation_time:
                break

sim = Simulation(simulation_time=60000)

sim.run()


timeinsystem = 0
for piece in sim.exits:
    timeinsystem += (piece.exit_supervisor_time - piece.arrival_time)
    print(piece)
print(timeinsystem/len(sim.exits))
print(sim.max_clientes_sistema)