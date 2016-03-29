import pstats
p = pstats.Stats('profile')
p.sort_stats('tottime', 'module').print_stats()
