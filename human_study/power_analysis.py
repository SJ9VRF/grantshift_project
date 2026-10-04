from statistics import NormalDist
import argparse, math, json

def n_two_proportions(p1,p2,alpha=.05,power=.8):
    # conservative normal approximation, independent-proportion equivalent; repeated-measures studies should refine with pilot ICC.
    z1=NormalDist().inv_cdf(1-alpha/2); z2=NormalDist().inv_cdf(power); p=(p1+p2)/2
    num=(z1*math.sqrt(2*p*(1-p))+z2*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    return math.ceil(num/((p1-p2)**2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--p1',type=float,default=.15); ap.add_argument('--p2',type=float,default=.08); ap.add_argument('--power',type=float,default=.8); args=ap.parse_args()
    print(json.dumps({'p1':args.p1,'p2':args.p2,'power':args.power,'approx_n_per_condition':n_two_proportions(args.p1,args.p2,power=args.power),'note':'normal approximation; use pilot-based mixed-effects simulation for preregistration'},indent=2))
