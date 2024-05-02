
def punto_cruze1(parent1: List[str], parent2: List[str]) -> (str, str):
			#parent1 = list(s)
			# seleccionde otro padre para cruzamiento
			#parent2 = list(random.choice(selection))
			
			# indice de corte
			i = random.randint(0, N-1)
			
			parent1_low = parent1[:i]
			parent1_high = parent1[i:]
			
			
			parent2_low = parent2[:i]
			parent2_high = parent2[i:]
			
			child1 = parent1_low + parent2_high
			child2 = parent1_high + parent2_low
			
			child1 = int(''.join(child1), 2)
			child2 = int(''.join(child2), 2)
			return child1, child2
