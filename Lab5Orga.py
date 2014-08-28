'Programa que simula  el tiempo que le toma entrar a una tienda y ser atendidos'
'hecho por : Erick Hernandez 13197 y Ma. Isabel Fernandez 13024'
import random
import simpy


RANDOM_SEED = 42
new_process=5
intervalo=10


def source(env, new_process, intervalo, RAM, CPU,WAITING ):
    """Source generates customers randomly"""
    tiempo=0
    for i in range(new_process):
        instruc = random.randint(1,10)
        memoria = random.randint(1,10)
        c = proceso(env, 'Customer%02d' % i, memoria, RAM, CPU, WAITING, instruc)
        env.process(c)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

def proceso(env, name, memoria, RAM, CPU, WAITING, instruc):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print arrive 
    print('%7.4f %s: New, esperando RAM, RAM DISPONIBLE:' % (arrive, name))
    with RAM.get(memoria) as req:
		yield req #espera que tenga mas memoria

		wait = env.now - arrive
		print('%7.4f %s: LISTO, espero memoria %6.3f' % (env.now, name, wait))
		while instruc > 0:
			with CPU.request() as reqCPU:
				yield reqCPU
                #print('%7.4f %s: RUNNING instrucciones %6.3f' % (env.now,name,wait))
				yield env.timeout(1)
				if instruc > 3:
					instruc = instruc - 3
				else:
					instruc = 0
					
			if instruc > 0:
				siguiente = random.choice(["ready","waiting"])
				if siguiente == "waiting":
					with WAITING.request() as reqWAITING:
						yield reqWAITING
						print ('%7.4f %s: WAITING' % (env.now,name))
						yield env.timeout(1)
                        
				print ('%7.4f %s: READY' % (env.now,name))
		tiempoProceso = env.now-arrive
		global tiempop
		tiempop = tiempop + tiempoProceso
		print ('%7.4f %s: TERMINATED tiempo ejecucion %s' % (env.now,name,tiempoProceso))
	
		with RAM.put(memoria) as reqDevolverRAM:
			yield reqDevolverRAM
			print ('%7.4f %s: regresando RAM %s' % (env.now,name,memoria))

print('SISTEMA OPERATIVO')
random.seed(RANDOM_SEED)
env = simpy.Environment()
CPU = simpy.Resource(env, capacity=1)
RAM= simpy.Container(env,init=100,capacity=100)
WAITING = simpy.Resource(env,capacity=1)
env.process(source(env, new_process,intervalo,RAM, CPU,WAITING ))
tiempop = 0
env.run()# Setup and start the simulation
print('TIEMPO PROMEDIO: %6.3f' % (tiempop/new_process))
