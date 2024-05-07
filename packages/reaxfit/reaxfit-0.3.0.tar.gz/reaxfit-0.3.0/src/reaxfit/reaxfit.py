from lammps import lammps
import json,os,sys,re
import numpy as np
from scipy.optimize import differential_evolution, minimize

# global parameters are required for multiprocessing
def wrap_eval(): pass

default_option={
            "refE_file":"refE", # reference energy file
            "refF_file":"refF", # reference force norm file
            "ref_eV":True, # units for reference energy is in eV
            "relative_force":True, # force norms are relative as refE
            "force_weight":1e-6, # penalty weight for force norms
            "harmonic":0, # harmonic constraint on initial parameters
            "datafile":"data0", # data file with initial structure
            "initfile":"ffield.temp", # initial template file
            "midfile":"ffield.currentbest", # intermediate file
            "endfile":"ffield.end", # final file
            "bound":0.1, # define range of parameters with "{"
            "bound2":0.1, # define range of parameters  with "["
            "stopfile":"STOP", # file for early stopping
            "seed":None, # seed for random number
            "tol":0.01, # tolerance for convergence
            "workers":4, # number of cpus
            "maxiter":1000, # maximum number of iteration
            "popsize":16, # popsize for differential_evolution
            "optimizer":"differential_evolution", # maximum number of iteration
            "scrdir":"scr", # scratch directory
            "uniform":False
}

