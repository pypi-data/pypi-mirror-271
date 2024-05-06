import pstats

with open('cProfile_stats_cum.txt','w') as f:
    p = pstats.Stats('cProfile_report.txt',stream=f)
    p.sort_stats('cumtime').print_stats(100)
with open('cProfile_stats_tot.txt','w') as f:
    p = pstats.Stats('cProfile_report.txt',stream=f)
    p.sort_stats('tottime').print_stats(100)    