"""Command-line entry points. Run from the project root."""
import argparse,subprocess,sys,json
from pathlib import Path
from src.project_config import DEFAULT_OPTIMIZER_SEED

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('test'); exp=sub.add_parser('experiments'); exp.add_argument('--workers',type=int,default=4); exp.add_argument('--budget',type=int,default=10000)
    one=sub.add_parser('one'); one.add_argument('--algorithm',type=int,required=True); one.add_argument('--problem',required=True); one.add_argument('--budget',type=int,default=10000); one.add_argument('--seed',type=int,default=DEFAULT_OPTIMIZER_SEED); one.add_argument('--objectives',type=int,default=3)
    sub.add_parser('report'); sub.add_parser('verify')
    args=p.parse_args(); root=Path(__file__).resolve().parent
    def call(*cmd): subprocess.run([sys.executable,*cmd],cwd=root,check=True)
    if args.command=='test': call('-m','unittest','discover','-s','tests','-v')
    elif args.command=='experiments':
        call('-m','src.experiments.runner','--workers',str(args.workers),'--budget',str(args.budget))
        call('-m','src.experiments.supplementary'); call('-c','from src.experiments.supplementary import population_study; population_study()'); call('-m','src.experiments.traces')
    elif args.command=='report':
        call('-m','src.experiments.build_deliverables'); call('-m','src.experiments.docx_report')
    elif args.command=='verify': call('-m','src.experiments.verify')
    else:
        import numpy as np
        from src.algorithms import load
        from src.problems import get_problem,SUPPLIERS
        a=load(args.algorithm)
        if args.algorithm in [8,9]: result=a.run(SUPPLIERS,[.3,.3,.2,.2],[False,True,False,True])
        else: result=a.run(get_problem(args.problem,args.objectives),budget=args.budget,seed=args.seed)
        print(json.dumps({k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in result.items()},indent=2))
if __name__=='__main__': main()