class reaxfit():
  def __init__(self,cfile="config.json"):
    self.cfile=cfile
    self.option=default_option
    return

  def changes(self,para,file_name,atm1,atm2,numbers):
    with open(file_name) as f:
        text=f.read().splitlines()
    general =text[1].split()
    generals = int(general[0]) + 1
    atom=text[generals+1].split()
    atoms = int(atom[0])*4 +1 +3
    x = generals +atoms
    j=1 
    atm=[]
    atm_dict={}
    while j <= int(atom[0]):
        y = text[generals+1+j*4].split()
        atm.append(y[0])
        atm_dict[y[0]]=j
        j+=1
    bonds=text[x+1].split()
    bond_max =int(bonds[0])*2+2+x
    #print(x)
    i=x+1
    while i <= bond_max:
        regax=re.compile(f"^\s*{atm_dict[atm1]}\s+{atm_dict[atm2]}\s|^\s*{atm_dict[atm2]}\s+{atm_dict[atm1]}\s")
        fire=regax.findall(text[i])
        if len(fire) != 0:
            #print(i)
            #print(text[i])
            #print(text[i+1])
            d = text[i].split()
            if numbers <= 8:
                if d[numbers+1].startswith("{") or d[numbers+1].startswith("["):
                    pass
                elif para=="{":
                    d[numbers+1]="{"+d[numbers+1]
                    print(text[i])
                    print(d[numbers+1])
                else:
                    d[numbers+1]="["+d[numbers+1]
                    print(text[i])
                    print(d[numbers+1])
                result =" ".join(d)
                gyou = i
            else:
                i+=1
                gyou = i
                d = text[i].split()
                if d[numbers-9].startswith("{") or d[numbers-9].startswith("["):
                    pass
                elif para=="{":
                    d[numbers-9]="{"+d[numbers-9]
                    print(text[i])
                    print(d[numbers-9])
                    i-=1
                else:
                    d[numbers-9]="["+d[numbers-9]
                    print(text[i])
                    print(d[numbers-9])
                    i-=1
                    
                result=" ".join(d)
        i+=1
    with open(file_name) as f:
        l = f.readlines()
    del l[gyou]
    l.insert(gyou,f"{result}\n")
    with open(file_name,mode="w")as f:
        f.writelines(l)

  def config(self,**kwargs):
    if hasattr(kwargs,"cfile"): self.cfile=kwargs["cfile"]
    opt=self.option
    isconfig=os.path.isfile(self.cfile)
    if isconfig:
        print(f"read {self.cfile}")
        with open(self.cfile) as f:
            jwargs=json.load(f)
            optk=opt.keys()&jwargs.keys()
            opt.update(**{k:jwargs[k] for k in optk})
            if(optk != jwargs.keys()): 
                print("unrecognized options: ",*(jwargs.keys()-optk))
    # overwrite options if given
    if kwargs:
        optk=opt.keys()&kwargs.keys()
        opt.update(**{k:kwargs[k] for k in optk})
        if(optk != kwargs.keys()): 
            print("unrecognized options: ",*(kwargs.keys()-optk))
    self.option=opt
    #midfile=opt["midfile"]
    #stopfile=opt["stopfile"]
    for k in opt:
        setattr(self,k,opt[k])
    # create scratch directory
    os.makedirs(self.scrdir,exist_ok=True)
    # convert eV to kcal/mol if refE is in eV
    _coeff = 1.0/0.043364124 if self.ref_eV else 1.0
    # define the base points for relative energy
    if os.path.isfile(self.refE_file):
      with open(self.refE_file) as f:
        refE=f.read().split()
        _idx=[ i for i,v in enumerate(refE) if "*" in v ]+[len(refE)]
        if _idx[0] != 0: _idx = [0] + _idx # initial snapshot must be base
        _diff=[(i,j-i) for i,j in zip(_idx[:-1],_idx[1:])]
        self.base_indices=np.hstack([[i]*d for i,d in _diff])
        _idx2=[ i for i,v in enumerate(refE) if "**" in v ]
        # set diff mode
        if _idx2:
          self.base_indices+=[j*(i in _idx2) for i,d in _diff for j in np.roll(range(d),1)]
        refE=[en.replace("*","") for en in refE]
    else:
      self.base_indices=np.array([0])
      refE=[0.0]
    if os.path.isfile(self.refF_file):
      with open(self.refF_file) as f:
        refF=f.read().split()
    else:
      refF=[0.0]
    self.refE=np.array(refE,dtype=float)*_coeff # raw energy
    self.refF=np.array(refF,dtype=float)*_coeff # raw force norm
    self.refE_relative = self.refE - self.refE[self.base_indices]
    self.refF_relative = self.refF.copy()
    if self.relative_force: self.refF_relative-=self.refF[self.base_indices]
    # read template and x0
    with open(self.initfile) as f:
      _template=f.read()
    # with open("0.xyz") as f:
    #   _xyz=f.read()
    regex=re.compile("[\{\[][\d.-]+")
    x0=regex.findall(_template)
    isBound1=[x.startswith("{") for x in x0]
    #print(x0)
    self.x0=[float(x.strip("{").strip("[")) for x in x0]
    #print(x1)
    self.template = _template
    # change {S
    # define bounds
    if 0 in self.x0:
      sys.exit("error:0 cannot be used as a ffield parameter.")
    bounds=[]
    for i,x in enumerate(self.x0):
        if isBound1[i]:
            delta = abs(float(self.bound)*x)
            t = (x-delta,x+delta)
            bounds.append(t)
        else:
            sigma = abs(float(self.bound2)*x)
            k=(x-sigma,x+sigma)
            bounds.append(k)
    #print(bounds)
    self.bounds=bounds
    template=regex.sub("{}",_template)
    self.template=template
    # get elements from templates
    eles=re.findall(r"\n *(:?[A-Z][a-z]?) ",template)
    #idxs=sorted(set(re.findall("\n *\d+ +(\d+) +",_xyz)))
    #eles=re.findall(r"\n *(:?[A-Z][a-z]?)",_xyz)
    #eles=sorted(set(eles),key=eles.index)
    #idxs=[int(i) for i in idxs]
    #eles=[eles[i-1] for i in idxs]
    self.elements=" ".join(eles)
    #dump_best=self.callbackF
    return

  def callbackF(self,xk,convergence=False,fout=None):
    fname=self.option["midfile"]
    stopfile=self.option["stopfile"]
    sys.stdout.flush()
    if fout: fname=fout
    with open(fname,"w") as f:
        _x=np.round(xk,5)
        y=[f"{{{xx}" for xx in _x]
        f.write(self.template.format(*y))
    if os.path.isfile(stopfile):
        print("optimization will be stopped by the stop file")
        os.remove(stopfile)
        return True

  def set_eval(self,func):
    global wrap_eval
    if not hasattr(self,"x0"): self.config()
    _x0=np.array(self.x0)
    def wrap_eval(*args,**kwargs):
      pid=os.getpid()
      pes,fns=self.reax(*args,pid=pid)
      output = func(pes,fns,self.refE,self.refF) 
      if self.harmonic > 0:
        deltax=(np.array(args[0])-_x0)/(_x0+0.01)
        output+=deltax@deltax*self.harmonic
      return output
    return wrap_eval

  def reax(self,xk=None,pid=0):
      x=xk if xk is not None else self.x0
      ffname=f"{self.scrdir}/ffield.reax.{pid}"
      elements=self.elements
      pes,fns=[],[]
      with open(ffname,"w") as f:
          f.write(self.template.format(*np.round(x,6)))
      lmp=lammps(cmdargs=["-log", "none", "-screen", "none",  "-nocite"])
      for i in range(1):
          cmds=["units real",
              "atom_style charge",
              f"read_data {self.datafile}",
              "pair_style      reaxff NULL",
              f"pair_coeff      * * {ffname} {elements}",
              "fix             1 all qeq/reaxff 1 0.0 10.0 1.0e-6 reaxff"]
          lmp.commands_list(cmds)
          lmp.command("run 0 post no")
          pes.append(lmp.get_thermo("pe"))
          fns.append(lmp.get_thermo("fnorm"))
      if self.uniform == "False" or not self.uniform:
        b="add yes purge yes replace no "
      else:
        b=""
      for i in range(1,len(self.refE)):
        a=f"read_dump {i}.xyz 0 x y z box no "
        c="format xyz"
        lmp.command(a+b+c)
        lmp.command("run 0 post no")
        pes.append(lmp.get_thermo("pe"))
        fns.append(lmp.get_thermo("fnorm"))
      lmp.close()
      pes=np.array(pes)
      fns=np.array(fns)
      return pes,fns

  def default_func(self,*args,**kwargs):
    _x0=np.array(self.x0)
    pid=os.getpid()
    pes,fns=self.reax(*args,pid=pid)
    pes-=pes[self.base_indices] # initial structure is base by default
    pes-=self.refE_relative
    if self.relative_force: fns-=fns[self.base_indices]
    fns-=self.refF_relative
    fns*=self.force_weight
    fmax=np.abs(fns).max()
    output = pes@pes + np.linalg.norm(fns)+np.abs(pes).max()*np.abs(fns).max()+fmax**2
    if self.harmonic > 0:
      deltax=(np.array(args[0])-_x0)/(np.abs(_x0)+0.01)
      output+=deltax@deltax*self.harmonic
    return output

  def fit(self,myfunc=None):
      #global dump_best
      if not hasattr(self,"x0"): self.config()
      print("config parameters for fitting")
      json.dump(self.option,sys.stdout)
      print("")
      print(f"initial {len(self.x0)} parameters : {self.x0}")
      func = myfunc if myfunc else self.default_func
      if self.optimizer == "differential_evolution":
        result = differential_evolution(func, self.bounds,workers=self.workers,x0=self.x0,updating='deferred',
                                  disp=True,maxiter=self.maxiter,tol=self.tol,callback=self.callbackF,popsize=self.popsize,seed=self.seed)
      else:
        result = minimize(func,x0=self.x0,method=self.optimizer,tol=self.tol,callback=self.callbackF,jac='3-point') 
      print(result)
      self.callbackF(result.x,fout=self.endfile)
      self.result=result
      self.E,self.F=self.reax(result.x)
      return result

if __name__ =='__main__':
  pass
